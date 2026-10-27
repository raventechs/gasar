// Backend simulado de Firestore + Auth con las reglas de Rodix (tal cual el comentario del index.html)
let SECURE = false; const setSecure = v => { SECURE = v; };
const store = new Map();           // path -> data
const users = new Map();           // email -> {uid, pass}
let seq = 1000;
const ADMIN = 'rgaraventa@gmail.com';
const isTs = v => v && typeof v === 'object' && '__ts' in v;
const resolveSV = d => JSON.parse(JSON.stringify(d, (k, v) => (v && v.__sv ? { __ts: Date.now() } : v)));
const cmp = (a, b) => { const x = isTs(a) ? a.__ts : a, y = isTs(b) ? b.__ts : b; return x < y ? -1 : x > y ? 1 : 0; };
const seg = p => p.split('/');
const isDocPath = p => seg(p).length % 2 === 0;

function authEmail(auth) { return auth && auth.email; }
function get(p) { return store.has(p) ? store.get(p) : undefined; }
function miUsuario(auth) { const u = get('usuarios/' + auth.uid); if (!u) throw new Error('sin usuario'); return u; }
const miFlotaId = a => miUsuario(a).flotaId;
const esChofer = a => miUsuario(a).rolFlota === 'chofer';
const esAdmin = a => authEmail(a) === ADMIN;
const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);

const changed = (a, b) => { const ks = new Set([...Object.keys(a || {}), ...Object.keys(b || {})]); return [...ks].filter(k => !eq((a || {})[k], (b || {})[k])); };
function allowedSecure(op, path, existing, incoming, auth) {
  try {
    const s = seg(path);
    if (s[0] === 'usuarios') {
      if (op === 'read') return !!auth && (auth.uid === s[1] || esAdmin(auth) || (existing && existing.flotaId === auth.uid) || miFlotaId(auth) === s[1]);
      if (!auth) return false;
      if (op === 'create') return auth.uid === s[1] && incoming.rolFlota === 'owner' && incoming.flotaId === auth.uid && incoming.status === 'demo' && !incoming.banned && Object.keys(incoming.features || {}).join() === 'limiteVehiculos' && incoming.features.limiteVehiculos === 1;
      if (op === 'update') {
        if (esAdmin(auth)) return true;
        const ch = changed(existing, incoming);
        const PROT = ['features', 'status', 'banned', 'demoStart', 'demoExpiry', 'uid', 'email'];
        if (ch.some(k => PROT.includes(k))) return false;
        if (auth.uid === s[1]) {
          if (!ch.includes('flotaId') && !ch.includes('rolFlota')) return true;                    // edición propia sin tocar flota
          const inv = get('invitaciones/' + incoming.inviteId);                                      // unirse como chofer: invitación válida y sin usar
          return ch.every(k => ['flotaId', 'rolFlota', 'inviteId'].includes(k)) && incoming.rolFlota === 'chofer' && !!inv && inv.usado === false && inv.ownerUid === incoming.flotaId && incoming.flotaId !== auth.uid;
        }
        return existing.flotaId === auth.uid && incoming.flotaId === s[1] && incoming.rolFlota === 'owner' && ch.every(k => ['flotaId', 'rolFlota'].includes(k));   // el dueño quita a un chofer
      }
      if (op === 'delete') return esAdmin(auth);
    }
    if (s[0] === 'invitaciones') {
      if (!auth) return false;
      if (op === 'read') return true;
      if (op === 'create') return incoming.ownerUid === auth.uid && !esChofer(auth) && incoming.usado === false;
      if (op === 'update') return existing.usado === false && incoming.usado === true && incoming.usadoUid === auth.uid && changed(existing, incoming).every(k => ['usado', 'usadoPor', 'usadoUid'].includes(k));
      return false;
    }
    if (s[0] === 'errores') return op === 'create' ? true : (op === 'read' && esAdmin(auth));
    return allowedBase(op, path, existing, incoming, auth);
  } catch (e) { return false; }
}
function allowed(op, path, existing, incoming, auth) { return SECURE ? allowedSecure(op, path, existing, incoming, auth) : allowedBase(op, path, existing, incoming, auth); }
function allowedBase(op, path, existing, incoming, auth) {   // op: read|create|update|delete
  try {
    const s = seg(path);
    if (s[0] === 'vehicles') {
      if (!auth) return false;
      const vid = s[1];
      const vdata = s.length === 2 ? existing : get('vehicles/' + vid);
      if (s.length === 2) {
        if (op === 'read') return existing.uid === miFlotaId(auth) || esAdmin(auth);
        if (op === 'create') return incoming.uid === auth.uid && !esChofer(auth);
        if (op === 'update') return existing.uid === miFlotaId(auth) && !esChofer(auth);
        if (op === 'delete') return (existing.uid === miFlotaId(auth) && !esChofer(auth)) || esAdmin(auth);
      }
      const dueno = vdata && (vdata.uid === miFlotaId(auth) || esAdmin(auth));
      const sub = s[2];
      if (sub === 'docs' || sub === 'services') return op === 'read' ? dueno : (!esChofer(auth) && dueno);
      if (sub === 'insumos') {
        if (op === 'read' || op === 'update') return dueno;
        return !esChofer(auth) && dueno;
      }
      if (sub === 'revisiones') {
        if (op === 'read' || op === 'create') return dueno;
        return !esChofer(auth) && dueno;
      }
      return false;
    }
    if (s[0] === 'usuarios') {
      if (!auth) return false;
      if (op === 'read') return true;
      if (op === 'create') return auth.uid === s[1];
      if (op === 'update') return esAdmin(auth) ||
        (auth.uid === s[1] && eq(incoming.features, existing.features)) ||
        (existing.flotaId === auth.uid && incoming.flotaId === s[1] && incoming.rolFlota === 'owner');
      if (op === 'delete') return esAdmin(auth);
    }
    if (s[0] === 'invitaciones') {
      if (op === 'read') return true;
      if (op === 'create') return !!auth && incoming.ownerUid === auth.uid && !esChofer(auth);
      if (op === 'update') return !!auth;
      return false;
    }
    return false; // colecciones sin regla (errores, etc.) => denegado
  } catch (e) { return false; }
}

const denied = () => ({ err: 'permission-denied' });
function matchWhere(d, w) {
  return w.every(([f, op, v]) => {
    const x = f.split('.').reduce((o, k) => (o == null ? undefined : o[k]), d);
    if (op === '==') return eq(x, v); if (op === '!=') return !eq(x, v);
    if (op === 'in') return v.some(y => eq(x, y));
    if (x === undefined) return false;
    const c = cmp(x, v); return op === '<' ? c < 0 : op === '<=' ? c <= 0 : op === '>' ? c > 0 : op === '>=' ? c >= 0 : false;
  });
}
function handle(auth, op, a) {
  if (op === 'get') {
    const d = get(a.path);
    if (d === undefined) {   // en Firestore real, leer doc inexistente evalúa reglas con resource null; aprobamos si el usuario podría leer
      return { exists: false };
    }
    if (!allowed('read', a.path, d, null, auth)) return denied();
    return { exists: true, data: d };
  }
  if (op === 'list') {
    const prefix = a.path + '/';
    let docs = [...store.keys()].filter(k => k.startsWith(prefix) && seg(k).length === seg(a.path).length + 1)
      .map(k => ({ id: k.split('/').pop(), path: k, data: store.get(k) })).filter(x => matchWhere(x.data, a.where || []));
    for (const x of docs) if (!allowed('read', x.path, x.data, null, auth)) return denied();
    (a.order || []).slice().reverse().forEach(([f, dir]) => docs.sort((p, q) => (dir === 'desc' ? -1 : 1) * cmp(p.data[f], q.data[f])));
    if (a.limit) docs = docs.slice(0, a.limit);
    return { docs: docs.map(x => ({ id: x.id, data: x.data })) };
  }
  if (op === 'set' || op === 'update' || op === 'delete' || op === 'add') {
    let path = a.path; if (op === 'add') path = a.path + '/auto' + (++seq);
    const ex = get(path);
    if (op === 'delete') { if (ex === undefined) return { ok: true, path }; if (!allowed('delete', path, ex, null, auth)) return denied(); store.delete(path); return { ok: true, path }; }
    const inc = resolveSV(a.data);
    if (op === 'update') {
      if (ex === undefined) return { err: 'not-found' };
      const merged = Object.assign({}, ex); for (const [k, v] of Object.entries(inc)) {
        if (k.includes('.')) { const [h, ...r] = k.split('.'); merged[h] = Object.assign({}, merged[h], { [r.join('.')]: v }); } else merged[k] = v; }
      if (!allowed('update', path, ex, merged, auth)) return denied(); store.set(path, merged); return { ok: true, path };
    }
    const merged = a.merge && ex ? Object.assign({}, ex, inc) : inc;
    const kind = ex === undefined ? 'create' : 'update';
    if (!allowed(kind, path, ex, merged, auth)) return denied();
    store.set(path, merged); return { ok: true, path };
  }
  if (op === 'signup') { if (users.has(a.email)) return { err: 'auth/email-already-in-use' }; const u = { uid: 'uid_' + a.email.split('@')[0], pass: a.pass }; users.set(a.email, u); return { uid: u.uid, email: a.email }; }
  if (op === 'signin') { const u = users.get(a.email); if (!u || u.pass !== a.pass) return { err: 'auth/invalid-credential' }; return { uid: u.uid, email: a.email }; }
  return { err: 'op?' };
}
module.exports = { setSecure, store, users, handle, seed: (p, d) => store.set(p, d) };
