#!/usr/bin/env python3
"""Instructivo (ayuda/index.html) y folleto de Traductor de Hábitos."""
import sys, pathlib, re
sys.path.insert(0, '/home/claude/tools')
import gen_instructivos as G

REPO = pathlib.Path('/home/claude/raventechs-traductor-habitos')
steps, cards, faq = G.steps, G.cards, G.faq

app = dict(name='Traductor de Hábitos', emoji='🧬', color='#157a5f', tag='Registrá tus hábitos y entendé tus patrones',
  wa='Hola%20RavenTechs%2C%20necesito%20ayuda%20con%20Traductor%20de%20H%C3%A1bitos', secs=[
  ('¿Qué es Traductor de Hábitos?', '<p>Es una app para registrar lo que hacés día a día (comida, sueño, ánimo, actividad, pulso, peso, glucemia) y descubrir cómo se relacionan entre sí. Registrás hablando o escribiendo, y la inteligencia artificial ordena tus registros y te muestra patrones.</p><div class="aviso"><b>Importante:</b> es una herramienta de observación personal, sin juicios. No reemplaza el diagnóstico, el consejo ni el tratamiento de un profesional de la salud.</div>'),
  ('Instalar la app en tu celular', '<p><b>En Android (Chrome)</b></p>' + steps([
    'Abrí <b>habitos.raventechsapp.com</b> en Chrome.',
    'Tocá <b>Instalar</b> en el cartel de abajo. Si no aparece, tocá los tres puntitos de arriba a la derecha y elegí <b>Instalar aplicación</b>.',
    'Listo: queda el ícono en tu pantalla de inicio, como cualquier app.']) + '<p><b>En iPhone (Safari)</b></p>' + steps([
    'Abrí el link en <b>Safari</b> (no en Chrome).', 'Tocá <b>Compartir</b> (el cuadradito con la flecha hacia arriba).', 'Elegí <b>Agregar a pantalla de inicio</b> y después <b>Agregar</b>.'])),
  ('Entrar a tu cuenta', steps([
    'Tocá <b>Continuar con Google</b> y elegí tu cuenta de Gmail (es la opción más simple).',
    'Si preferís, usá tu email y una contraseña y tocá <b>Registrarte</b> la primera vez.']) + '<div class="aviso">Entrá siempre con la <b>misma cuenta</b>: así tus registros están en todos tus dispositivos.</div>'),
  ('Tu prueba gratis de 14 días', '<p>Cuando creás tu cuenta tenés <b>14 días de prueba gratis</b> con todo funcionando. Arriba ves un cartel con los días que te quedan; cuando faltan 3 o menos se pone rojo y titila.</p><p>Al terminar, la app se bloquea con un mensaje. <b>No perdés ningún dato</b>: al activar tu cuenta sigue todo como lo dejaste. Incluso con la prueba vencida podés <b>descargar tus datos</b>.</p><a class="btn" href="' + G.WA + 'Hola%20RavenTechs%2C%20quiero%20activar%20mi%20cuenta%20de%20Traductor%20de%20H%C3%A1bitos">📲 Activar mi cuenta por WhatsApp</a>'),
  ('Conocer las pantallas', cards([
    ('🏠 Hoy', 'Una observación del día escrita por la IA según tus últimos registros, tu índice TH de la semana y tus últimos descubrimientos.'),
    ('🎤 Registrar', 'Tocá el micrófono y hablá, o escribí en el recuadro y tocá <b>Guardar</b>. En <b>Auto</b> la IA elige la categoría; también podés elegirla vos: Comida, Pulso, Sueño, Ánimo, Actividad, Peso o Glucemia.'),
    ('🔍 Descubrir', 'Tocá <b>Analizar ahora</b> y el motor cruza tus registros para encontrar comparaciones, patrones, tendencias y sugerencias. Necesitás al menos 4 registros.'),
    ('🧬 Mi Huella', 'Tu perfil que crece con cada registro: total de registros, días activos, el hábito más frecuente, tu último pulso y gráficos de los últimos 7 días.'),
    ('👤 Perfil', 'Modo oscuro, copia de seguridad, modo práctica, este instructivo y cerrar sesión.'),
    ('🤖 Asistente', 'El botón del robot abre un chat donde le preguntás cosas sobre tus propios hábitos.')])),
  ('Practicar sin miedo', '<p>Si querés ver la app funcionando antes de cargar tus datos:</p>' + steps([
    'Andá a <b>Perfil</b>.', 'Tocá <b>Cargar datos de práctica</b>: la app suma registros de ejemplo de dos semanas.',
    'Probá <b>Analizar ahora</b> en Descubrir y mirá Mi Huella.',
    'Cuando termines, tocá <b>Quitar datos de práctica</b>. Se borran solo los de ejemplo; <b>tus registros reales no se tocan</b>.'])),
  ('Copia de seguridad', '<p>La app guarda sola una copia <b>una vez por día</b> al abrirla. También podés hacerla cuando quieras:</p>' + steps([
    'Andá a <b>Perfil</b>.', 'Tocá <b>Descargar backup</b>. Se baja un archivo con la fecha.',
    'Para recuperar datos, tocá <b>Restaurar backup</b> y elegí ese archivo. Lo que ya tenés no se borra.']) + '<div class="aviso">Guardá el archivo también en tu Google Drive o mandátelo por mail.</div>'),
  ('Tu privacidad', '<p>Tus registros se guardan en tu cuenta y la app no permite que otros usuarios los lean. Para clasificarlos y generar observaciones, el texto se envía a un servicio de inteligencia artificial <b>sin tu nombre ni tu email</b>.</p>'),
  ('Preguntas frecuentes', faq([
    ('La IA dice que no está disponible', 'Puede ser un problema pasajero. Tus registros se guardan igual (quedan como "otro") y podés volver a intentar más tarde.'),
    ('El micrófono no anda', 'Revisá que hayas dado permiso de micrófono al navegador. Si no, escribí el registro en el recuadro.'),
    ('Me equivoqué en un registro', 'Podés borrarlo desde la lista de últimos registros y cargarlo de nuevo.'),
    ('¿Se pierden mis datos si cambio de celular?', 'No. Entrás con tu cuenta y está todo. Además podés bajar un backup desde Perfil.'),
    ('La app no se actualiza', 'Cerrala del todo y volvé a abrirla. Si sigue igual, desinstalala y volvé a instalarla desde el link.')])),
])

d = REPO / 'ayuda'; d.mkdir(exist_ok=True)
(d / 'index.html').write_text(G.page(app), encoding='utf-8')
print('ok ayuda')

# ── Folleto (molde de CarneAR) ──
tpl = pathlib.Path('/home/claude/carnear/ayuda/../../raventechs.github.io/folletos/folleto-carnear.html').read_text(encoding='utf-8')
css = re.search(r'<style>(.*?)</style>', tpl, re.S).group(1)
script = re.search(r'<script>(.*?)</script>', tpl, re.S).group(1)
css = css.replace('#c0392b', '#1E8C6E')
css = re.sub(r'--glow:[^;]*;', '--glow:#1E8C6E26;', css)
css = re.sub(r'\.plus-[^\n]*\n', '', css)
URL = 'https://habitos.raventechsapp.com/'
q = [('¿Sabés si dormir poco te cambia el ánimo del día siguiente?', '¿O lo notás recién cuando ya estás cansado?'),
     ('¿Cuántas cosas anotás de tu salud y las perdés en el celular?', 'Traductor de Hábitos las ordena y las cruza por vos.')]
f = [('🎤', 'Registrá hablando', 'Decilo en voz alta o escribilo: la IA lo ordena'),
     ('🔍', 'Descubrí patrones', 'Cruza sueño, comida, ánimo y actividad'),
     ('🧬', 'Mi Huella', 'Tu perfil que crece con cada registro'),
     ('🤖', 'Asistente', 'Preguntale cosas sobre tus propios hábitos')]
esc = G.esc
html = f'''<!--
  Folleto Traductor de Hábitos · RavenTechs
  Versión: 1.0
  Fecha: 2026-11-02
  Changelog:
   - 1.0: primer folleto (molde de los demás folletos).
  PENDIENTE:
   - Capturas reales de la app
-->
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Folleto Traductor de Hábitos — RavenTechs</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>{css}
.feat:last-child:nth-child(even){{grid-column:1/-1;}}</style>
</head>
<body>
<section class="hero">
  <div class="badge">🧬 Hábitos y bienestar</div>
  <span class="hero-emoji">🧬</span>
  <h1>Tu cuerpo habla.
Nosotros lo traducimos.</h1>
  <p style="max-width:520px;color:var(--text2);line-height:1.6;margin-bottom:28px;">Registrá tus hábitos hablando o escribiendo y descubrí cómo se relacionan entre sí, con observaciones sin juicios.</p>
  <a href="{URL}" class="cta-btn" target="_blank">Probá Traductor de Hábitos gratis →</a>
</section>

<section class="preguntas">
  <h2>¿Te suena esto?</h2>
  {''.join(f'<div class="pregunta-card"><p>{esc(a)}</p><span>{esc(b)}</span></div>' for a, b in q)}
</section>

<section class="features">
  <h2>Qué incluye Traductor de Hábitos</h2>
  <div class="feat-grid">
    {''.join(f'<div class="feat"><span class="feat-icon">{i}</span><div class="feat-title">{esc(t)}</div><div class="feat-desc">{esc(d_)}</div></div>' for i, t, d_ in f)}
  </div>
</section>

<section class="footer-cta">
  <h2>Empezá hoy, sin instalar nada.</h2>
  <p>Funciona desde el navegador de tu celular. Probala 14 días gratis.</p>
  <p style="font-size:12px;margin-top:-8px">Herramienta de observación personal: no reemplaza el consejo médico.</p>
  <a href="{URL}" class="cta-btn" target="_blank">Abrir Traductor de Hábitos →</a>
  <div class="footer-brand">Una app de <span>RavenTechs</span> · raventechs.github.io</div>
</section>

<script>{script}</script>
</body>
</html>
'''
out = pathlib.Path('/home/claude/raventechs.github.io/folletos/folleto-habitos.html')
out.write_text(html, encoding='utf-8')
print('ok folleto')
