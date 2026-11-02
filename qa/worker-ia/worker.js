/**
 * RavenTechs — Servidor intermedio de IA (Cloudflare Worker)
 * Versión: 1.0 · 02/11/2026
 *
 * Para qué sirve: las apps con IA (CharlAR y Traductor de Hábitos) ya NO llevan la clave de Groq en el código.
 * La app le manda sus mensajes a este Worker junto con el token de sesión de Firebase del usuario; el Worker
 * comprueba que el usuario esté logueado en una de las apps autorizadas, le agrega la clave y consulta a Groq.
 *
 * Variable secreta que hay que cargar en Cloudflare (Settings → Variables and Secrets → tipo "Secret"):
 *   GROQ_KEY   = la clave NUEVA de Groq (la vieja hay que anularla en Groq)
 *
 * Qué NO hace: no guarda mensajes, no registra textos, no conoce el nombre ni el correo del usuario.
 */

// Apps autorizadas: projectId de Firebase → dominios desde los que se aceptan pedidos
const APPS = {
  'charlar-e5408':    ['https://charlar.raventechsapp.com'],
  'traductor-habitos': ['https://habitos.raventechsapp.com'],
};
const MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile'];
const MODELO_POR_DEFECTO = 'llama-3.1-8b-instant';
const MAX_TOKENS = 1000;       // tope por respuesta
const MAX_MENSAJES = 24;       // mensajes por pedido
const MAX_CARACTERES = 16000;  // texto total por pedido
const LIMITE_POR_MINUTO = 20;  // pedidos por usuario y minuto (por servidor, aproximado)

const JWK_URL = 'https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com';
let jwkCache = { keys: null, hasta: 0 };
const usos = new Map();

function cors(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
  };
}
function json(obj, status, origin) {
  return new Response(JSON.stringify(obj), {
    status, headers: Object.assign({ 'Content-Type': 'application/json' }, origin ? cors(origin) : {}),
  });
}
function b64uBytes(s) {
  s = s.replace(/-/g, '+').replace(/_/g, '/'); while (s.length % 4) s += '=';
  const bin = atob(s); const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
function b64uJson(s) { return JSON.parse(new TextDecoder().decode(b64uBytes(s))); }

async function claves() {
  if (jwkCache.keys && Date.now() < jwkCache.hasta) return jwkCache.keys;
  const r = await fetch(JWK_URL);
  if (!r.ok) throw new Error('No se pudieron leer las claves públicas de Google');
  const data = await r.json();
  const cc = r.headers.get('cache-control') || '';
  const m = cc.match(/max-age=(\d+)/);
  jwkCache = { keys: data.keys, hasta: Date.now() + (m ? Number(m[1]) : 3600) * 1000 };
  return jwkCache.keys;
}

// Comprueba la firma y los datos del token de sesión de Firebase. Devuelve { uid, projectId } o lanza error.
async function verificarToken(token) {
  const partes = (token || '').split('.');
  if (partes.length !== 3) throw new Error('token');
  const cab = b64uJson(partes[0]);
  const carga = b64uJson(partes[1]);
  if (cab.alg !== 'RS256' || !cab.kid) throw new Error('token');
  const proyecto = carga.aud;
  if (!APPS[proyecto]) throw new Error('app no autorizada');
  if (carga.iss !== 'https://securetoken.google.com/' + proyecto) throw new Error('emisor');
  const ahora = Math.floor(Date.now() / 1000);
  if (!carga.exp || carga.exp < ahora) throw new Error('vencido');
  if (carga.iat && carga.iat > ahora + 300) throw new Error('fecha');
  if (!carga.sub) throw new Error('sin usuario');
  const jwk = (await claves()).find(k => k.kid === cab.kid);
  if (!jwk) throw new Error('clave desconocida');
  const key = await crypto.subtle.importKey('jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64uBytes(partes[2]),
    new TextEncoder().encode(partes[0] + '.' + partes[1]));
  if (!ok) throw new Error('firma');
  return { uid: carga.sub, projectId: proyecto };
}

function demasiado(uid) {
  const ahora = Date.now();
  const lista = (usos.get(uid) || []).filter(t => ahora - t < 60000);
  if (lista.length >= LIMITE_POR_MINUTO) { usos.set(uid, lista); return true; }
  lista.push(ahora); usos.set(uid, lista);
  if (usos.size > 5000) usos.clear();
  return false;
}

export default {
  async fetch(request, env) {
    const origen = request.headers.get('Origin') || '';
    const permitidos = [].concat(...Object.values(APPS));

    if (request.method === 'OPTIONS') {
      return permitidos.includes(origen) ? new Response(null, { status: 204, headers: cors(origen) }) : new Response(null, { status: 403 });
    }
    if (request.method !== 'POST') return json({ error: 'Método no permitido' }, 405, permitidos.includes(origen) ? origen : null);
    if (!permitidos.includes(origen)) return json({ error: 'Origen no autorizado' }, 403, null);
    if (!env.GROQ_KEY) return json({ error: 'Servidor sin configurar' }, 500, origen);

    let sesion;
    try {
      const auth = request.headers.get('Authorization') || '';
      sesion = await verificarToken(auth.replace(/^Bearer\s+/i, ''));
      if (!APPS[sesion.projectId].includes(origen)) throw new Error('origen distinto de la app');
    } catch (e) {
      return json({ error: 'Sesión no válida. Volvé a iniciar sesión.' }, 401, origen);
    }
    if (demasiado(sesion.uid)) return json({ error: 'Demasiados pedidos seguidos. Esperá un minuto.' }, 429, origen);

    let cuerpo;
    try { cuerpo = await request.json(); } catch (e) { return json({ error: 'Pedido inválido' }, 400, origen); }
    const mensajes = Array.isArray(cuerpo.messages) ? cuerpo.messages : null;
    if (!mensajes || !mensajes.length || mensajes.length > MAX_MENSAJES) return json({ error: 'Mensajes inválidos' }, 400, origen);
    let total = 0;
    for (const m of mensajes) {
      if (!m || !['system', 'user', 'assistant'].includes(m.role) || typeof m.content !== 'string') return json({ error: 'Mensajes inválidos' }, 400, origen);
      total += m.content.length;
    }
    if (total > MAX_CARACTERES) return json({ error: 'Texto demasiado largo' }, 413, origen);

    const modelo = MODELOS.includes(cuerpo.model) ? cuerpo.model : MODELO_POR_DEFECTO;
    const maxTokens = Math.min(Math.max(parseInt(cuerpo.max_tokens, 10) || 400, 1), MAX_TOKENS);
    const temperatura = typeof cuerpo.temperature === 'number' ? Math.min(Math.max(cuerpo.temperature, 0), 1.2) : 0.6;

    const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + env.GROQ_KEY },
      body: JSON.stringify({ model: modelo, max_tokens: maxTokens, temperature: temperatura, messages: mensajes }),
    });
    const texto = await r.text();
    return new Response(texto, { status: r.status, headers: Object.assign({ 'Content-Type': 'application/json' }, cors(origen)) });
  },
};
