import asyncio,sys
sys.path.insert(0,'/home/claude/tw')
from fake_modular import install
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)+' | '+str(getattr(e,'stack',''))[:300])); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
        await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8775/index.html'); await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{localStorage.setItem('rt_admin','1');window.__DB.set('usuarios/adm',{email:'rgaraventa@gmail.com',status:'activo',nombre:'Adm'});window.__DB.set('usuarios/c1',{email:'cli@t.com',nombre:'Cli',status:'demo',demoStart:{__ts:Date.now()},demoExpiry:{__ts:Date.now()+86400000},features:{limiteIntegrantes:1}})}")
        await pg.evaluate("()=>window.__login({uid:'adm',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        for i in range(5): await pg.evaluate("()=>{const e=document.getElementById('app-logo');e.click()}")
        await pg.wait_for_timeout(700)
        print('admin screen:',await pg.evaluate("()=>document.getElementById('screen-admin').classList.contains('active')"),'| .btn-anotif:',await pg.evaluate("()=>document.querySelectorAll('.btn-anotif').length"))
        async def feat(): return await pg.evaluate("()=>JSON.stringify(window.__DB.get('usuarios/c1').features)")
        clk=lambda c:"()=>{[...document.querySelectorAll('%s')].find(b=>b.dataset.uid==='c1').click()}"%c
        await pg.evaluate(clk('.btn-anotif')); await pg.wait_for_timeout(700); print('recordatorios ON :',await feat())
        await pg.evaluate(clk('.btn-anotif')); await pg.wait_for_timeout(700); print('recordatorios OFF:',await feat())
        await pg.evaluate("()=>{[...document.querySelectorAll('.btn-alim')].find(b=>b.dataset.uid==='c1'&&b.dataset.val==='3').click()}"); await pg.wait_for_timeout(700); print('limite integrantes 3:',await feat())
        print('errs',errs[:3]); await br.close()
asyncio.run(main())
