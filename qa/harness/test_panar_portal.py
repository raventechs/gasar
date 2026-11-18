import asyncio, subprocess, time
from playwright.async_api import async_playwright
FAKE=open('/home/claude/raventechs/gasar/qa/harness/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
BASE='http://127.0.0.1:8784/index.html'
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)
async def nuevo(br,modo=None,negocio=True,comandas=True):
    ctx=await br.new_context(viewport={'width':390,'height':844},service_workers='block'); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    async def gs(r):
        if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
        else: await r.fulfill(body='',content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort())
    await pg.goto(BASE); await pg.wait_for_timeout(1200)
    await pg.evaluate("""(a)=>{
      if(a.neg) localStorage.setItem('rt_negocio','NEGOCIOABCDEFGHIJ1');
      window.__DB.set('negocios/NEGOCIOABCDEFGHIJ1/configuracion/general',{nombre:'Pizzeria',features:{comandasHabilitado:a.com}});
      firebase.auth().signInAnonymously=()=>window.__login({uid:'cajx',isAnonymous:true});
    }""",{'neg':negocio,'com':comandas})
    return ctx,pg,errs
async def vis(pg,sel): return await pg.evaluate("(s)=>{const e=document.querySelector(s);return !!e&&e.offsetParent!==null}",sel)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        ctx,pg,e=await nuevo(br)
        chk('al abrir: muestra los 2 botones',await vis(pg,'#bienDueno') and await vis(pg,'#bienCaja') and not await vis(pg,'#bienCocina'))
        chk('no muestra mail y clave todavía',not await vis(pg,'#loginEmail'))
        await pg.click('#bienDueno')
        chk('Dueño: aparece mail, clave y Google',await vis(pg,'#loginEmail') and await vis(pg,'#loginGoogleBtn'))
        await pg.click('#bienVolver')
        chk('Volver regresa a los botones',await vis(pg,'#bienCaja') and not await vis(pg,'#loginEmail'))
        await ctx.close()
        # sin link del dueño
        ctx,pg,e=await nuevo(br,negocio=False)
        await pg.click('#bienCaja')
        t=await pg.inner_text('#bienError'); chk('Caja sin link del dueño: explica qué hacer','link' in t.lower(),t[:60])
        await ctx.close()
        # Caja con PIN
        ctx,pg,e=await nuevo(br)
        await pg.click('#bienCaja'); chk('Caja: pide el PIN',await vis(pg,'#pinCajeroInput'))
        await pg.fill('#pinCajeroInput','123456'); await pg.click('#pinCajeroConfirmBtn'); await pg.wait_for_timeout(2500)
        chk('Caja: entra a la app',await vis(pg,'#app') or await pg.evaluate("document.getElementById('app').classList.contains('active')"))
        chk('Caja: muestra la vista Caja',await pg.evaluate("document.getElementById('view-caja').classList.contains('active')"))
        chk('Caja: no ve Reportes ni Configuración',not await vis(pg,'.tab-btn[data-view="reportes"]') and not await vis(pg,'.tab-btn[data-view="configuracion"]'))
        await ctx.close()
        ctx,pg,e=await nuevo(br)
        await pg.click('#bienCaja'); await pg.fill('#pinCajeroInput','123456'); await pg.click('#pinCajeroConfirmBtn'); await pg.wait_for_timeout(2000)
        await pg.click('#logoutBtn'); await pg.wait_for_timeout(600)
        chk('Salir: vuelve a la bienvenida',await vis(pg,'#bienCaja'))
        chk('sin errores JS',not e,e); await ctx.close()
        await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
