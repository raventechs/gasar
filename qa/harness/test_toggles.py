import asyncio,sys,json
from playwright.async_api import async_playwright
APP,PORT=sys.argv[1],sys.argv[2]
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        async def gs(r):
            if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
            else: await r.fulfill(body='',content_type='application/javascript')
        await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>{localStorage.setItem('rt_admin','1');window.__DB.set('usuarios/u1',{email:'rgaraventa@gmail.com',demoHasta:null})}")
        await pg.evaluate("()=>window.__login({uid:'u1',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        for i in range(5): await pg.click('#logoBtn'); await pg.wait_for_timeout(80)
        await pg.wait_for_timeout(600)
        ids=await pg.evaluate("()=>{const m=document.getElementById('modalFeatures');return {open:m.classList.contains('active'),flags:[...m.querySelectorAll('input[type=checkbox]')].map(i=>i.id)}}")
        print('modal abierto:',ids['open'],'| toggles:',ids['flags'])
        fallas=[]
        for fid in ids['flags']:
            # activar
            await pg.evaluate("(f)=>{document.getElementById('modalFeatures').classList.add('active');const e=document.getElementById(f);e.checked=true;}",fid)
            await pg.click('#modalFeaturesGuardar'); await pg.wait_for_timeout(500)
            on=await pg.evaluate("()=>{for(const [k,v] of window.__DB){if(k.endsWith('configuracion/general'))return v.features||null}return null}")
            await pg.evaluate("(f)=>{document.getElementById('modalFeatures').classList.add('active');document.getElementById(f).checked=false;}",fid)
            await pg.click('#modalFeaturesGuardar'); await pg.wait_for_timeout(500)
            off=await pg.evaluate("()=>{for(const [k,v] of window.__DB){if(k.endsWith('configuracion/general'))return v.features||null}return null}")
            nTrue=sum(1 for v in (on or {}).values() if v is True); nOff=sum(1 for v in (off or {}).values() if v is True)
            ok=nTrue>=1 and nOff==0
            print(('OK    ' if ok else 'FALLA ')+fid,'activa→',nTrue,'true | desactiva→',nOff,'true')
            if not ok: fallas.append(fid)
        print('FALLAS:',fallas,'| errores JS:',errs)
        await br.close()
asyncio.run(main())
