import asyncio,sys,time
sys.path.insert(0,'/home/claude/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
OK=[];BAD=[]
def chk(n,c):
    (OK if c else BAD).append(n); print(('✓ ' if c else '✗ ')+n)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await (await br.new_context(viewport={'width':390,'height':844})).new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
        await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8777/index.html'); await pg.wait_for_timeout(900)
        now=int(time.time()*1000)
        await pg.evaluate("""now=>{const D=window.__DB;
          D.set('usuarios/b1',{uid:'b1',email:'b@g.com',rol:'owner',modo:'single',plan:'basico',status:'demo',banned:false,demoHasta:{__ts:now+14*86400000}});
          D.set('negocios/nb',{nombre:'Lo de Ana',ownerUid:'b1',tipo:'Negocio único',icon:'🏪'});}""",now)
        await pg.evaluate("()=>window.__login({uid:'b1',email:'b@g.com',emailVerified:True})".replace('True','true')); await pg.wait_for_timeout(2500)
        chk('pregunta el rubro al empezar',await pg.evaluate("()=>!!document.getElementById('modal-rubro')"))
        tt=await pg.evaluate("()=>document.getElementById('owner-page-title').innerText")
        chk('barra: Lo de Ana grande + PuntoVenta chico',('Lo de Ana' in tt and 'PuntoVenta' in tt))
        await pg.evaluate("()=>document.querySelector('[data-rubro=\"Tienda de ropa\"]').click()"); await pg.wait_for_timeout(800)
        nb=await pg.evaluate("()=>window.__DB.get('negocios/nb')")
        chk('guarda rubro e ícono',nb['tipo']=='Tienda de ropa' and nb['icon']=='👕')
        chk('el cartel se cierra',await pg.evaluate("()=>!document.getElementById('modal-rubro')"))
        tt=await pg.evaluate("()=>document.getElementById('owner-page-title').innerText")
        chk('barra con ícono del rubro',('👕' in tt and 'Lo de Ana' in tt))
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=vender]').click()"); await pg.wait_for_timeout(500)
        chips=await pg.evaluate("()=>[...document.querySelectorAll('#depto-chips-vender [data-atajo]')].map(b=>b.textContent)")
        ph=await pg.evaluate("()=>document.getElementById('vd-desc').placeholder")
        chk('atajos de ropa en Vender',('Remera' in chips) and 'Remera' in ph)
        await pg.evaluate("()=>document.querySelector('[data-atajo=\"Jean\"]').click()")
        chk('tocar un atajo completa la descripción',await pg.evaluate("()=>document.getElementById('vd-desc').value")=='Jean')
        # Historial: búsqueda en todo el historial y un solo resumen aunque haya varios negocios
        await pg.evaluate("now=>{const D=window.__DB;D.set('negocios/nb2',{nombre:'Otro',ownerUid:'b1',tipo:'Otro',icon:'🏬'});D.set('negocios/nb3',{nombre:'Otro 3',ownerUid:'b1',tipo:'Otro',icon:'🏬'});D.set('ventas/hv1',{ownerUid:'b1',negocioId:'nb',importe:4500,medio:'efectivo',pagos:[{medio:'efectivo',importe:4500}],descripcion:'Campera',clienteNombre:'Marta Gómez',fecha:'2026-10-20',hora:'10:00',createdAt:{__ts:now-19*86400000}});D.set('ventas/hv2',{ownerUid:'b1',negocioId:'nb',importe:1200,medio:'mp',pagos:[{medio:'mp',importe:1200}],descripcion:'Remera',fecha:'2026-11-02',hora:'11:00',createdAt:{__ts:now-6*86400000}});}",now)
        await pg.evaluate("()=>window.__logout&&0")
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=ventas]').click()"); await pg.wait_for_timeout(600)
        chk('Historial: sin resumen duplicado por negocio',await pg.evaluate("()=>document.querySelectorAll('#page-ventas .cierre-card').length")==0)
        await pg.fill('#ventas-buscar','marta'); await pg.wait_for_timeout(1200)
        tt=await pg.evaluate("()=>document.getElementById('page-ventas').innerText")
        chk('búsqueda encuentra una venta de otro día por cliente','Campera' in tt and 'Remera' not in tt)
        await pg.fill('#ventas-buscar','remera'); await pg.wait_for_timeout(1200)
        chk('búsqueda por producto','Remera' in await pg.evaluate("()=>document.getElementById('page-ventas').innerText"))
        await pg.fill('#ventas-buscar','zzzz'); await pg.wait_for_timeout(1200)
        chk('búsqueda sin resultados avisa','No encontré' in await pg.evaluate("()=>document.getElementById('page-ventas').innerText"))
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=vender]').click()"); await pg.wait_for_timeout(600)
        chk('Caja: UN resumen con 3 negocios cargados',await pg.evaluate("()=>document.querySelectorAll('#page-vender .cierre-card').length")==1)
        chk('sin errores JS',errs==[])
        await br.close()
    print('OK',len(OK),'FALLAS',BAD)
asyncio.run(main())
