import asyncio
from playwright.async_api import async_playwright
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        async def gs(r):
            if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
            else: await r.fulfill(body='',content_type='application/javascript')
        await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8770/index.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>window.__login({uid:'u1',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>{document.getElementById('appShell').style.display=''}")
        print('abrir menú admin:',await pg.evaluate("()=>{try{abrirAdminLavar();return document.getElementById('adminModal').classList.contains('open')||document.getElementById('adminModal').classList.contains('active')||getComputedStyle(document.getElementById('adminModal')).display}catch(e){return 'ERR '+e.message}}"))
        # ¿tiene PIN? flujo de apertura
        print('entrada al menú:',await pg.evaluate("()=>{const s=[...document.querySelectorAll('[onclick]')].map(e=>e.getAttribute('onclick')).filter(x=>/admin|pin/i.test(x));return s.slice(0,6)}"))
        for fid,key in [('flagFidelizacion','fidelizacion'),('flagGastos','gastos'),('flagPersonal','personal')]:
            for val in (True,False):
                await pg.evaluate("([f,v])=>{document.getElementById(f).checked=v}",[fid,val]); await pg.evaluate("()=>guardarAdmin()"); await pg.wait_for_timeout(400)
                got=await pg.evaluate("()=>{for(const [k,v] of window.__DB){if(k.startsWith('config/'))return v.features}}")
                tab=await pg.evaluate("(k)=>{const e=document.querySelector('[data-tab=\"'+k+'\"]');return e?!e.classList.contains('section-hidden'):null}",key)
                ok=got and got.get(key)==val and tab==val
                print(('OK    ' if ok else 'FALLA ')+key,'→',val,'| guardado',got.get(key) if got else None,'| pestaña visible',tab)
        for n in (3,99,1):
            await pg.evaluate("()=>abrirAdminLavar()"); await pg.click(f'[data-suc="{n}"]'); await pg.evaluate("()=>guardarAdmin()"); await pg.wait_for_timeout(400)
            v=await pg.evaluate("()=>{for(const [k,v] of window.__DB){if(k.startsWith('config/'))return v.limiteSucursales}}")
            print(('OK    ' if v==n else 'FALLA ')+'sucursales botón',n,'→',v)
        print('errores JS:',errs); await br.close()
asyncio.run(main())
