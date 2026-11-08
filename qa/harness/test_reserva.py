import asyncio
from playwright.async_api import async_playwright
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        async def gs(r):
            if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
            else: await r.fulfill(body='',content_type='application/javascript')
        await pg.route('**/www.gstatic.com/**',gs)
        await pg.add_init_script("window.__DB=new Map();window.__DB.set('negocios/U1',{nombre:'Barbería Test',horaApertura:'09:00',horaCierre:'18:00',duracionTurno:30});window.__DB.set('negocios/U1/barberos/b1',{nombre:'Juan',activo:true});window.__DB.set('negocios/U1/productos/p1',{nombre:'Corte',precio:5000});")
        await pg.goto('http://127.0.0.1:8773/reservar-barbear/?neg=U1'); await pg.wait_for_timeout(1500)
        print('pasos visibles:',await pg.evaluate("getComputedStyle(document.getElementById('pasos')).display"),'| error:',await pg.evaluate("document.getElementById('errorBox').textContent"))
        print('barberos:',await pg.evaluate("document.body.innerText.includes('Juan')"),'servicios:',await pg.evaluate("document.body.innerText.includes('Corte')"))
        await pg.goto('http://127.0.0.1:8773/reservar-barbear/'); await pg.wait_for_timeout(600)
        print('sin código:',await pg.evaluate("document.getElementById('errorBox').textContent"))
        print('errs',errs); await br.close()
asyncio.run(main())
