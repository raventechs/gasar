import asyncio
from playwright.async_api import async_playwright
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
BASE='http://127.0.0.1:8771/index.html'
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
    await pg.evaluate("""(d)=>{const T=firebase.firestore.Timestamp;const c={email:'l@t.com',activo:true,nombre:'Barb',plan:'basico',features:{}};
      if(d==='null')c.demoHasta=null; else if(d!=='absent')c.demoHasta=T.fromMillis(Date.now()+d*86400000);
      window.__DB.set('clientes/l@t.com',c);}""",demo)
    await pg.evaluate("()=>window.__login({uid:'u1',email:'l@t.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
    await pg.evaluate("()=>{0}")
    return ctx,pg,errs

async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        ctx,pg,e=await caso(br,6)
        hoy=await pg.evaluate("()=>new Date().toISOString().slice(0,10)")
        await pg.evaluate("""(h)=>{window.__DB.set('negocios/u1/barberos/b1',{nombre:'Juan',activo:true});window.__DB.set('negocios/u1/barberos/b2',{nombre:'Pedro',activo:true});
          window.__DB.set('negocios/u1/turnos/t1',{fecha:h,hora:'10:00',barberoId:'b1',barberoNombre:'Juan',servicioNombre:'Corte',clienteNombre:'Ana',estado:'pendiente',origen:'cliente'});
          window.__DB.set('negocios/u1/turnos/t2',{fecha:h,hora:'11:00',barberoId:'b2',barberoNombre:'Pedro',servicioNombre:'Barba',clienteNombre:'Luis',estado:'pendiente',origen:'staff'});}""",hoy)
        await pg.evaluate("()=>switchTab('turnos')"); await pg.wait_for_timeout(600)
        await pg.evaluate("()=>switchTab('caja')"); await pg.wait_for_timeout(400)
        await pg.click("text=📅 Turno"); await pg.wait_for_timeout(1500)
        c=await pg.evaluate("()=>document.getElementById('agendaCal').innerText")
        chk('botón Turno en la caja abre agenda con calendario y marca 2 turnos hoy','📌' in c and '2' in c,c[:70].replace('\n',' '))
        await pg.evaluate("()=>{const f=document.getElementById('turnosFecha').value;const d=new Date(f+'T12:00:00');d.setDate(d.getDate()+1);calElegir(d.toISOString().slice(0,10))}"); await pg.wait_for_timeout(900)
        await pg.evaluate("()=>calElegir(new Date().toISOString().slice(0,10))"); await pg.wait_for_timeout(900)
        print(await pg.evaluate("()=>[typeof turnosDelDia==='object'?JSON.stringify(turnosDelDia).slice(0,200):'',[...window.__DB.keys()].filter(k=>k.includes('turnos')||k.includes('barberos')).join(',')]"))
        t=await pg.evaluate("()=>document.getElementById('agendaGrid').innerText")
        chk('agenda muestra web (Ana) y local (Luis)','Ana' in t and 'Luis' in t,t[:120].replace('\n',' '))
        chk('columnas Juan y Pedro','Juan' in t and 'Pedro' in t)
        await pg.click("#agendaGrid button >> nth=0"); await pg.wait_for_timeout(500)
        v=await pg.evaluate("()=>[document.getElementById('modalTurno').classList.contains('show'),document.getElementById('turnoHora').value,document.getElementById('turnoBarbero').value]")
        chk('tocar libre abre modal con hora y barbero',v[0] and v[1] and v[2],v)
        await pg.evaluate("()=>cerrarModalTurno()")
        await pg.evaluate("()=>agendaDia(1)"); await pg.wait_for_timeout(800)
        t=await pg.evaluate("()=>document.getElementById('agendaGrid').innerText"); chk('día siguiente sin turnos','Ana' not in t)
        await pg.evaluate("()=>setVistaTurnos('lista')"); await pg.wait_for_timeout(500)
        chk('sin errores JS',not e,e)
        await br.close()
asyncio.run(main())
