import asyncio,sys
sys.path.insert(0,'/home/claude/tw')
from fake_modular import install
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
        await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8776/index.html'); await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{localStorage.setItem('rt_admin','1');window.__DB.set('usuarios/adm',{email:'rgaraventa@gmail.com',status:'activo',nombre:'Adm'});window.__DB.set('usuarios/c1',{email:'cli@t.com',nombre:'Cli',status:'demo',demoStart:{__ts:Date.now()},demoExpiry:{__ts:Date.now()+86400000},features:{limitePerfiles:1}})}")
        await pg.evaluate("()=>window.__login({uid:'adm',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        for i in range(5): await pg.evaluate("()=>{(document.getElementById('app-logo')||document.getElementById('login-logo')).click()}")
        await pg.wait_for_timeout(700)
        print('admin screen:',await pg.evaluate("()=>document.getElementById('screen-admin').classList.contains('active')"))
        g=lambda:pg.evaluate("()=>JSON.stringify(window.__DB.get('usuarios/c1'))")
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-afam-on')].find(b=>b.dataset.uid==='c1').click()}"); await pg.wait_for_timeout(800); print('habilitar familiar:',(await g())[:260])
        print('window.setLimitePerfiles:',await pg.evaluate("()=>typeof window.setLimitePerfiles"))
        await pg.evaluate("()=>{const s=document.querySelector('select[onchange*=setLimitePerfiles]');s.value='5';s.dispatchEvent(new Event('change'))}"); await pg.wait_for_timeout(800); print('select 5 perfiles:',(await g())[:260])
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-acupo')].find(b=>b.dataset.uid==='c1'&&b.dataset.val==='10').click()}"); await pg.wait_for_timeout(800); print('cupo 10:',(await g())[200:330])
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-afam-off')].find(b=>b.dataset.uid==='c1').click()}"); await pg.wait_for_timeout(800); print('deshabilitar:',(await g())[:200])
        print('errs',errs[:4]); await br.close()
asyncio.run(main())
