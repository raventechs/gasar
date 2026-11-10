import asyncio,sys,time
sys.path.insert(0,'/home/claude/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
OK=[];BAD=[]
def chk(n,c):
    (OK if c else BAD).append(n); print(('✓ ' if c else '✗ ')+n)
async def boot(br):
    pg=await (await br.new_context(viewport={'width':390,'height':844})).new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
    await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
    await pg.goto('http://127.0.0.1:8777/index.html'); await pg.wait_for_timeout(800)
    return pg,errs
def seed(uid,extra,now):
    return """a=>{const D=window.__DB,now=a[0];
      D.set('usuarios/%s',Object.assign({uid:'%s',email:'%s@g.com',rol:'owner',modo:'multi',status:'activo',banned:false,rubroPreguntado:true},%s));
      D.set('negocios/n1',{nombre:'Kiosco Centro',ownerUid:'%s',tipo:'Kiosco',icon:'🍬',productos:[
        {id:'p1',nombre:'Gaseosa',precio:1500,sk:true,min:3,base:5,desde:now-86400000},
        {id:'p2',nombre:'Alfajor',precio:800,sk:false,min:0}]});}"""%(uid,uid,uid,extra,uid)
async def login(pg,uid):
    await pg.evaluate("u=>window.__login({uid:u,email:u+'@g.com',emailVerified:true})",uid); await pg.wait_for_timeout(2500)
    await pg.evaluate("()=>document.getElementById('modal-rubro')?.remove()")
async def main():
    now=int(time.time()*1000)
    async with async_playwright() as p:
        br=await p.chromium.launch()
        # A) Avanzada en prueba: ve Plus con etiqueta, vende por catálogo y baja el stock
        pg,errs=await boot(br)
        await pg.evaluate(seed('a1',"{plan:'avanzada',demoHasta:{__ts:%d}}"%(now+10*86400000),now),[now])
        await login(pg,'a1')
        chk('Avanzada en prueba: aparece Productos en el menú',await pg.evaluate("()=>[...document.querySelectorAll('.mob-item[data-page=productos]')].some(e=>e.offsetParent!==null)"))
        await pg.evaluate("()=>document.querySelector('.nav-item[data-page=productos]').click()"); await pg.wait_for_timeout(900)
        t=await pg.evaluate("()=>document.getElementById('page-productos').innerText")
        chk('lista de productos con stock calculado (5 u.)','Gaseosa' in t and '5 u.' in t and 'Alfajor' in t and 'sin control de stock' in t)
        chk('etiqueta Plus incluido en la prueba','Plus' in t)
        # vender por catálogo
        await pg.evaluate("()=>document.querySelector('.nav-item[data-page=ventas]').click()"); await pg.wait_for_timeout(500)
        await pg.evaluate("()=>document.getElementById('btn-nueva-venta').click()"); await pg.wait_for_timeout(900)
        chk('en Vender hay catálogo',await pg.evaluate("()=>!!document.getElementById('vd-cat')"))
        await pg.evaluate("()=>{document.querySelector('[data-add=p1]').click();document.querySelector('[data-add=p1]').click();document.querySelector('[data-add=p2]').click()}"); await pg.wait_for_timeout(300)
        imp=await pg.evaluate("()=>document.getElementById('vd-importe').value"); desc=await pg.evaluate("()=>document.getElementById('vd-desc').value")
        chk('el total se arma solo (2×1500+800=3800) y la descripción también',imp=='3800' and '2× Gaseosa' in desc and 'Alfajor' in desc)
        await pg.evaluate("()=>{document.querySelector('#vd-medios [data-m=efectivo]').click();document.getElementById('vd-guardar').click()}"); await pg.wait_for_timeout(1500)
        v=[x for k,x in (await pg.evaluate("()=>[...window.__DB.entries()]")) if k.startswith('ventas/')]
        chk('la venta guarda los items',bool(v) and any(i.get('id')=='p1' and i.get('c')==2 for i in v[0].get('items',[])))
        await pg.evaluate("()=>document.querySelector('.nav-item[data-page=productos]').click()"); await pg.wait_for_timeout(1200)
        t=await pg.evaluate("()=>document.getElementById('page-productos').innerText")
        chk('el stock baja a 3 u. y aparece la alerta (mínimo 3)','3 u.' in t and 'Se te está acabando' in t)
        # nuevo producto
        await pg.evaluate("()=>document.getElementById('pr-nuevo').click()"); await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{document.getElementById('pm-nombre').value='Chicle';document.getElementById('pm-precio').value='200';document.getElementById('pm-save').click()}"); await pg.wait_for_timeout(900)
        negp=await pg.evaluate("()=>window.__DB.get('negocios/n1').productos.map(p=>p.nombre)")
        chk('crear producto lo agrega al negocio',negp==['Gaseosa','Alfajor','Chicle'])
        # dashboard con alerta
        await pg.evaluate("()=>document.querySelector('.nav-item[data-page=dashboard]').click()"); await pg.wait_for_timeout(1500)
        chk('el tablero muestra la alerta de stock',('Se te está acabando' in await pg.evaluate("()=>document.getElementById('dash-stock').innerText")))
        chk('sin errores JS',not errs); 
        if errs: print(errs)
        await pg.close()
        # B) Avanzada con prueba vencida y sin Plus: promo, sin Productos, sin catálogo, ficha bloqueada
        pg,errs=await boot(br)
        await pg.evaluate(seed('b1',"{plan:'avanzada',demoHasta:{__ts:%d}}"%(now-86400000),now),[now])
        await login(pg,'b1')
        chk('sin Plus: no hay Productos en el menú',await pg.evaluate("()=>![...document.querySelectorAll('.mob-item[data-page=productos]')].some(e=>e.offsetParent!==null)"))
        await pg.evaluate("()=>document.querySelector('.nav-item[data-page=dashboard]').click()"); await pg.wait_for_timeout(1200)
        d=await pg.evaluate("()=>document.getElementById('dash-auto').innerText")
        chk('sin Plus: el tablero muestra la tarjeta para pedirlo',('Quiero este Plus' in d and 'Lo importante de hoy' not in d))
        await pg.close()
        # C) mismo caso pero con features activadas por el admin
        pg,errs=await boot(br)
        await pg.evaluate(seed('c1',"{plan:'avanzada',demoHasta:{__ts:%d},features:{catalogo:true,tablero:true,limiteNegocios:3}}"%(now-86400000),now),[now])
        await login(pg,'c1')
        chk('con features del admin: aparece Productos',await pg.evaluate("()=>[...document.querySelectorAll('.mob-item[data-page=productos]')].some(e=>e.offsetParent!==null)"))
        await pg.close()
        # D) cuenta anterior (sin plan) conserva todo; E) Básico no lo ve
        pg,errs=await boot(br)
        await pg.evaluate(seed('d1',"{}",now),[now]); await login(pg,'d1')
        chk('cuenta anterior (sin plan) conserva todo',await pg.evaluate("()=>[...document.querySelectorAll('.mob-item[data-page=productos]')].some(e=>e.offsetParent!==null)"))
        await pg.close()
        pg,errs=await boot(br)
        await pg.evaluate(seed('e1',"{plan:'basico',modo:'single',demoHasta:{__ts:%d}}"%(now+10*86400000),now),[now]); await login(pg,'e1')
        chk('Básico no ve Productos ni catálogo en Caja',await pg.evaluate("()=>![...document.querySelectorAll('.mob-item[data-page=productos]')].some(e=>e.offsetParent!==null)&&!document.getElementById('vd-cat')"))
        await pg.close(); await br.close()
    print('OK',len(OK),'FALLAS',BAD)
asyncio.run(main())
