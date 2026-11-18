import asyncio, subprocess, time
from playwright.async_api import async_playwright
FAKE=open('/home/claude/raventechs/gasar/qa/harness/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
BASE='http://127.0.0.1:8783/index.html'
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

async def dueno(br,creacion):
    ctx,pg,e=await nuevo(br,negocio=False)
    await pg.evaluate("()=>{window.__wa=[];window.open=u=>{window.__wa.push(u);return null}}")
    await pg.evaluate("(c)=>window.__login({uid:'own1',email:'o@t.com',emailVerified:true,metadata:{creationTime:c}})",creacion)
    await pg.wait_for_timeout(2800)
    return ctx,pg,e
async def vis(pg,sel): return await pg.evaluate("(s)=>{const e=document.querySelector(s);return !!e&&e.offsetParent!==null}",sel)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        ctx,pg,e=await nuevo(br)
        chk('al abrir: muestra los 3 botones',await vis(pg,'#bienDueno') and await vis(pg,'#bienCaja') and await vis(pg,'#bienCocina'))
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
        # Cocina con comandas activas
        ctx,pg,e=await nuevo(br)
        await pg.click('#bienCocina'); await pg.fill('#pinCajeroInput','123456'); await pg.click('#pinCajeroConfirmBtn'); await pg.wait_for_timeout(3000)
        chk('Cocina: abre la vista de comandas',await pg.evaluate("document.getElementById('view-cocina').classList.contains('active')"))
        chk('Cocina: no muestra la vista Caja',not await pg.evaluate("document.getElementById('view-caja').classList.contains('active')"))
        chk('Cocina: solo la pestaña Cocina',await vis(pg,'.tab-btn[data-view="cocina"]') and not await vis(pg,'.tab-btn[data-view="caja"]') and not await vis(pg,'.tab-btn[data-view="menu"]'))
        await pg.click('#logoutBtn'); await pg.wait_for_timeout(600)
        chk('Salir: vuelve a la bienvenida',await vis(pg,'#bienCocina'))
        await ctx.close()
        # Cocina con comandas apagadas
        ctx,pg,e=await nuevo(br,comandas=False)
        await pg.click('#bienCocina'); await pg.fill('#pinCajeroInput','123456'); await pg.click('#pinCajeroConfirmBtn'); await pg.wait_for_timeout(3000)
        t=await pg.evaluate("(document.getElementById('rtAvisoCocina')||{}).textContent||''")
        chk('Cocina sin comandas activadas: avisa',('no están activadas' in t),t[:70])
        chk('Cocina sin comandas: no deja ver la caja',not await vis(pg,'.tab-btn[data-view="caja"]'))
        chk('sin errores JS',not e,e); await ctx.close()
        # ── versión de prueba mínima (cuentas nuevas) ──
        ctx,pg,e=await dueno(br,'Thu, 19 Nov 2026 10:00:00 GMT')
        chk('cuenta nueva: se marca versión mínima',await pg.evaluate("featuresActuales.planMinimo===true"))
        chk('cuenta nueva: ve la pestaña Adicionales',await vis(pg,'#rtTabAdic'))
        chk('cuenta nueva: no ve Historial',not await vis(pg,'.tab-btn[data-view="historial"]'))
        chk('cuenta nueva: Facturación en lugar de Reportes','Facturación' in await pg.inner_text('.tab-btn[data-view="reportes"]'))
        chk('cuenta nueva: gastos y importe libre visibles',await vis(pg,'#gastosSection') and await vis(pg,'#rtImporteLibre'))
        chk('cuenta nueva: no ve Stock, Empleados ni Cocina',not await vis(pg,'.tab-btn[data-view="stock"]') and not await vis(pg,'.tab-btn[data-view="empleados"]') and not await vis(pg,'.tab-btn[data-view="cocina"]'))
        await pg.fill('#rtImpLibreInput','2500'); await pg.click('#rtImpLibreBtn')
        t=await pg.inner_text('#carritoTotal'); chk('importe libre suma al total',t.replace('.','').replace(',','')=='$2500',t)
        await pg.click('#rtTabAdic'); await pg.wait_for_timeout(300)
        t=await pg.inner_text('#rtAdicionales'); chk('Adicionales: lista Comandas y Stock con botón de pedir','Comandas de cocina' in t and 'Stock e insumos' in t and 'Pedir este adicional' in t)
        chk('Adicionales: no dice «básica»','básic' not in t.lower())
        await pg.click('#rtAdicionales button >> nth=0'); await pg.wait_for_timeout(200)
        w=await pg.evaluate("window.__wa[0]||''"); chk('Pedir abre WhatsApp de Raven con el adicional',('wa.me/5491136547592' in w) and ('Comandas' in w or 'comandas' in w.lower() or '%C2%AB' in w),w[:90])
        cfg=await pg.evaluate("JSON.stringify(window.__DB.get('negocios/own1/configuracion/general')||{})"); chk('quedó guardado en la configuración del negocio','planMinimo' in cfg,cfg[:80])
        chk('sin errores JS',not e,e); await ctx.close()
        ctx,pg,e=await dueno(br,'Mon, 03 Mar 2025 10:00:00 GMT')
        chk('cuenta anterior: NO cambia (sin Adicionales, con Historial)',not await vis(pg,'#rtTabAdic') and await vis(pg,'.tab-btn[data-view="historial"]'))
        chk('cuenta anterior: sin importe libre ni versión mínima',not await vis(pg,'#rtImporteLibre') and not await pg.evaluate("featuresActuales.planMinimo"))
        chk('cuenta anterior: Reportes se llama igual',(await pg.inner_text('.tab-btn[data-view="reportes"]')).strip()=='Reportes')
        chk('sin errores JS',not e,e); await ctx.close()
        await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
