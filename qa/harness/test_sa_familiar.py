import asyncio,sys,time
sys.path.insert(0,'/home/claude/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
OK=[];BAD=[];SNAP=[]
def chk(n,c):
    (OK if c else BAD).append(n); print(('✓ ' if c else '✗ ')+n)
async def boot(br,qs='',pre=''):
    pg=await (await br.new_context(viewport={'width':390,'height':844})).new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
    await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
    await pg.expose_function('pySnap',lambda x:((SNAP.clear(),SNAP.append(x)) if 'usuarios/f3' in x else None) and None)
    if pre: await pg.add_init_script(pre)
    await pg.goto('http://127.0.0.1:8778/index.html'+qs); await pg.wait_for_timeout(900)
    return pg,errs
SEED="""now=>{const D=window.__DB;
 D.set('usuarios/t1',{uid:'t1',email:'tit@g.com',nombre:'Titular',plan:'individual',status:'activo',banned:false});
 D.set('perfiles/p1',{nombre:'Mamá',titularUid:'t1',cantidadMiembros:0});
 D.set('perfiles/p1/medicamentos/m1',{nombre:'Enalapril 10mg',dosis:'1',horarios:'08:00',activo:true,createdAt:{__ts:now}});}"""
async def main():
    now=int(time.time()*1000)
    async with async_playwright() as p:
        br=await p.chromium.launch()
        # A) familiar con perfilId: ve el perfil del titular
        pg,errs=await boot(br)
        await pg.evaluate(SEED,now)
        await pg.evaluate("now=>{const D=window.__DB;D.set('usuarios/f1',{uid:'f1',email:'f@g.com',nombre:'Fam',plan:'familiar',esFamiliar:true,perfilId:'p1',status:'activo',banned:false});D.set('perfiles/p1/miembros/f1',{uid:'f1',email:'f@g.com',rol:'editor'});}",now)
        await pg.evaluate("()=>window.__login({uid:'f1',email:'f@g.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        t=await pg.evaluate("()=>document.body.innerText")
        chk('familiar con perfilId ve el perfil del titular (Mamá)','Mamá' in t)
        await pg.evaluate("()=>[...document.querySelectorAll('[data-page=medicacion]')].forEach(e=>e.click())"); await pg.wait_for_timeout(600)
        print('   meds en página:',(await pg.evaluate("()=>(document.getElementById('page-medicacion')||{}).innerText||'sin page'"))[:120].replace('\n',' | '))
        chk('familiar ve la medicación cargada por el titular','Enalapril' in await pg.evaluate("()=>document.body.innerText"))
        chk('sin aviso de error',await pg.evaluate("()=>!document.getElementById('banner-sin-perfil')"))
        await pg.close()
        # B) familiar sin vínculo: aviso rojo (no app vacía muda)
        pg,errs=await boot(br)
        await pg.evaluate(SEED,now)
        await pg.evaluate("()=>window.__DB.set('usuarios/f2',{uid:'f2',email:'g@g.com',nombre:'Fam2',plan:'familiar',esFamiliar:true,status:'activo',banned:false})")
        await pg.evaluate("()=>window.__login({uid:'f2',email:'g@g.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        chk('familiar sin vínculo: aviso rojo visible',await pg.evaluate("()=>!!document.getElementById('banner-sin-perfil')"))
        await pg.close()
        # D) herencia del estado del titular
        pg,errs=await boot(br)
        await pg.evaluate(SEED,now)
        await pg.evaluate("now=>{const D=window.__DB;D.set('usuarios/f4',{uid:'f4',email:'i@g.com',nombre:'Fam4',plan:'familiar',esFamiliar:true,perfilId:'p1',banned:false,demoStart:{__ts:now-40*86400000}});D.set('perfiles/p1/miembros/f4',{uid:'f4',email:'i@g.com',rol:'editor'});D.set('perfiles/p1',{nombre:'Mamá',titularUid:'t1',titularStatus:'activo',titularVence:null});}",now)
        await pg.evaluate("()=>window.__login({uid:'f4',email:'i@g.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        chk('familiar con titular activo: sin pared de prueba aunque su cuenta tenga demo vieja',await pg.evaluate("()=>!document.getElementById('demo-wall').classList.contains('open')"))
        await pg.close()
        pg,errs=await boot(br)
        await pg.evaluate(SEED,now)
        await pg.evaluate("now=>{const D=window.__DB;D.set('usuarios/f5',{uid:'f5',email:'j@g.com',nombre:'Fam5',plan:'familiar',esFamiliar:true,perfilId:'p1',banned:false});D.set('perfiles/p1/miembros/f5',{uid:'f5',email:'j@g.com',rol:'editor'});D.set('perfiles/p1',{nombre:'Mamá',titularUid:'t1',titularStatus:'demo',titularVence:now-86400000});}",now)
        await pg.evaluate("()=>window.__login({uid:'f5',email:'j@g.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        chk('titular con prueba vencida: el familiar ve la pared',await pg.evaluate("()=>document.getElementById('demo-wall').classList.contains('open')"))
        await pg.close()
        pg,errs=await boot(br)
        await pg.evaluate(SEED,now)
        await pg.evaluate("()=>window.__login({uid:'t1',email:'tit@g.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        p1=await pg.evaluate("()=>window.__DB.get('perfiles/p1')")
        chk('el titular activo deja su estado en el perfil',p1.get('titularStatus')=='activo' and p1.get('titularVence') is None)
        await pg.close()
        # C) unirse por link: guarda perfilId y miembro
        pg,errs=await boot(br,'?invite=COD1',"(()=>{const M=new Map();M.set('invitacionesSalud/COD1',{perfilId:'p1',titularUid:'t1',rol:'editor',expiry:{__ts:Date.now()+86400000},usado:false});M.set('perfiles/p1',{nombre:'Mamá',titularUid:'t1',cantidadMiembros:0});window.__DB=M;setInterval(()=>{try{window.pySnap&&window.pySnap(JSON.stringify([...M.entries()]))}catch(e){}},5)})()")
        await pg.evaluate(SEED,now)
        await pg.evaluate("now=>window.__DB.set('invitacionesSalud/COD1',{perfilId:'p1',titularUid:'t1',rol:'editor',expiry:{__ts:now+86400000},usado:false})",now)
        await pg.evaluate("()=>window.__login({uid:'f3',email:'h@g.com',emailVerified:true})"); await pg.wait_for_timeout(2000)
        vis=await pg.evaluate("()=>[document.getElementById('invite-already-logged').style.display,document.getElementById('screen-invite').classList.contains('active')]")
        print('   invitación estado:',vis,await pg.evaluate("()=>[document.getElementById('invite-perfil-nombre').textContent,document.getElementById('invite-expired-msg').textContent.slice(0,60),JSON.stringify(window.__DB.get('usuarios/f3')||null)]"),errs)
        await pg.evaluate("()=>document.getElementById('btn-inv-join').click()"); await pg.wait_for_timeout(2500)
        snap=dict(__import__('json').loads(SNAP[0]) if SNAP else [])
        u=snap.get('usuarios/f3'); m=snap.get('perfiles/p1/miembros/f3'); inv=snap.get('invitacionesSalud/COD1',{})
        chk('unirse guarda perfilId en la cuenta',bool(u) and u.get('perfilId')=='p1' and u.get('esFamiliar')==True)
        chk('unirse crea el miembro con su rol',bool(m) and m.get('rol')=='editor')
        chk('la invitación queda usada',inv.get('usado')==True)
        await pg.close(); await br.close()
    print('OK',len(OK),'FALLAS',BAD)
asyncio.run(main())
