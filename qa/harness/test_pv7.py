import asyncio,sys,time
sys.path.insert(0,'/home/claude/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
OK=[];BAD=[]
def chk(n,c):
    (OK if c else BAD).append(n); print(('✓ ' if c else '✗ ')+n)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await (await br.new_context(viewport={'width':390,'height':844})).new_page(); errs=[]; dlg=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('dialog',lambda d:(dlg.append(d.message[:50]),asyncio.ensure_future(d.accept())))
        await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8777/index.html'); await pg.wait_for_timeout(800)
        now=int(time.time()*1000)
        await pg.evaluate("""now=>{const D=window.__DB;
          D.set('usuarios/adm',{email:'rgaraventa@gmail.com',rol:'owner',status:'activo',rubroPreguntado:true});D.set('negocios/nadm',{nombre:'Adm',ownerUid:'adm',tipo:'Kiosco',icon:'🏪'});
          D.set('usuarios/libre',{email:'libre@t.com',rol:'owner',status:'demo',demoStart:{__ts:now}});D.set('negocios/nl',{nombre:'Vacío',ownerUid:'libre',tipo:'Kiosco',icon:'🏪'});
          D.set('usuarios/emp1',{email:'emp@t.com',rol:'employee',ownerUid:'libre',negocioId:'nl',estado:'aprobado'});
          D.set('usuarios/usado',{email:'usado@t.com',rol:'owner',status:'activo'});D.set('negocios/nu',{nombre:'Con datos',ownerUid:'usado',tipo:'Kiosco',icon:'🏪'});
          D.set('ventas/v1',{ownerUid:'usado',negocioId:'nu',importe:100,medio:'efectivo',fecha:'2026-11-01',createdAt:{__ts:now}});}""",now)
        await pg.evaluate("()=>window.__login({uid:'adm',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>{localStorage.setItem('rt_admin','1');document.getElementById('modal-rubro')?.remove()}")
        for i in range(5): await pg.evaluate("()=>document.getElementById('owner-page-title').click()")
        await pg.wait_for_timeout(500); await pg.click('#atab-users'); await pg.wait_for_timeout(800)
        chk('tu cuenta de administrador no tiene botón Eliminar',await pg.evaluate("()=>![...document.querySelectorAll('.btn-adelu')].some(b=>b.dataset.email==='rgaraventa@gmail.com')"))
        chk('las demás cuentas sí',await pg.evaluate("()=>document.querySelectorAll('.btn-adelu').length")==3)
        await pg.evaluate("()=>document.querySelector('.btn-adelu[data-uid=usado]').click()"); await pg.wait_for_timeout(800)
        chk('cuenta con ventas: avisa y NO se borra',await pg.evaluate("()=>!!window.__DB.get('usuarios/usado')&&!!window.__DB.get('negocios/nu')") and any('datos cargados' in d for d in dlg))
        await pg.evaluate("()=>document.querySelector('.btn-adelu[data-uid=libre]').click()"); await pg.wait_for_timeout(1000)
        r=await pg.evaluate("()=>[!!window.__DB.get('usuarios/libre'),!!window.__DB.get('negocios/nl'),!!window.__DB.get('usuarios/emp1'),!!window.__DB.get('usuarios/usado'),!!window.__DB.get('usuarios/adm')]")
        chk('cuenta sin uso: se borra con su negocio vacío y su empleado',r==[False,False,False,True,True])
        chk('la lista se actualiza',await pg.evaluate("()=>!document.getElementById('admin-users-list').innerText.includes('libre@t.com')"))
        chk('sin errores JS',not errs)
        if errs: print(errs)
        await br.close()
    print('OK',len(OK),'FALLAS',BAD)
asyncio.run(main())
