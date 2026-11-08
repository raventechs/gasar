#!/usr/bin/env python3
"""Genera probar/index.html: landing de entrega instantanea de la prueba (una sola pagina para todas las apps)."""
import json, pathlib

apps = json.load(open('/tmp/apps.json', encoding='utf-8'))
COL = dict(carnear='#c0392b', pizzar='#e74c3c', panar='#e67e22', puntoventa='#16a085', lavar='#2980b9', barbear='#d4a017',
           pelotear='#27ae60', securepro='#27ae60', empresar='#0ea5e9', rodix='#8e44ad', manejar='#22c55e', saludar='#06b6d4',
           miagenda='#3498db', habitos='#1E8C6E', timbrear='#c8a84b', comprazona='#f97316', gasar='#0a57c8')
DIAS14 = {'carnear','pizzar','panar','puntoventa','lavar','barbear','pelotear','securepro','empresar','rodix','saludar','miagenda','manejar','habitos'}
PRACTICA = {'carnear','pizzar','panar','puntoventa','lavar','barbear','pelotear','securepro','empresar','rodix','saludar','miagenda','habitos'}

data = {}
for a in apps:
    data[a['id']] = dict(n=a['n'], e=a['e'], t=a['t'], d=a['d'], b=a['b'], ok=a['ok'], url=a['url'], demo=a.get('demo'),
                         ficha=a.get('ficha'), ayuda=a.get('ayuda'), c=COL.get(a['id'], '#f0b84a'),
                         dias=a['id'] in DIAS14, practica=a['id'] in PRACTICA)

HTML = r'''<!--
  ARCHIVO: probar/index.html
  VERSIÓN: v1.0
  FECHA: 02/11/2026
  PROYECTO: RavenTechs — Landing de entrega instantánea de la prueba (Pilar 1 del embudo de demos)
  CHANGELOG:
  - v1.0 (02/11/2026): una sola página para todas las apps (?app=<id>&ref=<código del vendedor>). Muestra qué es la app,
    los 3 primeros pasos, botón para abrir la prueba (reenvía el código del vendedor), instructivo, folleto y WhatsApp.
  PENDIENTE:
  - Medir visitas por vendedor (requiere colección en Firestore y reglas)
  - Los datos de las apps salen del catálogo de vendedores/index.html: si cambia allá, regenerar esta página
-->
<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Tu prueba gratis — RavenTechs</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--c:#f0b84a;--bg:#0a0c12;--bg2:#12151f;--tx:#eef0f6;--mu:#8b93ad;--bd:rgba(255,255,255,.1)}
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--tx);overflow-wrap:anywhere}
.w{max-width:560px;margin:0 auto;padding:20px 18px 40px}
.hero{text-align:center;padding:34px 8px 22px;background:radial-gradient(ellipse 80% 60% at 50% 0%,color-mix(in srgb,var(--c) 22%,transparent),transparent 70%)}
.badge{display:inline-block;border:1px solid var(--bd);background:rgba(255,255,255,.05);color:var(--mu);padding:6px 14px;border-radius:99px;font-size:12px;font-weight:700;letter-spacing:.5px;text-transform:uppercase}
.emo{font-size:64px;margin:18px 0 6px}
h1{font-size:30px;line-height:1.15;margin-bottom:8px}
h1 span{color:var(--c)}
.sub{color:var(--mu);font-size:16px;line-height:1.5;margin:0 auto 22px;max-width:440px}
.btn{display:block;text-align:center;text-decoration:none;font-weight:800;font-size:17px;padding:16px 20px;border-radius:14px;margin:10px 0;border:2px solid var(--c)}
.pri{background:var(--c);color:#fff;box-shadow:0 8px 28px color-mix(in srgb,var(--c) 35%,transparent)}
.sec{background:transparent;color:var(--tx)}
.wa{background:#25D366;border-color:#25D366;color:#fff}
.card{background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:18px;margin-top:18px}
.card h2{font-size:13px;color:var(--c);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px}
.step{display:flex;gap:12px;align-items:flex-start;margin:12px 0;line-height:1.45}
.n{flex:0 0 32px;height:32px;border-radius:50%;background:var(--c);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800}
ul{list-style:none}li{padding:8px 0;border-bottom:1px solid var(--bd);display:flex;gap:10px}li:last-child{border:0}li:before{content:'✓';color:var(--c);font-weight:800}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
.grid a{display:block;background:var(--bg2);border:1px solid var(--bd);border-radius:14px;padding:14px;text-align:center;color:var(--tx);text-decoration:none;font-weight:700;font-size:14px}
.grid a span{display:block;font-size:26px}
.aviso{margin-top:14px;font-size:14px;color:var(--mu);text-align:center;line-height:1.5}
footer{text-align:center;color:var(--mu);font-size:12px;margin-top:30px}footer b{color:var(--c)}
</style></head><body><div class="w" id="app"></div>
<script>
const APPS = __DATA__;
const WA = '5491136547592';
const q = new URLSearchParams(location.search);
const id = (q.get('app') || '').toLowerCase();
const ref = (q.get('ref') || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 24);
const root = document.getElementById('app');

function el(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  for (const k in (attrs || {})) { if (k === 'class') e.className = attrs[k]; else e.setAttribute(k, attrs[k]); }
  kids.flat().forEach(c => e.append(c && c.nodeType ? c : document.createTextNode(c ?? '')));
  return e;
}
const conRef = u => ref ? u + (u.includes('?') ? '&' : '?') + 'ref=' + encodeURIComponent(ref) : u;
const wa = txt => 'https://wa.me/' + WA + '?text=' + encodeURIComponent(txt);

function lista() {
  document.title = 'Probá una app gratis — RavenTechs';
  root.append(el('div', { class: 'hero' }, el('div', { class: 'badge' }, 'RavenTechs'), el('h1', {}, 'Elegí qué app querés probar')));
  const g = el('div', { class: 'grid' });
  Object.entries(APPS).filter(([, a]) => a.ok).forEach(([k, a]) =>
    g.append(el('a', { href: '?app=' + k + (ref ? '&ref=' + encodeURIComponent(ref) : '') }, el('span', {}, a.e), a.n)));
  root.append(g, pie());
}
function pie() { return el('footer', {}, 'Una app de ', el('b', {}, 'RavenTechs')); }

function landing(a) {
  document.title = 'Tu prueba gratis de ' + a.n + ' — RavenTechs';
  document.documentElement.style.setProperty('--c', a.c);
  const dias = a.dias ? '14 días gratis' : 'Probala gratis';
  const hero = el('div', { class: 'hero' },
    el('div', { class: 'badge' }, a.t),
    el('div', { class: 'emo' }, a.e),
    el('h1', {}, 'Tu prueba de ', el('span', {}, a.n), a.dias ? ' por 14 días' : ''),
    el('p', { class: 'sub' }, a.d));
  root.append(hero);

  if (!a.ok) {
    root.append(el('div', { class: 'card' }, el('h2', {}, 'Próximamente'), el('p', {}, a.n + ' todavía está en desarrollo. Escribinos y te avisamos cuando esté lista.')),
      el('a', { class: 'btn wa', href: wa('Hola RavenTechs, quiero que me avisen cuando esté lista ' + a.n) }, '📲 Avisame por WhatsApp'), pie());
    return;
  }

  root.append(el('a', { class: 'btn pri', href: conRef(a.url) }, '▶ Abrir ' + a.n + ' — ' + dias));
  if (a.demo && a.demo !== a.url) root.append(el('a', { class: 'btn sec', href: a.demo }, '👀 Solo mirar la demo'));

  const pasos = [
    ['Tocá el botón de arriba.', ' Se abre en tu celular, no hace falta instalar nada de la tienda.'],
    ['Ingresá con Google.', a.dias ? ' Con eso se crea tu prueba y tenés 14 días para usar todo.' : ' Elegí tu cuenta de Gmail para guardar tus datos.'],
    a.practica ? ['Probá con datos de ejemplo.', ' En Configuración tocá “Cargar datos de práctica” para ver la app funcionando; después los quitás con un toque y tus datos reales no se tocan.']
               : ['Mirá la guía paso a paso.', ' Es corta y te muestra cómo empezar.']
  ];
  root.append(el('div', { class: 'card' }, el('h2', {}, 'Empezá en 3 pasos'),
    ...pasos.map((p, i) => el('div', { class: 'step' }, el('div', { class: 'n' }, String(i + 1)), el('div', {}, el('b', {}, p[0]), p[1])))));

  root.append(el('div', { class: 'card' }, el('h2', {}, 'Qué te da ' + a.n), el('ul', {}, a.b.map(x => el('li', {}, x)))));

  const rec = el('div', { class: 'grid' });
  if (a.ayuda) rec.append(el('a', { href: a.ayuda }, el('span', {}, '📖'), 'Instructivo'));
  if (a.ficha) rec.append(el('a', { href: a.ficha }, el('span', {}, '📄'), 'Folleto'));
  if (rec.children.length) root.append(rec);

  root.append(el('a', { class: 'btn wa', href: wa('Hola RavenTechs, estoy probando ' + a.n + (ref ? ' (código ' + ref + ')' : '') + ' y tengo una consulta') }, '📲 Tengo una duda'),
    el('p', { class: 'aviso' }, 'Si te gusta, escribinos y la activamos. Tus datos no se pierden al terminar la prueba.'), pie());
}

if (APPS[id]) landing(APPS[id]); else lista();
</script></body></html>
'''
import os
out = pathlib.Path(os.environ.get('OUT', '/home/claude/raventechs.github.io/probar'))
out.mkdir(exist_ok=True)
(out / 'index.html').write_text(HTML.replace('__DATA__', json.dumps(data, ensure_ascii=False)), encoding='utf-8')
print('ok', len(data))
