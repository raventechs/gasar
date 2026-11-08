#!/usr/bin/env python3
"""Genera folletos de RavenTechs con el molde de folleto-carnear.html (contenido: solo lo que dice el catalogo)."""
import re, sys, html, pathlib

BASE = pathlib.Path('/home/claude/raventechs.github.io/folletos')
tpl = (BASE / 'folleto-carnear.html').read_text(encoding='utf-8')

# --- molde: CSS y script del folleto de CarneAR (sin el bloque PLUS) ---
css = re.search(r'<style>(.*?)</style>', tpl, re.S).group(1)
script = re.search(r'<script>(.*?)</script>', tpl, re.S).group(1)
css = css.replace('#c0392b', '@ACC@')  # color del molde

APPS = [
  dict(file='folleto-barbear.html', name='BarbeAR', emoji='💈', acc='#d4a017', badge='Barberías',
    h1='Tu barbería llena,\nsin contestar mensajes.', url='https://barbear.raventechsapp.com/',
    sub='La barbería maneja su caja y sus turnos, y el cliente reserva solo desde un link, sin mensajes ni llamadas.',
    q=[('¿Cuántos mensajes contestás por día para dar un turno?', '¿Y cuántos clientes no aparecen a la hora acordada?'),
       ('¿Tenés la agenda y la caja en el mismo lugar?', 'BarbeAR junta turnos y caja en una sola app.')],
    f=[('🔗','Reservas online por link','El cliente elige su turno solo'),
       ('📅','Agenda y caja juntas','Todo en un solo lugar'),
       ('🔕','Menos ausencias','Menos mensajes para confirmar turnos'),
       ('📱','Desde el celular','Sin instalar nada, desde el navegador')]),
  dict(file='folleto-empresar.html', name='EmpresAR', emoji='📋', acc='#0ea5e9', badge='Empresas y flotas',
    h1='Que no se te venza\nningún documento.', url='https://garrafar.raventechsapp.com/',
    sub='Habilitaciones, seguros, VTV y documentación del personal: la empresa carga todo y recibe aviso antes de cada vencimiento.',
    q=[('¿Sabés hoy qué documento de tu empresa vence primero?', '¿O te enterás cuando ya venció y llegó la multa?'),
       ('¿La documentación de tus vehículos y tu personal está toda en un lugar?', 'EmpresAR la junta en un solo panel.')],
    f=[('⏰','Alertas antes del vencimiento','Te avisa antes de que venza cada documento'),
       ('🗂️','Todo en un solo panel','Habilitaciones, seguros, VTV y personal'),
       ('🚚','Ideal para flotas','Y para empresas reguladas'),
       ('📱','Desde el celular','Sin instalar nada, desde el navegador')]),
  dict(file='folleto-manejar.html', name='manejAr', emoji='🚕', acc='#22c55e', badge='Choferes de apps',
    h1='Cuánto ganás de verdad,\ndespués de los gastos.', url='https://raventechs.github.io/ManejAr/manejar.html',
    sub='Para choferes de Uber, Didi y Cabify: muestra cuánto ganan de verdad después de combustible y gastos, y ofrece un plan para flotas.',
    q=[('¿Cuánto te quedó hoy después de poner combustible?', '¿O lo sabés recién a fin de mes?'),
       ('¿Manejás una flota de autos para apps?', 'manejAr tiene un plan para dueños de flota.')],
    f=[('💵','Ganancia real','Por viaje y por día'),
       ('⛽','Combustible y gastos','Todo descontado de lo que cobrás'),
       ('🚗','Plan para flotas','Para dueños de varios autos'),
       ('📱','Desde el celular','Sin instalar nada, desde el navegador')]),
  dict(file='folleto-comprazona.html', name='CompraZona', emoji='🛒', acc='#f97316', badge='Garrafas y agua',
    h1='Tu garrafa o tu agua,\ncon un toque.', url='https://comprazona.raventechsapp.com/',
    sub='Los vecinos piden garrafas y agua a las empresas de su zona con el mapa y el historial de pedidos; las empresas reciben los pedidos en tiempo real.',
    q=[('¿Cuánto tardás en conseguir una garrafa cuando se acaba?', '¿Y a quién le pedís si el de siempre no contesta?'),
       ('¿Tenés una empresa de reparto?', 'Recibís los pedidos de tu zona en tiempo real.')],
    f=[('🗺️','Mapa de empresas cercanas','El vecino ve quién reparte en su zona'),
       ('⚡','Pedidos en tiempo real','La empresa los recibe al instante'),
       ('🔁','Repetir un pedido','Con un solo toque'),
       ('📱','Desde el celular','Sin instalar nada, desde el navegador')]),
]

def e(s): return html.escape(s, quote=False)

def build(a):
    c = css.replace('@ACC@', a['acc'])
    c = re.sub(r'--glow:[^;]*;', '--glow:' + a['acc'] + '26;', c)
    c = re.sub(r'/\* ?PLUS.*?(?=\n\.footer-cta)', '', c, flags=re.S) if 'plus-section' in c else c
    c = re.sub(r'\.plus-[^\n]*\n', '', c)
    qs = ''.join(f'<div class="pregunta-card"><p>{e(p)}</p><span>{e(s)}</span></div>' for p, s in a['q'])
    fs = ''.join(f'<div class="feat"><span class="feat-icon">{i}</span><div class="feat-title">{e(t)}</div><div class="feat-desc">{e(d)}</div></div>' for i, t, d in a['f'])
    return f'''<!--
  Folleto {a['name']} · RavenTechs
  Versión: 1.0
  Fecha: 2026-11-02
  Changelog:
   - 1.0: primer folleto de {a['name']} (molde de los demás folletos). Contenido tomado del catálogo de la app de vendedores.
  PENDIENTE:
   - Capturas reales de la app cuando haya un cliente de referencia
-->
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Folleto {a['name']} — RavenTechs</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>{c}
.feat:last-child:nth-child(even){{grid-column:1/-1;}}</style>
</head>
<body>
<section class="hero">
  <div class="badge">{a['emoji']} {e(a['badge'])}</div>
  <span class="hero-emoji">{a['emoji']}</span>
  <h1>{e(a['h1'])}</h1>
  <p style="max-width:520px;color:var(--text2);line-height:1.6;margin-bottom:28px;">{e(a['sub'])}</p>
  <a href="{a['url']}" class="cta-btn" target="_blank">Probá {a['name']} gratis →</a>
</section>

<section class="preguntas">
  <h2>¿Te suena esto?</h2>
  {qs}
</section>

<section class="features">
  <h2>Qué incluye {a['name']}</h2>
  <div class="feat-grid">
    {fs}
  </div>
</section>

<section class="footer-cta">
  <h2>Empezá hoy, sin instalar nada.</h2>
  <p>Funciona desde el navegador de tu celular.{'' if a['name'] == 'CompraZona' else ' Probala 14 días gratis.'}</p>
  <a href="{a['url']}" class="cta-btn" target="_blank">Abrir {a['name']} →</a>
  <div class="footer-brand">Una app de <span>RavenTechs</span> · raventechs.github.io</div>
</section>

<script>{script}</script>
</body>
</html>
'''

for a in APPS:
    (BASE / a['file']).write_text(build(a), encoding='utf-8')
    print('ok', a['file'])
