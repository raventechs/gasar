import asyncio
from playwright.async_api import async_playwright
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1)
BASE='http://127.0.0.1:8766/manejar.html'
DAY=86400000
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)
FAKE=FAKE.replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
async def caso(br,estado,vence_dias,email='cliente@test.com'):
    ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    async def gs(r):
        if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
        else: await r.fulfill(body='',content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw-manejar.js',lambda r:r.abort())
    await pg.goto(BASE); await pg.wait_for_timeout(800)
    import time
    await pg.evaluate("([e,d])=>{const ms=Date.now()+d*86400000;window.__DB.set('usuarios/u1',{email:'cliente@test.com',estado:e,vence:ms,creado:Date.now()})}",[estado,vence_dias])
    await pg.evaluate("([m])=>window.__login({uid:'u1',email:m,emailVerified:true})",[email]); await pg.wait_for_timeout(1800)
    d=await pg.evaluate("""()=>{const b=document.getElementById('barvenc');const r=b?b.getBoundingClientRect():null;
      return {bar:!!b,txt:b?b.textContent:'',pos:b?getComputedStyle(b).position:'',anim:b?getComputedStyle(b).animationName:'',cerrar:b?!!b.querySelector('[aria-label*=errar],.x,.cerrar'):false,
      bloq:/pausada|Terminó tu prueba gratis|venció/.test(document.querySelector('#view').textContent)&&!!document.querySelector('.auth'),
      nav:document.querySelectorAll('#nav button').length,inview:r?(r.bottom<=innerHeight&&r.top>0):false,banner:!!document.querySelector('.banner.red')}}""")
    await ctx.close(); return d,errs
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        d,e=await caso(br,'demo',-3); chk('demo vencida: entra a la app (no bloquea)',d['nav']>=3 and not d['bloq'],d)
        chk('demo vencida: cartel fijo, titilante, visible',d['bar'] and d['pos']=='fixed' and d['anim']!='none' and d['inview'])
        chk('demo vencida: sin botón de cerrar y dice prueba terminada','Terminó tu prueba' in d['txt'] and not d['cerrar'])
        chk('sin errores de JS',not e,e)
        d,e=await caso(br,'activo',-1); chk('plan vencido: cartel y app funcionando',d['bar'] and 'plan venció' in d['txt'] and d['nav']>=3)
        d,e=await caso(br,'demo',5); chk('demo en curso: sin cartel fijo, con aviso de días',not d['bar'] and d['banner'] and d['nav']>=3)
        d,e=await caso(br,'activo',20); chk('activo vigente: sin cartel',not d['bar'] and d['nav']>=3)
        d,e=await caso(br,'bloqueado',20); chk('bloqueado manual: sigue bloqueado y sin cartel',d['nav']==0 and not d['bar'])
        d,e=await caso(br,'demo',-3,'rgaraventa@gmail.com'); chk('admin: sin cartel',not d['bar'])
        await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
