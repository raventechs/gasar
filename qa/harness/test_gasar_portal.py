# Prueba del portal de entrada de GasAR (index.html) con Firebase simulado. Servir el repo en el puerto 8781:
#   cd gasar && python3 -m http.server 8781
import asyncio, os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
FAKE=open(os.path.join(HERE,'fake_firebase_tw.js'),encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
BASE='http://127.0.0.1:8781/'
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)
USERS={
 'adm':{'rol':'administrador','activo':True,'ubicacionId':None},
 'adn':{'rol':'administracion','activo':True,'ubicacionId':None},
 'cam':{'rol':'vendedor_camioneta','activo':True,'ubicacionId':'ub2'},
 'rev':{'rol':'vendedor_revendedores','activo':True,'ubicacionId':'ub3'},
 'cen':{'rol':'vendedor_central','activo':True,'ubicacionId':'ub1'},
 'ina':{'rol':'vendedor_central','activo':False,'ubicacionId':'ub1'},
 'sub':{'rol':'vendedor_camioneta','activo':True,'ubicacionId':None},
}
async def nuevo(br,ua=None,previo=None):
    ctx=await br.new_context(viewport={'width':390,'height':844},user_agent=ua,service_workers='block') if ua else await br.new_context(viewport={'width':390,'height':844},service_workers='block')
    pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    async def gs(r):
        if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
        else: await r.fulfill(body='',content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw-*.js',lambda r:r.abort())
    await pg.goto(BASE+'index.html'); await pg.wait_for_timeout(500)
    await pg.evaluate("U=>{for(const k in U){window.__DB.set('usuarios/'+k,Object.assign({email:k+'@t.com',nombre:k,tenantId:'t1'},U[k]))}}",USERS)
    return ctx,pg,errs
async def probar(br,boton,uid,esperado):
    ctx,pg,errs=await nuevo(br)
    await pg.click(f'button[data-s={boton}]'); await pg.wait_for_timeout(200)
    await pg.evaluate("u=>window.__login({uid:u,email:u+'@t.com'})",uid); await pg.wait_for_timeout(900)
    url=pg.url
    try: txt=await pg.inner_text('#msg',timeout=1500)
    except Exception: txt=''
    await ctx.close(); return url,txt,errs
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        ctx,pg,e=await nuevo(br)
        n=await pg.evaluate("document.querySelectorAll('#vHome .sec').length")
        t=await pg.inner_text('#vHome')
        chk('bienvenida: 4 botones',n==4 and all(x in t for x in ['Administración','Reparto','Distribución','Venta mostrador']))
        await pg.click('button[data-s=admin]')
        chk('navegador común: no muestra aviso de navegador embebido',not await pg.is_visible('#boxEmbed'))
        await pg.click('#bVolver')
        await pg.click('button[data-s=reparto]')
        chk('al tocar un botón aparece el ingreso con Google y mail/clave',await pg.is_visible('#bGoogle') and await pg.is_visible('#em') and await pg.is_visible('#pw'))
        chk('volver regresa a los 4 botones',(await pg.click('#bVolver') or True) and await pg.is_visible('#vHome'))
        chk('sin errores JS',not e,e); await ctx.close()
        casos=[('admin','adm','gasar-admin.html',True),('admin','adn','gasar-admin.html',True),
               ('reparto','cam','gasar-vendedor.html',True),('distribucion','rev','gasar-vendedor.html',True),('mostrador','cen','gasar-vendedor.html',True),
               ('admin','cam',None,False),('admin','cen',None,False),('reparto','adm',None,False),('reparto','cen',None,False),('distribucion','cam',None,False),('mostrador','rev',None,False),
               ('mostrador','ina',None,False),('reparto','sub',None,False),('distribucion','nadie',None,False)]
        for b,u,dest,ok in casos:
            url,txt,e=await probar(br,b,u,ok)
            if ok: chk(f'{b} + {u}: entra a {dest}',url.endswith(dest),url)
            else: chk(f'{b} + {u}: NO entra y avisa "no tenés permiso habilitado"',(not url.endswith('.html') or url.endswith('index.html')) and 'No tenés permiso habilitado' in txt,txt)
            chk(f'{b} + {u}: sin errores JS',not e,e)
        # sin documento y en Administración: pasa a la app de administración, que la verifica (cuenta de soporte)
        url,txt,e=await probar(br,'admin','sinDoc',True)
        chk('administración sin documento: deriva a la app de administración (ella verifica)',url.endswith('gasar-admin.html'),url)
        # cuenta Raven (sin documento) por otro botón: ofrece la Consola Raven y no cierra la sesión
        ctx,pg,e=await nuevo(br)
        await pg.click('button[data-s=reparto]'); await pg.evaluate("window.__login({uid:'sinDoc',email:'raven@t.com'})"); await pg.wait_for_timeout(900)
        chk('Reparto sin documento: ofrece CONSOLA RAVEN',await pg.is_visible('#bConsola'))
        chk('sin documento: no cierra la sesión',await pg.evaluate("firebase.auth().currentUser!=null"))
        await pg.click('#bConsola'); await pg.wait_for_timeout(600)
        chk('CONSOLA RAVEN lleva a la app de administración',pg.url.endswith('gasar-admin.html'),pg.url)
        await ctx.close()
        # tocó el botón equivocado pero su usuario es válido en otra sección: ofrece ir a la suya
        ctx,pg,e=await nuevo(br)
        await pg.click('button[data-s=admin]'); await pg.evaluate("window.__login({uid:'cam',email:'cam@t.com'})"); await pg.wait_for_timeout(900)
        chk('botón equivocado: ofrece "IR A REPARTO"',await pg.is_visible('#bOtra') and 'REPARTO' in await pg.inner_text('#bOtra'))
        await pg.click('#bOtra'); await pg.wait_for_timeout(900)
        chk('y desde ahí entra a la app del vendedor sin pedir clave de nuevo',pg.url.endswith('gasar-vendedor.html'),pg.url)
        await ctx.close()
        # sesión ya abierta: tocar el botón verifica directo
        ctx,pg,e=await nuevo(br)
        await pg.evaluate("window.__login({uid:'cen',email:'cen@t.com'})"); await pg.wait_for_timeout(500)
        chk('con sesión abierta se queda en la bienvenida',pg.url.endswith('index.html') and await pg.is_visible('#vHome'))
        await pg.click('button[data-s=mostrador]'); await pg.wait_for_timeout(900)
        chk('con sesión abierta, el botón correcto entra directo',pg.url.endswith('gasar-vendedor.html'),pg.url)
        await ctx.close()
        # sin permiso → la sesión se cierra
        ctx,pg,e=await nuevo(br)
        await pg.click('button[data-s=admin]'); await pg.evaluate("window.__login({uid:'ina',email:'ina@t.com'})"); await pg.wait_for_timeout(900)
        chk('usuario inactivo: sesión cerrada',await pg.evaluate("firebase.auth().currentUser==null"))
        await ctx.close()
        # conexión inestable: Firestore "unavailable" dos veces y luego responde -> entra solo
        ctx,pg,e=await nuevo(br)
        await pg.evaluate("""()=>{window.__fail=2;const o=db.collection.bind(db);db.collection=n=>{const c=o(n);if(n!=='usuarios')return c;return {doc:id=>{const d=c.doc(id);const g=d.get.bind(d);return {get:async()=>{if(window.__fail-->0){const x=new Error('x');x.code='unavailable';throw x}return g()}}}}}}""")
        await pg.click('button[data-s=admin]'); await pg.evaluate("window.__login({uid:'adm',email:'adm@t.com'})"); await pg.wait_for_timeout(4500)
        chk('si Firestore falla 2 veces y luego responde: entra solo',pg.url.endswith('gasar-admin.html'),pg.url)
        await ctx.close()
        # conexión caída del todo: avisa, no cierra la sesión y permite reintentar
        ctx,pg,e=await nuevo(br)
        await pg.evaluate("""()=>{window.__fail=3;const o=db.collection.bind(db);db.collection=n=>{const c=o(n);if(n!=='usuarios')return c;return {doc:id=>{const d=c.doc(id);const g=d.get.bind(d);return {get:async()=>{if(window.__fail-->0){const x=new Error('x');x.code='unavailable';throw x}return g()}}}}}}""")
        await pg.click('button[data-s=admin]'); await pg.evaluate("window.__login({uid:'adm',email:'adm@t.com'})"); await pg.wait_for_timeout(5500)
        chk('sin conexión: muestra Reintentar y NO cierra la sesión',await pg.is_visible('#bReint') and await pg.evaluate("firebase.auth().currentUser!=null"))
        await pg.click('#bReint'); await pg.wait_for_timeout(1500)
        chk('al reintentar con conexión: entra sin pedir clave',pg.url.endswith('gasar-admin.html'),pg.url)
        await ctx.close()
        # navegador embebido
        ctx,pg,e=await nuevo(br,ua='Mozilla/5.0 (Linux; Android 13; wv) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36 Instagram 300.0')
        await pg.click('button[data-s=reparto]')
        chk('dentro de Instagram/WhatsApp: muestra el aviso y deja mail y clave',await pg.is_visible('#boxEmbed') and await pg.is_visible('#em'))
        await ctx.close()
        await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
