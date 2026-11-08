import asyncio,sys
sys.path.insert(0,'/home/claude/tw')
from fake_modular import install
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
        await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8774/index.html'); await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{window.__DB.set('usuarios/adm',{email:'rgaraventa@gmail.com',rol:'owner',status:'activo'});window.__DB.set('usuarios/c1',{email:'cli@t.com',rol:'owner',status:'demo',demoStart:{__ts:Date.now()},demoExpiry:{__ts:Date.now()+86400000},features:{limiteNegocios:1}})}")
        await pg.evaluate("()=>window.__login({uid:'adm',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>localStorage.setItem('rt_admin','1')")
        ids=await pg.evaluate("()=>{const m=['logo-owner','logo-auth','logo-cashier','owner-logo'];return [...document.querySelectorAll('[id*=logo]')].map(e=>e.id)}"); print('logos',ids)
        for i in range(5): await pg.evaluate("()=>document.getElementById('owner-page-title').click()")
        await pg.wait_for_timeout(500)
        print('admin screen:',await pg.evaluate("()=>document.getElementById('screen-admin').classList.contains('active')"))
        await pg.click('#atab-users'); await pg.wait_for_timeout(700)
        print('botones moros/lim:',await pg.evaluate("()=>[document.querySelectorAll('.btn-amoros').length,document.querySelectorAll('.btn-alim').length]"))
        # activar plus morosidad
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-amoros')].find(b=>b.dataset.uid==='c1').click()}"); await pg.wait_for_timeout(600)
        print('moros on:',await pg.evaluate("()=>window.__DB.get('usuarios/c1').features"))
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-amoros')].find(b=>b.dataset.uid==='c1').click()}"); await pg.wait_for_timeout(600)
        print('moros off:',await pg.evaluate("()=>window.__DB.get('usuarios/c1').features"))
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-alim')].find(b=>b.dataset.uid==='c1'&&b.dataset.val==='3').click()}"); await pg.wait_for_timeout(600)
        print('limite 3:',await pg.evaluate("()=>window.__DB.get('usuarios/c1').features"))
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-aact')].find(b=>b.dataset.uid==='c1').click()}"); await pg.wait_for_timeout(600)
        print('activar:',await pg.evaluate("()=>window.__DB.get('usuarios/c1').status"))
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-aext')].find(b=>b.dataset.uid==='c1')&&0}")
        print('errs',errs[:3]); await br.close()
asyncio.run(main())
