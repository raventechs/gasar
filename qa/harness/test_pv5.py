import asyncio,sys,time
from datetime import datetime
from zoneinfo import ZoneInfo
sys.path.insert(0,'/home/claude/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
OK=[];BAD=[]
def chk(n,c):
    (OK if c else BAD).append(n); print(('✓ ' if c else '✗ ')+n)
async def main():
    hoy=datetime.now(ZoneInfo('America/Argentina/Buenos_Aires')).strftime('%Y-%m-%d')
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await (await br.new_context(viewport={'width':390,'height':844})).new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
        await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8777/index.html'); await pg.wait_for_timeout(900)
        now=int(time.time()*1000)
        await pg.evaluate("""a=>{const D=window.__DB;const h=a[0],now=a[1];
          D.set('usuarios/o1',{uid:'o1',email:'o@g.com',rol:'owner',modo:'multi',plan:'avanzada',status:'activo',banned:false});
          D.set('negocios/n1',{nombre:'Kiosco Centro',ownerUid:'o1',tipo:'Kiosco',icon:'🍬'});
          D.set('usuarios/e1',{uid:'e1',email:'valen@g.com',rol:'employee',ownerUid:'o1',negocioId:'n1',estado:'aprobado',status:'activo',banned:false});
          D.set('ventas/a',{ownerUid:'o1',empleadoUid:'e1',negocioId:'n1',importe:3000,medio:'efectivo',descripcion:'x',fecha:h,hora:'10:00',createdAt:{__ts:now}});
          D.set('ventas/b',{ownerUid:'o1',empleadoUid:'e1',negocioId:'n1',importe:2000,medio:'mp',descripcion:'y',fecha:h,hora:'11:00',createdAt:{__ts:now-1000}});}""",[hoy,now])
        await pg.evaluate("()=>{window.__wa=[];window.open=u=>{window.__wa.push(u)}}")
        await pg.evaluate("()=>window.__login({uid:'e1',email:'valen@g.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        chk('pantalla del empleado',await pg.evaluate("()=>document.getElementById('screen-employee').classList.contains('active')"))
        await pg.evaluate("()=>{window.open=u=>{window.__wa.push(u)};document.getElementById('btn-emp-cierre').click()}"); await pg.wait_for_timeout(300)
        wa=await pg.evaluate("()=>window.__wa.map(decodeURIComponent)")
        print(wa)
        chk('abre WhatsApp con el cierre del empleado',len(wa)==1 and 'Kiosco Centro' in wa[0] and 'valen' in wa[0] and 'Total cobrado: $5.000' in wa[0] and 'Efectivo: $3.000' in wa[0])
        chk('sin errores JS',not errs)
        await br.close()
    print('OK',len(OK),'FALLAS',BAD)
asyncio.run(main())
