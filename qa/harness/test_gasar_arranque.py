# Prueba de la pestaña "Puesta en marcha" de GasAR admin (modo Raven). Servir el repo: cd gasar && python3 -m http.server 8781
import asyncio, os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
FAKE=open(os.path.join(HERE,'fake_firebase_tw.js'),encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
FAKE+="""
;(function(){const f=window.firebase;f.apps=[];const base=f.initializeApp;
 f.initializeApp=function(c,n){ if(n==='sec'){return {auth:()=>({createUserWithEmailAndPassword:async(e,p)=>{ if(e.indexOf('dup')===0){const x=new Error('dup');x.code='auth/email-already-in-use';throw x} window.__CREADOS=(window.__CREADOS||[]).concat([[e,p]]);return {user:{uid:'uid_'+e}}},signOut:async()=>{}})}} return base.apply(this,arguments)}})();
"""
BASE='http://127.0.0.1:8781/'
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)
async def abrir(br,raven=True):
    ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    async def gs(r):
        if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
        else: await r.fulfill(body='',content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw-*.js',lambda r:r.abort())
    await pg.goto(BASE+'gasar-admin.html'); await pg.wait_for_timeout(700)
    await pg.evaluate("""r=>{window.__DB.set('tenants/t1',{nombre:'Gas Test',plan:'full'});
      window.__DB.set('tenants/t1/ubicaciones/uC',{nombre:'Central',tipo:'central',activa:true});
      window.__DB.set('usuarios/ad1',{email:'dueno@t.com',nombre:'Dueño',rol:'administrador',activo:true,tenantId:'t1',ubicacionId:null});}""",raven)
    if raven:
        await pg.evaluate("window.__login({uid:'rv',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(1200)
        await pg.evaluate("entrarTenant('t1')"); await pg.wait_for_timeout(800)
    else:
        await pg.evaluate("window.__login({uid:'ad1',email:'dueno@t.com',emailVerified:true})"); await pg.wait_for_timeout(1200)
    return ctx,pg,errs
async def llenar(pg,sel,val):
    await pg.fill(sel,val)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        # dueño común: no ve la pestaña
        ctx,pg,e=await abrir(br,raven=False)
        chk('el dueño común NO ve la pestaña Puesta en marcha',await pg.evaluate("![...document.querySelectorAll('nav button')].some(b=>b.textContent.includes('Puesta en marcha'))"))
        await pg.evaluate("S.tab='arranque';render()"); await pg.wait_for_timeout(300)
        chk('aunque force la pestaña no ve el formulario (cae al Resumen)',not await pg.evaluate("document.body.innerText.includes('CREAR TODO')"))
        await ctx.close()
        ctx,pg,e=await abrir(br)
        chk('Raven ve la pestaña',await pg.evaluate("[...document.querySelectorAll('nav button')].some(b=>b.textContent.includes('Puesta en marcha'))"))
        await pg.evaluate("document.querySelector('nav button[data-v=arranque]').click()"); await pg.wait_for_timeout(300)
        chk('muestra el formulario',await pg.is_visible('text=CREAR TODO'))
        # puntos: 1 camioneta + 1 revendedores
        await pg.fill('input[data-pm=pun][data-i="0"][data-k=n]','Camioneta 1')
        await pg.click('button[data-a=arp]'); await pg.wait_for_timeout(200)
        await pg.fill('input[data-pm=pun][data-i="1"][data-k=n]','Revendedores Norte')
        await pg.select_option('select[data-pm=pun][data-i="1"][data-k=t]','revendedores')
        # personas
        await pg.fill('input[data-pm=usu][data-i="0"][data-k=e]','Chofer@Test.com'); await pg.fill('input[data-pm=usu][data-i="0"][data-k=n]','Chofer Uno')
        await pg.select_option('select[data-pm=usu][data-i="0"][data-k=p]','Camioneta 1')
        await pg.click('button[data-a=aru]'); await pg.wait_for_timeout(200)
        chk('lo escrito se conserva al agregar una fila',await pg.input_value('input[data-pm=usu][data-i="0"][data-k=e]')=='Chofer@Test.com')
        await pg.fill('input[data-pm=usu][data-i="1"][data-k=e]','rev@test.com'); await pg.fill('input[data-pm=usu][data-i="1"][data-k=n]','Rev Uno')
        await pg.select_option('select[data-pm=usu][data-i="1"][data-k=r]','vendedor_revendedores')
        await pg.select_option('select[data-pm=usu][data-i="1"][data-k=p]','Revendedores Norte')
        await pg.click('button[data-a=aru]'); await pg.wait_for_timeout(200)
        await pg.fill('input[data-pm=usu][data-i="2"][data-k=e]','mostrador@test.com'); await pg.fill('input[data-pm=usu][data-i="2"][data-k=n]','Mostrador Uno')
        await pg.select_option('select[data-pm=usu][data-i="2"][data-k=r]','vendedor_central'); await pg.select_option('select[data-pm=usu][data-i="2"][data-k=p]','Central')
        await pg.click('button[data-a=aru]'); await pg.wait_for_timeout(200)
        await pg.fill('input[data-pm=usu][data-i="3"][data-k=e]','admin2@test.com'); await pg.fill('input[data-pm=usu][data-i="3"][data-k=n]','Admin Dos')
        await pg.select_option('select[data-pm=usu][data-i="3"][data-k=r]','administracion')
        chk('administración no pide punto (selector oculto)',not await pg.is_visible('#arp_3'))
        await pg.click('button[data-a=aru]'); await pg.wait_for_timeout(200)
        await pg.fill('input[data-pm=usu][data-i="4"][data-k=e]','dup@test.com'); await pg.fill('input[data-pm=usu][data-i="4"][data-k=n]','Ya Existe')
        await pg.select_option('select[data-pm=usu][data-i="4"][data-k=r]','administrador')
        w0=await pg.evaluate("window.__WRITES.length")
        await pg.click('button[data-a=arx]'); await pg.wait_for_timeout(1500)
        chk('muestra pantalla de resultado',await pg.is_visible('text=Listo'))
        ubis=await pg.evaluate("[...window.__DB.entries()].filter(([k])=>k.startsWith('tenants/t1/ubicaciones/')).map(([k,v])=>v.nombre+'|'+v.tipo)")
        chk('creó los 2 puntos nuevos y dejó el central',sorted(ubis)==sorted(['Central|central','Camioneta 1|camioneta','Revendedores Norte|revendedores']),ubis)
        us=await pg.evaluate("[...window.__DB.entries()].filter(([k,v])=>k.startsWith('usuarios/uid_')).map(([k,v])=>({e:v.email,r:v.rol,u:v.ubicacionId,a:v.activo,t:v.tenantId}))")
        em={x['e']:x for x in us}
        chk('creó 4 usuarios (el que ya existía quedó afuera)',len(us)==4 and 'dup@test.com' not in em,us)
        chk('mails en minúscula, activos y con su distribuidora',all(x['a'] is True and x['t']=='t1' for x in us) and 'chofer@test.com' in em)
        chk('el chofer quedó en Camioneta 1 (tipo camioneta)',em['chofer@test.com']['r']=='vendedor_camioneta' and em['chofer@test.com']['u'] and True)
        idc=await pg.evaluate("[...window.__DB.entries()].find(([k,v])=>v.nombre==='Camioneta 1')[0].split('/').pop()")
        chk('ubicacionId del chofer = id real de Camioneta 1',em['chofer@test.com']['u']==idc)
        chk('administración sin punto (null)',em['admin2@test.com']['u'] is None)
        claves=await pg.evaluate("window.__CREADOS.map(x=>x[1])")
        chk('cada usuario tiene su clave propia de 8',len(set(claves))==4 and all(len(c)==8 for c in claves),claves)
        chk('el resultado muestra el que no se pudo crear con el motivo',await pg.evaluate("document.body.textContent.includes('Ese mail ya está registrado')"))
        chk('el resultado muestra las claves',all([await pg.evaluate("c=>document.body.textContent.includes(c)",c) for c in claves]))
        chk('no tocó usuarios existentes',await pg.evaluate("window.__DB.get('usuarios/ad1').nombre")=='Dueño')
        borr=await pg.evaluate("window.__WRITES.filter(w=>w[0]==='delete').length")
        chk('no borró nada',borr==0)
        chk('dejó registro en auditoría',await pg.evaluate("[...window.__DB.values()].some(v=>v.accion==='puesta_en_marcha')"))
        # copiar
        await pg.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{window.__COPIA=t}},configurable:true})"); await pg.click('button[data-a=arc]'); await pg.wait_for_timeout(300)
        cop=await pg.evaluate("window.__COPIA||''")
        chk('copiar arma el texto con portal, mails y claves',all(x in cop for x in ['Chofer Uno','chofer@test.com',claves[0]]) and 'Venta mostrador' in cop,cop[:120])
        # validaciones
        await pg.click('button[data-a=arn]'); await pg.wait_for_timeout(200)
        await pg.fill('input[data-pm=usu][data-i="0"][data-k=e]','sinarroba'); await pg.fill('input[data-pm=usu][data-i="0"][data-k=n]','X')
        n0=await pg.evaluate("window.__CREADOS.length"); await pg.click('button[data-a=arx]'); await pg.wait_for_timeout(300)
        chk('mail inválido: no crea nada',await pg.evaluate("window.__CREADOS.length")==n0)
        await pg.fill('input[data-pm=usu][data-i="0"][data-k=e]','ok@test.com')
        await pg.click('button[data-a=arx]'); await pg.wait_for_timeout(300)
        chk('vendedor sin punto: no crea nada',await pg.evaluate("window.__CREADOS.length")==n0)
        await pg.fill('input[data-pm=pun][data-i="0"][data-k=n]','central')
        await pg.select_option('select[data-pm=pun][data-i="0"][data-k=t]','central'); await pg.fill('input[data-pm=usu][data-i="0"][data-k=n]','');
        await pg.click('button[data-a=arx]'); await pg.wait_for_timeout(300)
        chk('segundo punto central o nombre repetido: no crea',await pg.evaluate("window.__CREADOS.length")==n0 and await pg.evaluate("[...window.__DB.keys()].filter(k=>k.startsWith('tenants/t1/ubicaciones/')).length")==3)
        chk('sin errores JS',not e,e)
        await ctx.close(); await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
