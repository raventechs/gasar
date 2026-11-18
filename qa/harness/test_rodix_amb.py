import asyncio,sys
sys.path.insert(0,'/home/claude/raventechs/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
BASE='http://127.0.0.1:8790/index.html'
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)
async def nuevo(br,feat=True,rol='owner'):
    ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:200])); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
    await pg.clock.install()
    await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
    await pg.goto(BASE); await pg.wait_for_timeout(900)
    await pg.evaluate("""(a)=>{const D=window.__DB;
      D.set('usuarios/own1',{uid:'own1',email:'own@t.com',status:'activo',flotaId:'own1',rolFlota:'owner',features:{limiteVehiculos:10,checklistHabilitado:a.feat,flotaHabilitada:true}});
      D.set('usuarios/ch1',{uid:'ch1',email:'chofer@t.com',status:'activo',flotaId:'own1',rolFlota:'chofer'});
      D.set('vehicles/v1',{uid:'own1',brand:'Mercedes-Benz',model:'Sprinter Ambulancia',plate:'AF412KL',year:2021,km:84500,fuel:'Diesel',createdAt:{__ts:Date.now()}});
      D.set('vehicles/v2',{uid:'own1',brand:'Fiat',model:'Cronos',plate:'AD330BH',year:2019,km:98700,fuel:'Nafta',createdAt:{__ts:Date.now()}});
    }""",{'feat':feat})
    u={'owner':"{uid:'own1',email:'own@t.com',emailVerified:true}",'chofer':"{uid:'ch1',email:'chofer@t.com',emailVerified:true}"}[rol]
    await pg.evaluate("()=>window.__login(%s)"%u); await pg.wait_for_timeout(2200)
    return ctx,pg,errs
async def vis(pg,sel): return await pg.evaluate("(s)=>{const e=document.querySelector(s);return !!e&&e.offsetParent!==null}",sel)
async def nav(pg,page,vid=None):
    await pg.evaluate("(p)=>{document.querySelector('.nav-item[data-page=\"'+p+'\"], .mob-nav-item[data-page=\"'+p+'\"]').click()}",'vehicles' if vid else page)
    await pg.wait_for_timeout(500)
    if vid:
        await pg.evaluate("(v)=>document.querySelector('.vehicle-card[data-vid=\"'+v+'\"]').click()",vid); await pg.wait_for_timeout(600)
async def ver(pg,vid='v1'): await nav(pg,'vehicles',vid)
async def db(pg,expr): return await pg.evaluate("()=>{const D=window.__DB;%s}"%expr)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        # ── sin el módulo activado
        ctx,pg,e=await nuevo(br,feat=False); await ver(pg)
        chk('sin módulo: no aparece la pestaña Insumos',not await vis(pg,'#tab-insumos'))
        await ctx.close()
        # ── dueño con el módulo
        ctx,pg,e=await nuevo(br); await ver(pg)
        chk('dueño: aparece la pestaña Insumos',await vis(pg,'#tab-insumos'))
        await pg.click('#tab-insumos'); await pg.wait_for_timeout(400)
        chk('sin lista: ofrece crear desde plantilla',await vis(pg,'#btn-seed-insumos'))
        await pg.click('#btn-seed-insumos'); await pg.wait_for_timeout(2500)
        n=await db(pg,"return [...D.keys()].filter(k=>k.startsWith('vehicles/v1/insumos/')).length")
        chk('plantilla crea 7 insumos',n==7,n)
        chk('HALLAZGO: la pantalla muestra la lista creada sin esperar el refresco de 60 s',await pg.evaluate("document.querySelectorAll('[data-insumo-id]').length")==7,'(0 = queda "Sin checklist" hasta el refresco)')
        await ver(pg)
        chk('muestra los 7 ítems tildados',await pg.evaluate("document.querySelectorAll('[data-insumo-id]').length")==7 and await pg.evaluate("[...document.querySelectorAll('[data-insumo-id]')].every(c=>c.checked)"))
        # destildar uno → falta
        await pg.evaluate("()=>{const c=document.querySelector('[data-insumo-id]');c.checked=false;c.dispatchEvent(new Event('change'))}"); await pg.wait_for_timeout(1500)
        f=await db(pg,"return [...D.entries()].filter(([k,v])=>k.startsWith('vehicles/v1/insumos/')&&v.presente===false).length")
        chk('destildar guarda «falta» y quién lo cambió',f==1)
        await nav(pg,'alerts')
        t=await pg.inner_text('#page-alerts'); chk('Alertas: avisa insumos faltantes y revisión sin confirmar','Faltan 1 insumo' in t and 'Sin confirmar la revisión' in t,t[:120].replace('\n',' '))
        chk('Alertas NO inventa insumos para el auto común (v2)','Cronos' not in t,'')
        # confirmar revisión
        await ver(pg)
        await pg.click('#tab-insumos'); await pg.wait_for_timeout(400)
        await pg.click('#btn-confirmar-revision'); await pg.wait_for_timeout(1500)
        r=await db(pg,"const k=[...D.keys()].filter(k=>k.startsWith('vehicles/v1/revisiones/'));return k.length?JSON.stringify(D.get(k[0])):''")
        chk('confirmar revisión guarda fecha, quién y faltantes','own@t.com' in r and '"completa":false' in r,r[:110])
        # agregar / editar / eliminar
        await ver(pg); await pg.click('#tab-insumos'); await pg.wait_for_timeout(400)
        await pg.click('#btn-add-insumo'); await pg.fill('#f-nombre','Suero fisiológico'); await pg.fill('#f-cantidad','6'); await pg.click('#modal-save-btn'); await pg.wait_for_timeout(1500)
        n=await db(pg,"return [...D.entries()].filter(([k,v])=>k.startsWith('vehicles/v1/insumos/')&&v.nombre==='Suero fisiológico'&&v.cantidad===6).length")
        chk('agregar ítem personalizado',n==1,n)
        await ver(pg); await pg.click('#tab-insumos'); await pg.wait_for_timeout(400)
        await pg.click('[data-edit-insumo] >> nth=0'); await pg.fill('#f-nombre','Jeringas 10ml'); await pg.click('#modal-save-btn'); await pg.wait_for_timeout(1200)
        n=await db(pg,"return [...D.entries()].filter(([k,v])=>v.nombre==='Jeringas 10ml').length"); chk('editar ítem',n==1,n)
        await ver(pg); await pg.click('#tab-insumos'); await pg.wait_for_timeout(400)
        await pg.click('[data-del-insumo] >> nth=0'); await pg.wait_for_timeout(1200)
        n=await db(pg,"return [...D.keys()].filter(k=>k.startsWith('vehicles/v1/insumos/')).length"); chk('eliminar ítem (8 → 7)',n==7,n)
        chk('sin errores JS',not e,e); await ctx.close()
        # ── chofer
        ctx,pg,e=await nuevo(br,rol='chofer')
        await pg.evaluate("()=>{const D=window.__DB;['Jeringas','Gasas'].forEach((n,i)=>D.set('vehicles/v1/insumos/i'+i,{nombre:n,cantidad:3,presente:true}))}")
        await pg.clock.fast_forward(61000); await pg.wait_for_timeout(1500)
        await ver(pg); await pg.wait_for_timeout(1000)
        chk('chofer: ve los insumos sin poder agregar/editar/borrar',await pg.evaluate("document.querySelectorAll('[data-insumo-id]').length")==2 and not await vis(pg,'#btn-add-insumo') and not await vis(pg,'[data-edit-insumo]') and not await vis(pg,'[data-del-insumo]'))
        await pg.evaluate("()=>{const c=document.querySelector('[data-insumo-id]');c.checked=false;c.dispatchEvent(new Event('change'))}"); await pg.wait_for_timeout(1200)
        u=await db(pg,"return JSON.stringify(D.get('vehicles/v1/insumos/i0'))"); chk('chofer: puede marcar que falta y queda su mail','chofer@t.com' in u,u[:100])
        await pg.click('#btn-confirmar-revision'); await pg.wait_for_timeout(1400)
        r=await db(pg,"const k=[...D.keys()].filter(k=>k.startsWith('vehicles/v1/revisiones/'));return k.length?JSON.stringify(D.get(k[0])):''"); chk('chofer: confirma la revisión diaria','chofer@t.com' in r,r[:100])
        chk('chofer: sin Ajustes ni Equipo',not await vis(pg,'#btn-ajustes-mob') and not await vis(pg,'#btn-equipo-mob'))
        chk('sin errores JS',not e,e); await ctx.close()
        # ── modo práctica
        ctx,pg,e=await nuevo(br)
        await pg.evaluate("()=>{const D=window.__DB;for(const k of [...D.keys()])if(k.startsWith('vehicles/'))D.delete(k)}")
        await pg.evaluate("()=>cargarPractica()"); await pg.wait_for_timeout(6000)
        nv=await db(pg,"return [...D.keys()].filter(k=>/^vehicles\\/[^/]+$/.test(k)).length"); ni=await db(pg,"return [...D.keys()].filter(k=>k.includes('/insumos/')).length")
        chk('práctica: 5 vehículos y insumos solo en las 2 ambulancias (14)',nv==5 and ni==14,(nv,ni))
        await pg.evaluate("()=>quitarPractica()"); await pg.wait_for_timeout(5000)
        nv=await db(pg,"return [...D.keys()].filter(k=>k.startsWith('vehicles/')).length"); chk('práctica: quitar deja todo limpio',nv==0,nv)
        chk('sin errores JS',not e,e); await ctx.close()
        await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
