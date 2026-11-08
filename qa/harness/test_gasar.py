import asyncio
from playwright.async_api import async_playwright
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
BASE='http://127.0.0.1:8767/'
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)
async def caso(br,pagina,demo_dias,rol='administrador',practica=False,email='dueno@test.com',tenant_extra=None):
    ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    async def gs(r):
        if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
        else: await r.fulfill(body='',content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw-*.js',lambda r:r.abort())
    await pg.goto(BASE+pagina); await pg.wait_for_timeout(800)
    await pg.evaluate("""([d,rol,pr,em])=>{const T=firebase.firestore.Timestamp;const t={nombre:'Gas Test',plan:'demo'};
      if(d!==null)t.demoHasta=T.fromMillis(Date.now()+d*86400000); if(pr)t.practica=true;
      window.__DB.set('tenants/t1',t);
      window.__DB.set('usuarios/u1',{email:em,nombre:'Dueño',rol:rol,activo:true,tenantId:'t1',ubicacionId:rol==='administrador'?null:'ub1'});
      window.__DB.set('tenants/t1/ubicaciones/ub1',{nombre:'Central',tipo:'central',activa:true});}""",[demo_dias,rol,practica,email])
    await pg.evaluate("([m])=>window.__login({uid:'u1',email:m,emailVerified:true})",[email]); await pg.wait_for_timeout(2000)
    d=await pg.evaluate("""()=>{const b=document.getElementById('barPrueba');const r=b?b.getBoundingClientRect():null;
      return {bar:!!b,cls:b?b.className:'',txt:b?b.textContent:'',pos:b?getComputedStyle(b).position:'',anim:b?getComputedStyle(b).animationName:'',
      inview:r?(r.bottom<=innerHeight&&r.top>0):false,wa:b&&b.querySelector('a')?b.querySelector('a').href:'',cerrar:b?!!b.querySelector('button'):false,
      app:!!document.querySelector('main')&&!document.querySelector('.login')}}""")
    await ctx.close(); return d,errs
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        for pagina in ('gasar-admin.html','gasar-vendedor.html'):
            rol='administrador' if 'admin' in pagina else 'vendedor'
            d,e=await caso(br,pagina,-2,rol); chk(pagina+': vencida → cartel rojo titilante fijo, app abierta',d['bar'] and 'venc' in d['cls'] and d['pos']=='fixed' and d['anim']!='none' and d['inview'] and d['app'],d)
            chk(pagina+': sin cerrar, con WhatsApp','Terminó tu prueba' in d['txt'] and not d['cerrar'] and 'wa.me/5491136547592' in d['wa'])
            chk(pagina+': sin errores JS',not e,e)
            d,e=await caso(br,pagina,6,rol); chk(pagina+': en curso → cartel ámbar con días',d['bar'] and 'curso' in d['cls'] and '6 días' in d['txt'] and d['app'])
            d,e=await caso(br,pagina,None,rol); chk(pagina+': cliente sin demoHasta (existente) → nada',not d['bar'] and d['app'])
            d,e=await caso(br,pagina,-2,rol,practica=True); chk(pagina+': distribuidora práctica → nada',not d['bar'])
        await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
