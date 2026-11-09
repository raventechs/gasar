import asyncio,sys,time
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
sys.path.insert(0,'/home/claude/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
OK=[];BAD=[]
def chk(n,c):
    (OK if c else BAD).append(n); print(('✓ ' if c else '✗ ')+n)
def f(dias): return (datetime.now(ZoneInfo('America/Argentina/Buenos_Aires'))-timedelta(days=dias)).strftime('%Y-%m-%d')
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await (await br.new_context(viewport={'width':390,'height':844})).new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
        await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8777/index.html'); await pg.wait_for_timeout(900)
        now=int(time.time()*1000)
        seed=[]
        def v(i,neg,dias,imp,medio,desc,extra=''):
            seed.append(f"D.set('ventas/v{i}',{{ownerUid:'a1',negocioId:'{neg}',importe:{imp},medio:'{medio}',pagos:[{{medio:'{medio}',importe:{imp}}}],descripcion:'{desc}',fecha:'{f(dias)}',hora:'10:00',createdAt:{{__ts:now-{dias}*86400000-{i}*1000}}{extra}}});")
        v(1,'n1',0,5000,'efectivo','Pan');v(2,'n1',0,3000,'mp','Leche');v(3,'n2',0,2000,'debito','Remera')
        v(4,'n1',1,4000,'efectivo','Ayer1');v(5,'n2',1,3000,'efectivo','Ayer2')
        v(6,'n1',3,9000,'transferencia','Hace3');v(7,'n2',8,1000,'efectivo','Vieja')
        v(8,'n2',0,1500,'fiado','Fiado Marta')
        await pg.evaluate("""now=>{const D=window.__DB;
          D.set('usuarios/a1',{uid:'a1',email:'a@g.com',rol:'owner',modo:'multi',plan:'avanzada',status:'demo',banned:false,demoHasta:{__ts:now+14*86400000},rubroPreguntado:true});
          D.set('negocios/n1',{nombre:'Kiosco Centro',ownerUid:'a1',tipo:'Kiosco',icon:'🍬'});
          D.set('negocios/n2',{nombre:'Verdulería Norte',ownerUid:'a1',tipo:'Verdulería',icon:'🥬'});
          D.set('gastos/g1',{ownerUid:'a1',negocioId:'n1',importe:800,fecha:'"""+f(0)+"""',descripcion:'Luz',createdAt:{__ts:now}});
          D.set('clientes/c1',{ownerUid:'a1',tipo:'cc',nombre:'Marta Gómez',saldo:1500,createdAt:{__ts:now}});
          """+"".join(seed)+"}",now)
        await pg.evaluate("()=>window.__login({uid:'a1',email:'a@g.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>{document.getElementById('modal-rubro')?.remove();document.querySelector('[data-page=dashboard]').click()}"); await pg.wait_for_timeout(1500)
        auto=await pg.evaluate("()=>document.getElementById('dash-auto').innerText")
        print(auto)
        chk('tarjeta Lo importante de hoy',('Lo importante de hoy' in auto))
        chk('compara con ayer (hoy 10000 vs ayer 7000 = 43% más)',('43% más' in auto))
        chk('nombra la sucursal que más vendió',('Kiosco Centro' in auto and 'más vendió' in auto))
        chk('avisa deuda en cuenta',('Marta Gómez' in auto and '1.500' in auto))
        chk('barras 7 días con 7 columnas',await pg.evaluate("()=>document.querySelectorAll('#dash-graf svg rect').length")==7)
        chk('torta de medios',await pg.evaluate("()=>document.querySelectorAll('#dash-graf circle').length")>=3)
        comp=await pg.evaluate("()=>document.getElementById('dash-graf').innerText")
        chk('comparativa con las dos sucursales',('Kiosco Centro' in comp and 'Verdulería Norte' in comp))
        chk('tarjetas por sucursal',await pg.evaluate("()=>document.querySelectorAll('.d-neg-card').length")==2)
        await pg.screenshot(path='/tmp/dash.png',full_page=True)
        await pg.evaluate("()=>document.querySelector('.d-neg-card[data-id=n1]').click()"); await pg.wait_for_timeout(800)
        await pg.screenshot(path='/tmp/ficha.png')
        ficha=await pg.evaluate("()=>document.querySelector('#modal-ficha-neg .modal').innerText")
        chk('ficha abre con nombre y rubro',('Kiosco Centro' in ficha and 'Kiosco' in ficha))
        chk('ficha: hoy $8.000 y gastos mes $800',('$8.000' in ficha and '$800' in ficha))
        await pg.fill('#ficha-buscar','hace3'); await pg.wait_for_timeout(300)
        r=await pg.evaluate("()=>document.getElementById('ficha-ventas').innerText")
        chk('buscador de la ficha encuentra venta vieja y no mezcla sucursales',('Hace3' in r and 'Remera' not in r))
        await pg.fill('#ficha-buscar','remera'); await pg.wait_for_timeout(300)
        chk('no aparece venta de otra sucursal',('Sin resultados' in await pg.evaluate("()=>document.getElementById('ficha-ventas').innerText")))
        await pg.click('#ficha-cerrar'); await pg.wait_for_timeout(200)
        chk('cierra la ficha',await pg.evaluate("()=>!document.getElementById('modal-ficha-neg').classList.contains('open')"))
        chk('sin errores JS',not errs)
        if errs: print(errs)
        await br.close()
    print('OK',len(OK),'FALLAS',BAD)
asyncio.run(main())
