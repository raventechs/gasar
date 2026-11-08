import asyncio
from playwright.async_api import async_playwright
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
BASE='http://127.0.0.1:8767/'
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)

async def caso(br,extra,tab):
    ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    async def gs(r):
        if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
        else: await r.fulfill(body='',content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw-*.js',lambda r:r.abort())
    await pg.goto(BASE+'gasar-admin.html'); await pg.wait_for_timeout(800)
    await pg.evaluate("""(x)=>{const T=firebase.firestore.Timestamp;const t=Object.assign({nombre:'Gas Test',plan:'activo'},x);
      for(const k of ['creadoTs','demoHasta']) if(typeof t[k]==='number') t[k]=T.fromMillis(t[k]);
      window.__DB.set('tenants/t1',t);window.__DB.set('usuarios/u1',{email:'d@t.com',nombre:'D',rol:'administrador',activo:true,tenantId:'t1'});
      window.__DB.set('tenants/t1/ubicaciones/ub1',{nombre:'Central',tipo:'central',activa:true});}""",extra)
    await pg.evaluate("()=>window.__login({uid:'u1',email:'d@t.com',emailVerified:true})"); await pg.wait_for_timeout(2000)
    await pg.evaluate("(k)=>{S.tab=k;render()}",tab); await pg.wait_for_timeout(500)
    t=await pg.evaluate("()=>document.querySelector('main')?document.querySelector('main').innerText:''")
    nav=await pg.evaluate("()=>document.querySelector('nav').innerText")
    await ctx.close(); return t,nav,errs
NEW=1800000000000; OLD=1700000000000; FUT=__import__('time').time()*1000+5*86400000
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        t,n,e=await caso(br,{'creadoTs':OLD},'revendedores'); chk('cliente anterior ve Revendedores (sin lock)','Quiero este plus' not in t)
        t,n,e=await caso(br,{'creadoTs':NEW,'demoHasta':FUT},'revendedores'); chk('nuevo en prueba ve Revendedores con ⭐ en la pestaña','Quiero este plus' not in t and '⭐' in n)
        t,n,e=await caso(br,{'creadoTs':NEW,'demoHasta':None},'revendedores'); chk('nuevo activado sin plus → lock','Quiero este plus' in t,t[:50])
        t,n,e=await caso(br,{'creadoTs':NEW,'demoHasta':None},'cargas'); chk('lock Reparto en Cargas','Reparto' in t and 'Quiero este plus' in t)
        t,n,e=await caso(br,{'creadoTs':NEW,'demoHasta':None},'rendiciones'); chk('lock Reparto en Rendiciones','Quiero este plus' in t)
        t,n,e=await caso(br,{'creadoTs':NEW,'demoHasta':None,'plusRevendedores':True},'revendedores'); chk('plusRevendedores activo → sin lock','Quiero este plus' not in t)
        t,n,e=await caso(br,{'creadoTs':NEW,'demoHasta':None,'plusRevendedores':True},'cargas'); chk('Reparto sigue bloqueado','Quiero este plus' in t)
        t,n,e=await caso(br,{'creadoTs':NEW,'demoHasta':None},'stock'); chk('Stock nunca se bloquea','Quiero este plus' not in t)
        chk('sin errores JS',not e,e)
        await br.close()
asyncio.run(main())
