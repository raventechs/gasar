#!/usr/bin/env python3
"""Instructivos (ayuda/index.html + PDF) de TimbreAR, CompraZona y GasAR con el molde de CarneAR."""
import re, pathlib, html as H

tpl = pathlib.Path('/home/claude/carnear/ayuda/index.html').read_text(encoding='utf-8')
CSS = re.search(r'<style>(.*?)</style>', tpl, re.S).group(1)
WA = 'https://wa.me/5491136547592?text='

def esc(s): return H.escape(s, quote=False)

def steps(items):
    return ''.join(f'<div class="step"><div class="n">{i}</div><div>{t}</div></div>' for i, t in enumerate(items, 1))

def cards(items):
    return ''.join(f'<div class="card"><b>{t}</b><p>{d}</p></div>' for t, d in items)

def faq(items):
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items)

def page(a):
    nav = ''.join(f'<a href="#s{i}">{i}. {t}</a>' for i, (t, _) in enumerate(a['secs'], 1))
    body = ''.join(f'<section id="s{i}"><h2>{i}. {t}</h2>{c}</section>' for i, (t, c) in enumerate(a['secs'], 1))
    ayuda = f'<a class="btn" href="{WA}{a["wa"]}">📲 Hablar con RavenTechs</a>'
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Guía de uso de {a['name']}</title>
<style>{CSS.replace('#9b1c1c', a['color'])}body{{overflow-wrap:anywhere}}</style></head><body><div class="w">
<header><div style="font-size:52px">{a['emoji']}</div><h1>{a['name']}</h1><p>Guía de uso paso a paso</p><p style="font-size:15px;margin-top:8px;opacity:.8">{a['tag']}</p></header>
<nav><b style="font-size:21px">¿Qué querés hacer?</b>{nav}</nav>
{body}
<section id="ayuda"><h2>{len(a['secs'])+1}. Necesito ayuda</h2><p>Escribinos y te respondemos lo antes posible.</p>{ayuda}</section>
<footer>{a['name']} · RavenTechs</footer></div></body></html>'''

# ───────────────────────── TimbreAR ─────────────────────────
timbrear = dict(name='TimbreAR', emoji='🔔', color='#b86e00', tag='Portero virtual para edificios',
  wa='Hola%20RavenTechs%2C%20necesito%20ayuda%20con%20TimbreAR', secs=[
  ('¿Qué es TimbreAR?', '<p>TimbreAR es el portero virtual de tu edificio. La visita escanea un código QR en la entrada, elige el departamento y al residente le llega el aviso en su celular. El residente atiende, habla o chatea con la visita y, si quiere, le abre la puerta.</p><p>No hace falta portero, intercom ni instalar nada para la visita: todo funciona desde el navegador del celular.</p>'),
  ('Quién usa qué', cards([
    ('🏢 Administrador', 'Arma el edificio en la consola, carga los departamentos, manda los links a los residentes e imprime el QR.'),
    ('🔔 Residente', 'Abre su link personal, activa su timbre y recibe el aviso cuando alguien toca su departamento.'),
    ('🚪 Visita', 'Escanea el QR de la entrada, toca el departamento que busca y espera que le atiendan.')])),
  ('Probar primero la demo', '<p>Antes de armar tu edificio podés ver cómo funciona de punta a punta, sin tocar datos reales:</p>' + steps([
    'Abrí <b>timbrear.raventechsapp.com</b> en tu celular.',
    'Tocá <b>Probar el timbre (demo completa)</b>.',
    'Tocá un departamento y mirá cómo le llega el aviso al residente, cómo atiende y cómo abre la puerta.'])),
  ('Administrador: armar el edificio', steps([
    'Entrá a la consola de administración (<b>Soy administrador</b> en la portada).',
    'Tocá <b>Nuevo edificio</b> y completá el nombre, la dirección y la ciudad.',
    'En <b>Departamentos</b> cargalos de a uno con <b>+ Agregar depto</b>, o todo un piso con <b>+ Agregar piso completo</b> (ponés el número de piso y las letras).',
    'Si ya tenés una lista, usá <b>Importar desde lista</b> y pegá una línea por departamento con el formato <b>DEPTO, NOMBRE, TELÉFONO</b>.',
    'Tocá <b>Guardar edificio</b>.']) + '<div class="aviso">Los edificios de la consola se guardan en el navegador que usás. Bajá una copia de seguridad (sección 8) y usá siempre el mismo celular o computadora.</div>'),
  ('Administrador: avisar a los residentes', steps([
    'En el edificio, tocá <b>Ver mensaje</b> para revisar el texto que van a recibir.',
    'Tocá <b>Enviar a todos</b>: se abre un WhatsApp por cada residente con su link personal para activar el timbre.',
    'En <b>Activaciones</b> ves quién ya activó y quién todavía no. Con <b>Reenviar pendientes</b> les mandás el link de nuevo a los que faltan.',
    'En <b>Códigos QR</b> generás el QR del edificio. Imprimilo y pegalo en la entrada.'])),
  ('Residente: activar mi timbre', steps([
    'Abrí el link que te mandó el administrador por WhatsApp.',
    'Completá tu nombre y tocá <b>Activar mi timbre</b>.',
    'Aceptá las notificaciones cuando el celular te pregunte. Es lo que permite que te avisen aunque no tengas la app abierta.',
    'Instalá la app: tocá el ícono de compartir del navegador y elegí <b>Agregar a pantalla de inicio</b> (en Android, <b>Instalar</b>).']) +
    '<p>Cuando alguien toque tu departamento vas a ver <b>Alguien en la puerta</b>, con tres opciones:</p>' + cards([
    ('📵 Rechazar', 'Cortás el aviso.'), ('📷 Foto', 'Podés ver la foto de la visita, cuando está disponible.'), ('📞 Atender', 'Hablás por audio o escribís por chat. Con el botón de la llave 🔓 abrís la puerta.')]) +
    '<p>Para no recibir avisos de noche, usá <b>No molestar</b> y elegí desde y hasta qué hora. En la pantalla ves las <b>últimas visitas</b>.</p>'),
  ('Visita: cómo llamar', steps([
    'Escaneá el QR de la entrada con la cámara del celular.',
    'Tocá el departamento que buscás.',
    'Esperá un momento: si el residente atiende, hablan por audio o chat.',
    'Si te abren, vas a ver <b>¡Puerta abierta!</b> y ya podés ingresar. Si no contestan, aparece <b>Sin respuesta</b> y podés <b>Volver a llamar</b>.'])),
  ('Copia de seguridad', '<p>La consola baja sola una copia de los edificios <b>una vez por día</b> al abrirla. También podés hacerla cuando quieras:</p>' + steps([
    'Entrá al <b>Dashboard</b> de la consola.',
    'Tocá <b>Descargar backup ahora</b>. Se baja un archivo con la fecha.',
    'Para recuperar los edificios, tocá <b>Restaurar desde un archivo</b> y elegí ese archivo.']) + '<div class="aviso">Guardá el archivo también en tu Google Drive o mandátelo por mail.</div>'),
  ('Preguntas frecuentes', faq([
    ('Al residente no le llega el aviso', 'Verificá que haya activado el timbre desde su link, que haya aceptado las notificaciones y que tenga la app instalada en la pantalla de inicio. Si sigue sin llegar, escribinos.'),
    ('La visita no ve ningún departamento', 'Revisá que el QR corresponda al edificio correcto y que el edificio tenga departamentos cargados y guardados.'),
    ('Un residente se mudó o cambió de celular', 'Mandale de nuevo su link de activación desde Activaciones. Al abrirlo en el celular nuevo vuelve a activar su timbre.'),
    ('La visita puede ver los nombres de los vecinos', 'No. La visita solo ve el número de cada departamento; el nombre y el teléfono quedan privados.')])),
])

# ───────────────────────── CompraZona ─────────────────────────
comprazona = dict(name='CompraZona', emoji='🛒', color='#c2570c', tag='Marketplace local de garrafas y agua',
  wa='Hola%20RavenTechs%2C%20necesito%20ayuda%20con%20CompraZona', secs=[
  ('¿Qué es CompraZona?', '<p>CompraZona es un mercado local de garrafas y agua. Los vecinos piden a las empresas de su zona desde el celular, con un mapa y su historial de pedidos. Las empresas reciben cada pedido en su panel, en tiempo real.</p><p>Esta guía tiene una parte para el <b>vecino</b> (quien pide) y otra para la <b>empresa</b> (quien reparte).</p>'),
  ('Vecino: instalar la app', '<p><b>En Android (Chrome)</b></p>' + steps([
    'Abrí <b>comprazona.raventechsapp.com</b> en Chrome.',
    'Tocá <b>Instalar</b> en el cartel de abajo. Si no aparece, tocá los tres puntitos y elegí <b>Instalar aplicación</b>.',
    'Listo: queda el ícono de CompraZona en tu pantalla de inicio.']) + '<p><b>En iPhone (Safari)</b></p>' + steps([
    'Abrí el link en <b>Safari</b>.', 'Tocá <b>Compartir</b> y elegí <b>Agregar a pantalla de inicio</b>.'])),
  ('Vecino: entrar y dar permisos', steps([
    'Tocá <b>Ingresar con Google</b> y elegí tu cuenta. La usamos para registrar tus pedidos y guardar tu historial.',
    'La primera vez aparece <b>Una sola vez</b>: la app te pide <b>Ubicación</b> (para mostrarte las empresas más cercanas) y <b>Notificaciones</b> (para avisarte que tu pedido está en camino). Tocá <b>Dar permisos y entrar</b>.']) + '<div class="aviso">Podés tocar <b>Omitir por ahora</b>, pero sin ubicación no te mostramos las empresas más cerca de tu casa.</div>'),
  ('Vecino: hacer un pedido', steps([
    'En el inicio elegí qué necesitás: <b>Garrafas</b> o <b>Agua</b>. También podés usar <b>Mapa</b> para ver las empresas cerca tuyo.',
    'Elegí una empresa de <b>Empresas en tu zona</b> y mirá sus productos.',
    'Tocá <b>Pedir</b> en lo que necesitás y después <b>Confirmar pedido</b>.',
    'Completá la <b>dirección de entrega</b>, tu <b>teléfono</b> y, si querés, una <b>nota para la empresa</b>.',
    'Tocá <b>Enviar pedido por WhatsApp</b> y confirmá con <b>Sí, enviar pedido</b>. El pedido queda registrado y se abre WhatsApp con el mensaje para la empresa.']) + '<p>En <b>Mis pedidos</b> ves tu historial y podés repetir un pedido con un toque.</p>'),
  ('Empresa: entrar al panel', steps([
    'La alta de tu empresa la hace RavenTechs con el email de Google que vas a usar. Pasanos nombre, WhatsApp, dirección, horario y tus productos con precios.',
    'Abrí <b>comprazona.raventechsapp.com/empresa.html</b> desde tu celular y tocá <b>Ingresar con Google</b>.',
    'Si te aparece <b>Tu cuenta no está vinculada a una empresa</b>, es normal la primera vez: avisanos y la vinculamos con ese email.']) + '<p>Guardá el link en tu pantalla de inicio para abrir el panel como una app.</p>'),
  ('Empresa: pedidos, productos y datos', cards([
    ('📋 Pedidos', 'Ves los pedidos nuevos en tiempo real. Podés filtrar por <b>Activos</b>, <b>Entregados</b> o <b>Todos</b>.'),
    ('🏷️ Productos', 'Tocá el precio para cambiarlo: se actualiza al instante en el marketplace. El botón 👁 muestra u oculta un producto. Con <b>+</b> agregás uno nuevo (nombre, precio y categoría).'),
    ('⚙️ Mi negocio', 'Editás el nombre, la dirección, el WhatsApp (con 549 y sin espacios), el tiempo estimado de entrega y el horario de atención. No te olvides de tocar <b>Guardar cambios</b>.')])),
  ('Preguntas frecuentes', faq([
    ('No me aparecen empresas cerca', 'Revisá que hayas dado permiso de ubicación a la app. Si lo negaste, activalo desde los ajustes del navegador y volvé a abrir CompraZona.'),
    ('Me equivoqué en el precio de un producto', 'En Productos tocá el precio, ponés el nuevo y confirmás. El cambio se ve enseguida.'),
    ('No me llegan los pedidos', 'Verificá en Mi negocio que el WhatsApp esté bien escrito (con 549, sin espacios) y que tengas el panel abierto o instalado.'),
    ('La app no se actualiza', 'Cerrala del todo y volvé a abrirla. Si sigue igual, desinstalala y volvé a instalarla desde el link.')])),
])

# ───────────────────────── GasAR ─────────────────────────
gasar = dict(name='GasAR', emoji='🔥', color='#0a57c8', tag='Sistema para distribuidoras de gas',
  wa='Hola%20RavenTechs%2C%20necesito%20ayuda%20con%20GasAR', secs=[
  ('¿Qué es GasAR?', '<p>GasAR junta en un solo sistema a la central, las camionetas y los revendedores de tu distribuidora. Cada venta se carga una sola vez, donde ocurre, y el stock de garrafas llenas y vacías, la caja y las cuentas se actualizan solos. Vos lo ves todo en tiempo real.</p>'),
  ('Quién ve qué', cards([
    ('👑 Dueño / Administración', 'Ve todo en tiempo real: ventas, stock, caja y diferencias. Maneja compras, gastos y precios, aprueba las rendiciones y baja reportes.'),
    ('🏪 Mostrador y revendedores', 'Cargan ventas, cargan camionetas, cobran y reciben envases, y abren y cierran caja.'),
    ('🚚 Chofer', 'Recibe la carga, vende (con o sin señal), anota gastos y rinde la camioneta al volver.')])),
  ('Entrar al sistema', steps([
    'El administrador entra a <b>raventechs.github.io/gasar/gasar-admin.html</b> con <b>Entrar con Google</b>.',
    'El personal (mostrador, choferes) entra a <b>raventechs.github.io/gasar/gasar-vendedor.html</b>.',
    'Tocá <b>Instalar</b> para dejar GasAR en la pantalla de inicio del celular.'])),
  ('Primer armado', '<p>Antes de vender, el administrador deja listo el negocio:</p>' + steps([
    'Cargá los <b>productos</b> (garrafas de cada tamaño) con su precio y las <b>marcas de envases</b>.',
    'Creá los <b>puntos de venta</b>: la central, cada camioneta y cada revendedor.',
    'Creá los <b>usuarios</b> con su email y su rol, y asignales su punto de venta.']) + '<div class="aviso">Si querés aprender sin riesgo, pedile a RavenTechs una <b>distribuidora de práctica</b> ya armada, con precios, stock y camionetas de ejemplo.</div>'),
  ('Vender una garrafa', '<p>Una venta se carga en pocos toques. Ejemplo: garrafa de 10 kg, el cliente entrega un envase vacío y paga en efectivo:</p>' + steps([
    'Elegí el producto (10 kg).', 'Indicá si el cliente <b>entrega envase</b>.', 'Elegí el medio de pago.', 'Tocá <b>CONFIRMAR</b>.']) +
    '<p>El sistema descuenta una garrafa llena, suma un envase vacío y suma el importe a la caja, con el usuario y la hora anotados.</p><div class="aviso">Si no hay internet, la venta queda guardada en el celular y sube sola cuando vuelve la señal, sin duplicarse.</div>'),
  ('Camionetas: cargar y rendir', steps([
    'Para mandar una camioneta, cargá lo que lleva con <b>ENVIAR CARGA</b>. Sale del stock de la central.',
    'Quien recibe la camioneta confirma con <b>APROBAR RECEPCIÓN</b>. Si hay diferencia, queda registrada.',
    'Durante el día el chofer vende y anota sus gastos.',
    'Al volver, el chofer rinde la camioneta: devuelve las llenas y vacías que sobraron y la plata. Administración compara contra lo esperado y aprueba la rendición.'])),
  ('Revendedores y cuenta corriente', '<p>Los revendedores compran al por mayor. Pueden pagar en el momento o dejar la deuda a cuenta. En <b>Revendedores</b> ves la <b>cuenta</b> de cada uno: lo que debe en plata y en envases, y con <b>REGISTRAR PAGO</b> anotás cada cobro.</p>'),
  ('Compras, proveedores y gastos', steps([
    'Con <b>REGISTRAR COMPRA</b> cargás lo que le comprás a un proveedor: las garrafas llenas suman al stock de la central y el pago descuenta de la caja. También se registra el canje de vacíos.',
    'En <b>Proveedores</b> ves la cuenta corriente de cada uno y registrás los pagos.',
    'Los <b>gastos</b> se cargan desde cualquier punto y se pueden anular, con historial.'])),
  ('Caja y reportes', '<p>El <b>Resumen</b> muestra el dinero real por caja abierta y los movimientos del día. Con <b>Exportar CSV</b> bajás ventas, stock, compras, gastos, cuentas corrientes y movimientos para abrirlos en Excel.</p>'),
  ('Copia de seguridad', steps([
    'El sistema baja una copia <b>una vez por día</b> cuando el administrador entra.',
    'Cuando quieras, tocá <b>Descargar backup ahora</b>.',
    'Para recuperar el catálogo, tocá <b>Restaurar catálogo desde un archivo</b> y elegí ese archivo.']) + '<div class="aviso">Guardá el archivo también en tu Google Drive o mandátelo por mail.</div>'),
  ('Preguntas frecuentes', faq([
    ('Me equivoqué en una venta o en una compra', 'Usá <b>Anular</b> en esa operación: queda el registro y el stock y la caja se corrigen.'),
    ('La camioneta volvió con diferencia', 'Es normal que a veces haya diferencias. Queda anotada en la rendición para que Administración la revise antes de aprobar.'),
    ('Un chofer no tiene señal', 'Puede vender igual. Las ventas suben solas cuando vuelve la conexión.'),
    ('¿Factura electrónica?', 'Todavía no está incluida. Es una etapa que estamos preparando.')])),
])

OUT = {
  'timbrear': ('/home/claude/timbrear/ayuda', 'Guia-TimbreAR', timbrear),
  'comprazona': ('/home/claude/comprazona/ayuda', 'Guia-CompraZona', comprazona),
  'gasar': ('/home/claude/gasar/ayuda', 'Guia-GasAR', gasar),
}
if __name__ == '__main__':
    for k, (d, pdf, a) in OUT.items():
        p = pathlib.Path(d); p.mkdir(exist_ok=True)
        (p / 'index.html').write_text(page(a), encoding='utf-8')
        print('ok', k)
