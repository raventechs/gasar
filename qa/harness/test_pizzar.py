import asyncio
from playwright.async_api import async_playwright
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
BASE='http://127.0.0.1:8768/index.html'
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)
async def caso(br,demo):
    ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    async def gs(r):
        if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
        else: await r.fulfill(body='',content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
    await pg.goto(BASE); await pg.wait_for_timeout(1500)
    await pg.evaluate("""(d)=>{const T=firebase.firestore.Timestamp;const u={email:'p@t.com'};
      if(d==='null')u.demoHasta=null; else if(d!==None_)u.demoHasta=T.fromMillis(Date.now()+d*86400000);
      window.__DB.set('usuarios/u1',u);}""".replace('None_','undefined') if demo!='absent' else "()=>{window.__DB.set('usuarios/u1',{email:'p@t.com'})}",demo if demo!='absent' else None)
    await pg.evaluate("()=>window.__login({uid:'u1',email:'p@t.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
    return ctx,pg,errs
TXT="()=>{const b=document.querySelector('#rtChecklist .rt-chk');return b?b.textContent:''}"
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        ctx,pg,e=await caso(br,6); t=await pg.evaluate(TXT)
        chk('prueba en curso → tarjeta 0 de 4','0 de 4' in t,t[:60])
        await pg.click('.tab-btn[data-view="reportes"]'); await pg.wait_for_timeout(300)
        t=await pg.evaluate(TXT); chk('abrir Reportes tilda paso 3','1 de 4' in t,t[:40])
        await pg.evaluate("()=>{rtChkMarcar('prod');rtChkMarcar('venta')}"); t=await pg.evaluate(TXT); chk('3 de 4','3 de 4' in t)
        await pg.reload(); await pg.wait_for_timeout(500)
        await pg.evaluate("()=>window.__login({uid:'u1',email:'p@t.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        t=await pg.evaluate(TXT); chk('persiste tras recargar','3 de 4' in t,t[:40])
        await pg.evaluate("()=>rtChkMarcar('cierre')"); t=await pg.evaluate(TXT); chk('completo → tarjeta desaparece',t=='')
        chk('sin errores JS',not e,e); await ctx.close()
        ctx,pg,e=await caso(br,6); await pg.click('#rtChecklist .tt button'); chk('Ocultar la saca',await pg.evaluate(TXT)==''); await ctx.close()
        ctx,pg,e=await caso(br,'null'); chk('cliente real (demoHasta null) → sin tarjeta',await pg.evaluate(TXT)=='' ); await ctx.close()
        ctx,pg,e=await caso(br,-2); chk('prueba vencida → sin tarjeta (cartel rojo)',await pg.evaluate(TXT)==''); await ctx.close()
        ctx,pg,e=await caso(br,'absent'); t=await pg.evaluate(TXT); chk('cuenta anterior sin campo → arranca prueba y muestra tarjeta','0 de 4' in t,t[:40]); await ctx.close()
        await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
