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
        chk('sin errores JS',errs==[])
        await br.close()
    print('OK',len(OK),'FALLAS',BAD)
asyncio.run(main())
