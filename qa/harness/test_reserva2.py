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
        await pg.add_init_script("window.__DB=new Map();window.__DB.set('negocios/U1',{nombre:'Barbería Test',horaApertura:'09:00',horaCierre:'18:00',duracionTurno:30});window.__DB.set('negocios/U1/barberos/b1',{nombre:'Juan',activo:true});window.__DB.set('negocios/U1/productos/p1',{nombre:'Corte clásico',categoria:'Peluquería',tamanos:[{nombre:'Servicio',precio:14000}]});window.__DB.set('negocios/U1/productos/p2',{nombre:'Gel fijador',categoria:'Insumos',tamanos:[{nombre:'Unidad',precio:5000}]});")
        await pg.goto('http://127.0.0.1:8773/reservar-barbear/?neg=U1'); await pg.wait_for_timeout(1500)
        print('pasos visibles:',await pg.evaluate("getComputedStyle(document.getElementById('pasos')).display"),'| error:',await pg.evaluate("document.getElementById('errorBox').textContent"))
        await pg.click("text=Juan"); await pg.wait_for_timeout(300)
        print('gel oculto:',not await pg.evaluate("document.body.innerText.includes('Gel fijador')"))
        await pg.click("text=Corte clásico"); await pg.wait_for_timeout(400)
        print('paso fecha activo:',await pg.evaluate("document.getElementById('step-fecha').classList.contains('active')"))
        await pg.evaluate("()=>{const i=document.getElementById('inputFecha');const d=new Date();d.setDate(d.getDate()+((1-d.getDay()+7)%7||7));i.value=d.toISOString().slice(0,10);i.dispatchEvent(new Event('change'))}"); await pg.wait_for_timeout(800)
        await pg.click('.slot-btn >> nth=1'); await pg.wait_for_timeout(1500)
        print('paso datos activo y se queda:',await pg.evaluate("document.getElementById('step-datos').classList.contains('active')"))
        await pg.fill('#inputNombre','Ana Test'); await pg.click('text=Confirmar turno'); await pg.wait_for_timeout(1200)
        print('confirmado:',await pg.evaluate("document.getElementById('step-confirmado').classList.contains('active')"),[k for k in await pg.evaluate("()=>[...window.__DB.keys()]") if 'turnos' in k or 'ocupados' in k])
        await pg.goto('http://127.0.0.1:8773/reservar-barbear/'); await pg.wait_for_timeout(600)
        print('sin código:',await pg.evaluate("document.getElementById('errorBox').textContent"))
        print('errs',errs); await br.close()
asyncio.run(main())
