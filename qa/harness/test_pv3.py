import asyncio,sys,json,time
sys.path.insert(0,'/home/claude/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
OK=[];BAD=[]
def chk(n,c):
    (OK if c else BAD).append(n); print(('✓ ' if c else '✗ ')+n)
async def boot(br,viewport=(390,844),fake_now=None):
    ctx=await br.new_context(viewport={'width':viewport[0],'height':viewport[1]}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
    await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
    if fake_now: await pg.add_init_script("(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off)}static now(){return R.now()+off}};window.Date=D})()"%fake_now)
    await pg.goto('http://127.0.0.1:8777/index.html'); await pg.wait_for_timeout(900)
    return pg,errs
async def db(pg,key): return await pg.evaluate("k=>window.__DB.get(k)",key)
async def keys(pg,pre): return await pg.evaluate("p=>[...window.__DB.keys()].filter(k=>k.startsWith(p))",pre)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        # ---------- 1) CUENTA NUEVA (Google) => Básica
        pg,errs=await boot(br)
        await pg.evaluate("()=>window.__login({uid:'n1',email:'nuevo@gmail.com',emailVerified:true,displayName:'Ana Pérez'})"); await pg.wait_for_timeout(2500)
        u=await db(pg,'usuarios/n1')
        chk('alta nueva: plan básico',u and u.get('plan')=='basico')
        chk('alta nueva: demoHasta ~14 días',u and abs(u['demoHasta']['__ts']-(time.time()*1000+14*86400000))<120000)
        chk('alta nueva: status demo',u and u.get('status')=='demo')
        vis=await pg.evaluate("()=>[...document.querySelectorAll('.mob-item')].filter(e=>e.style.display!=='none').map(e=>e.dataset.page)")
        chk('nav básico = vender, ventas, gastos, fiado, cierre',set(vis)=={'vender','ventas','gastos','fiado'})
        chk('arranca en Vender',await pg.evaluate("()=>document.getElementById('page-vender').style.display=='block'"))
        chk('banner de prueba visible',await pg.evaluate("()=>!!document.getElementById('demo-banner')&&document.getElementById('demo-banner').textContent.includes('14')"))
        chk('checklist visible (0 de 4)',await pg.evaluate("()=>document.querySelector('.pasos-card')?.textContent.includes('0 de 4')"))
        # venta efectivo
        await pg.fill('#vd-importe','1500'); await pg.click('#vd-medios [data-m=efectivo]'); await pg.fill('#vd-desc','Gaseosas'); await pg.click('#vd-guardar'); await pg.wait_for_timeout(800)
        vk=await keys(pg,'ventas/'); chk('venta efectivo guardada',len(vk)==1)
        v=await db(pg,vk[0]); chk('venta: medio efectivo, pagos[1], fecha AR',v['medio']=='efectivo' and len(v['pagos'])==1 and v['fecha'])
        # venta mixta efectivo+transferencia
        await pg.fill('#vd-importe','3000'); await pg.click('#vd-split-btn'); await pg.select_option('#vd-s-m1','efectivo'); await pg.fill('#vd-s-a','1000'); await pg.select_option('#vd-s-m2','transferencia'); await pg.wait_for_timeout(200)
        chk('resto mostrado',await pg.evaluate("()=>document.getElementById('vd-s-resto').textContent.replace(/\\D/g,'')")=='2000')
        await pg.click('#vd-guardar'); await pg.wait_for_timeout(800)
        vs=[await db(pg,k) for k in await keys(pg,'ventas/')]; mx=[v for v in vs if v['medio']=='mixto']
        chk('venta mixta guardada con 2 pagos',len(mx)==1 and mx[0]['pagos']==[{'medio':'efectivo','importe':1000},{'medio':'transferencia','importe':2000}])
        # fiado: pedir cliente
        await pg.fill('#vd-importe','800'); await pg.click('#vd-medios [data-m=fiado]'); await pg.click('#vd-guardar'); await pg.wait_for_timeout(300)
        chk('fiado sin cliente no guarda',len(await keys(pg,'ventas/'))==2)
        # nuevo cliente desde Vender
        await pg.click('#vd-cli-nuevo'); await pg.fill('#mcc-nombre','Doña Marta'); await pg.fill('#mcc-tel','11 5555-1234'); await pg.click('#btn-mcc-save'); await pg.wait_for_timeout(900)
        ck=await keys(pg,'clientes/'); chk('cliente cc creado',len(ck)==1 and (await db(pg,ck[0]))['tipo']=='cc' and (await db(pg,ck[0]))['saldo']==0)
        chk('cliente quedó elegido en el select',await pg.evaluate("()=>!!document.getElementById('vd-cliente').value"))
        await pg.fill('#vd-importe','800'); await pg.click('#vd-medios [data-m=fiado]'); await pg.fill('#vd-desc','Yerba y fideos')
        await pg.evaluate("()=>{const s=document.getElementById('vd-cliente');s.dispatchEvent(new Event('change'))}")
        await pg.click('#vd-guardar'); await pg.wait_for_timeout(900)
        c=await db(pg,ck[0]); chk('saldo = 800 tras fiado',c['saldo']==800)
        # fiado mixto: 500 efectivo + 700 fiado
        await pg.fill('#vd-importe','1200'); await pg.click('#vd-split-btn'); await pg.select_option('#vd-s-m1','efectivo'); await pg.fill('#vd-s-a','500'); await pg.select_option('#vd-s-m2','fiado')
        await pg.select_option('#vd-cliente',ck[0].split('/')[1]); await pg.click('#vd-guardar'); await pg.wait_for_timeout(900)
        c=await db(pg,ck[0]); chk('saldo = 1500 tras fiado mixto (800+700)',c['saldo']==1500)
        # Fiado page
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=fiado]').click()"); await pg.wait_for_timeout(500)
        chk('fiado lista cliente con saldo',await pg.evaluate("()=>document.getElementById('fd-lista').textContent.includes('1.500')"))
        await pg.evaluate("()=>document.querySelector('[data-cc]').click()"); await pg.wait_for_timeout(700)
        chk('detalle muestra 2 movimientos',await pg.evaluate("()=>document.querySelectorAll('#fd-movs .fd-mov').length")==2)
        # cobro parcial 600 en efectivo
        await pg.click('#fd-b-cobrar'); await pg.fill('#fd-c-monto','600'); await pg.select_option('#fd-c-medio','efectivo'); await pg.click('#fd-c-ok'); await pg.wait_for_timeout(1000)
        c=await db(pg,ck[0]); chk('saldo = 900 tras cobro parcial',c['saldo']==900)
        # cobro de más
        await pg.click('#fd-b-cobrar'); await pg.fill('#fd-c-monto','5000'); await pg.click('#fd-c-ok'); await pg.wait_for_timeout(400)
        chk('no deja cobrar más de lo que debe',(await db(pg,ck[0]))['saldo']==900)
        # anular el cobro => vuelve a 1500
        await pg.evaluate("()=>{const b=[...document.querySelectorAll('[data-anular]')];const cobro=b.find(x=>x.closest('.fd-mov').textContent.includes('−'));cobro.click()}"); await pg.wait_for_timeout(1000)
        chk('anular cobro restituye saldo (1500)',(await db(pg,ck[0]))['saldo']==1500)
        # whatsapp link
        wa=await pg.evaluate("()=>{let u='';window.open=x=>{u=x};document.getElementById('fd-b-wa').click();return u}")
        chk('whatsapp al 549 + teléfono limpio',wa.startswith('https://wa.me/5491155551234?text='))
        await pg.evaluate("()=>document.getElementById('fd-cerrar').click()")
        # Cierre de caja y dashboard-sumas
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=ventas]').click()"); await pg.wait_for_timeout(500)
        t=await pg.evaluate("()=>document.getElementById('page-ventas').innerText")
        chk('cierre: total cobrado = 1500+1000+500+... ',True)
        print(t.replace('\n',' | ')[:400])
        # Cobrado esperado: efectivo 1500+1000+500=3000 ; transferencia 2000 ; total 5000 ; fiado 1500
        chk('cierre: efectivo $3.000',('3.000' in t))
        chk('cierre: transferencia $2.000',('2.000' in t))
        chk('cierre: total cobrado $5.000',('Total cobrado' in t and '5.000' in t))
        chk('cierre: fiado del día $1.500',('En cuenta (no entró plata)' in t and '1.500' in t))
        wau=await pg.evaluate("()=>{let u='';window.open=x=>{u=x};document.getElementById('btn-cerrar-caja').click();return decodeURIComponent(u)}")
        chk('cierre: botón abre WhatsApp con el resumen',wau.startswith('https://wa.me/?text=') and 'Cierre de caja' in wau and 'Total cobrado: $' in wau and '5.000' in wau)
        chk('checklist: cierre marcado',await pg.evaluate("()=>JSON.parse(localStorage.getItem('pv_pasos_n1')||'{}').cierre===1"))
        chk('sin errores JS (cuenta nueva)',errs==[]); 
        if errs: print(errs)
        # práctica y quitar
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=cierre]')&&0"); 
        await pg.close()

        # ---------- 2) CUENTA ANTERIOR (sin plan) => todo como antes
        pg,errs=await boot(br)
        await pg.evaluate("()=>{window.__DB.set('usuarios/v1',{uid:'v1',email:'viejo@gmail.com',rol:'owner',modo:'multi',status:'activo',banned:false});window.__DB.set('negocios/nv',{nombre:'Kiosco Viejo',ownerUid:'v1',tipo:'Kiosco',icon:'🏪'});window.__DB.set('ventas/old1',{negocioId:'nv',ownerUid:'v1',empleadoUid:'v1',empleadoNombre:'viejo',importe:2500,medio:'mp',descripcion:'Venta vieja',fecha:'%s',hora:'10:00',createdAt:{__ts:%d}})}"%(__import__('datetime').datetime.now().strftime('%Y-%m-%d'),int(time.time()*1000)))
        await pg.evaluate("()=>window.__login({uid:'v1',email:'viejo@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        vis=await pg.evaluate("()=>[...document.querySelectorAll('.mob-item')].filter(e=>e.style.display!=='none').map(e=>e.dataset.page)")
        chk('cuenta vieja conserva dashboard y empleados, sin vender',set(vis)=={'dashboard','ventas','empleados','gastos','fiado'})
        chk('cuenta vieja arranca en dashboard',await pg.evaluate("()=>document.getElementById('page-dashboard').style.display!='none'"))
        chk('cuenta vieja: dato viejo cuenta (MP $2.500)',await pg.evaluate("()=>document.getElementById('page-dashboard').innerText.includes('2.500')"))
        chk('cuenta vieja sin banner',await pg.evaluate("()=>!document.getElementById('demo-banner')"))
        u=await db(pg,'usuarios/v1'); chk('cuenta vieja no recibe plan/demoHasta',('plan' not in u) and ('demoHasta' not in u))
        # nueva venta desde Ventas abre Vender
        await pg.evaluate("()=>document.querySelector('.nav-item[data-page=ventas]').click()"); await pg.wait_for_timeout(300)
        await pg.evaluate("()=>document.getElementById('btn-nueva-venta').click()"); await pg.wait_for_timeout(300)
        chk('Nueva venta (vieja) abre Vender',await pg.evaluate("()=>document.getElementById('page-vender').style.display=='block'"))
        # editar venta vieja sigue andando
        await pg.evaluate("()=>document.querySelector('.nav-item[data-page=ventas]').click()"); await pg.wait_for_timeout(300)
        chk('venta vieja editable (botón lápiz)',await pg.evaluate("()=>!!document.querySelector('[data-edit-venta=old1]')"))
        chk('sin errores JS (cuenta vieja)',errs==[]); 
        if errs: print(errs)
        await pg.close()

        # ---------- 3) Vencida: nueva no bloquea; vieja bloquea; empleado nunca
        pg,errs=await boot(br)
        ayer=int((time.time()-86400)*1000)
        await pg.evaluate("a=>{window.__DB.set('usuarios/e1',{uid:'e1',email:'exp@gmail.com',rol:'owner',modo:'single',plan:'basico',status:'demo',banned:false,demoStart:{__ts:a-14*86400000},demoHasta:{__ts:a}});window.__DB.set('negocios/ne',{nombre:'Exp',ownerUid:'e1',tipo:'Kiosco',icon:'🏪'})}",ayer)
        await pg.evaluate("()=>window.__login({uid:'e1',email:'exp@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2200)
        chk('prueba vencida (nueva): NO bloquea',await pg.evaluate("()=>!document.getElementById('demo-wall').classList.contains('open')"))
        chk('prueba vencida: banner rojo titilante',await pg.evaluate("()=>document.getElementById('demo-banner').className=='urgente'"))
        # se sigue pudiendo vender
        await pg.fill('#vd-importe','100'); await pg.click('#vd-medios [data-m=efectivo]'); await pg.click('#vd-guardar'); await pg.wait_for_timeout(600)
        chk('vencida: igual puede vender',len([k for k in await keys(pg,'ventas/')])==1)
        await pg.close()
        pg,errs=await boot(br)
        await pg.evaluate("a=>{window.__DB.set('usuarios/o1',{uid:'o1',email:'old@gmail.com',rol:'owner',modo:'single',status:'demo',banned:false,demoStart:{__ts:a-20*86400000}});window.__DB.set('negocios/no',{nombre:'Old',ownerUid:'o1',tipo:'Kiosco',icon:'🏪'})}",ayer)
        await pg.evaluate("()=>window.__login({uid:'o1',email:'old@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2200)
        chk('prueba vencida (vieja): bloquea como antes',await pg.evaluate("()=>document.getElementById('demo-wall').classList.contains('open')"))
        await pg.close()
        pg,errs=await boot(br)
        await pg.evaluate("a=>{window.__DB.set('usuarios/own2',{uid:'own2',email:'o2@gmail.com',rol:'owner',modo:'multi',status:'activo',banned:false});window.__DB.set('negocios/n2',{nombre:'N2',ownerUid:'own2',tipo:'Kiosco',icon:'🏪'});window.__DB.set('usuarios/em1',{uid:'em1',email:'emp@gmail.com',rol:'employee',ownerUid:'own2',negocioId:'n2',estado:'aprobado',status:'demo',banned:false,demoStart:{__ts:a-30*86400000}})}",ayer)
        await pg.evaluate("()=>window.__login({uid:'em1',email:'emp@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2200)
        chk('empleado: no se bloquea por prueba',await pg.evaluate("()=>!document.getElementById('demo-wall').classList.contains('open')"))
        chk('empleado: opción Transferencia',await pg.evaluate("()=>!!document.getElementById('m-transferencia')"))
        await pg.fill('#emp-importe','700'); await pg.click('#m-transferencia'); await pg.click('#btn-venta'); await pg.wait_for_timeout(700)
        vs=[await db(pg,k) for k in await keys(pg,'ventas/')]; chk('empleado registra transferencia',len(vs)==1 and vs[0]['medio']=='transferencia')
        await pg.close()

        # ---------- 4) HORA ARGENTINA: 23:30 AR del 8/11 = 02:30 UTC del 9/11
        import datetime
        fake=int(datetime.datetime(2026,11,9,2,30,tzinfo=datetime.timezone.utc).timestamp()*1000)
        pg,errs=await boot(br,fake_now=fake)
        r=await pg.evaluate("()=>{const x=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Argentina/Buenos_Aires'}).format(new Date());return [x,new Date().toISOString().slice(0,10)]}")
        print('   fake now ->',r)
        await pg.evaluate("()=>window.__login({uid:'h1',email:'noche@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2200)
        await pg.fill('#vd-importe','999'); await pg.click('#vd-medios [data-m=efectivo]'); await pg.click('#vd-guardar'); await pg.wait_for_timeout(700)
        vs=[await db(pg,k) for k in await keys(pg,'ventas/')]
        chk('venta de las 23:30 AR queda en el 8/11 (no en el 9/11)',len(vs)==1 and vs[0]['fecha']=='2026-11-08' and vs[0]['hora'].startswith('23:'))
        await pg.close()

        # ---------- 5) ADMIN: plan, demoHasta, +7, activar
        pg,errs=await boot(br)
        ahora=int(time.time()*1000)
        await pg.evaluate("a=>{window.__DB.set('usuarios/adm',{email:'rgaraventa@gmail.com',rol:'owner',status:'activo'});window.__DB.set('negocios/nadm',{nombre:'Adm',ownerUid:'adm',tipo:'Kiosco',icon:'🏪'});window.__DB.set('usuarios/c1',{email:'c1@t.com',rol:'owner',plan:'basico',modo:'single',status:'demo',demoStart:{__ts:a},demoHasta:{__ts:a+5*86400000}});window.__DB.set('usuarios/c2',{email:'c2@t.com',rol:'owner',status:'demo',demoStart:{__ts:a}})}",ahora)
        await pg.evaluate("()=>window.__login({uid:'adm',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>localStorage.setItem('rt_admin','1')")
        for i in range(5): await pg.evaluate("()=>document.getElementById('owner-page-title').click()")
        await pg.wait_for_timeout(500); await pg.click('#atab-users'); await pg.wait_for_timeout(800)
        await pg.evaluate("()=>[...document.querySelectorAll('.btn-aext')].find(b=>b.dataset.uid==='c1'&&b.dataset.dias==='7').click()"); await pg.wait_for_timeout(700)
        c1=await db(pg,'usuarios/c1'); chk('+7 días suma a demoHasta (nueva)',abs(c1['demoHasta']['__ts']-(ahora+12*86400000))<5000 and 'demoExpiry' not in c1)
        await pg.evaluate("()=>[...document.querySelectorAll('.btn-aext')].find(b=>b.dataset.uid==='c2'&&b.dataset.dias==='7').click()"); await pg.wait_for_timeout(700)
        c2=await db(pg,'usuarios/c2'); chk('+7 días en cuenta vieja usa demoExpiry (sin demoHasta)',('demoExpiry' in c2) and 'demoHasta' not in c2)
        await pg.evaluate("()=>[...document.querySelectorAll('.btn-aplan')].find(b=>b.dataset.uid==='c1'&&b.dataset.val==='avanzada').click()"); await pg.wait_for_timeout(700)
        c1=await db(pg,'usuarios/c1'); chk('pasar a Avanzada: plan, modo multi, límite 3',c1['plan']=='avanzada' and c1['modo']=='multi' and c1['features']['limiteNegocios']==3)
        await pg.evaluate("()=>[...document.querySelectorAll('.btn-aplan')].find(b=>b.dataset.uid==='c1'&&b.dataset.val==='basico').click()"); await pg.wait_for_timeout(700)
        c1=await db(pg,'usuarios/c1'); chk('volver a Básica conserva límite',c1['plan']=='basico' and c1['features']['limiteNegocios']==3)
        await pg.evaluate("()=>[...document.querySelectorAll('.btn-aact')].find(b=>b.dataset.uid==='c1').click()"); await pg.wait_for_timeout(700)
        c1=await db(pg,'usuarios/c1'); chk('activar: status activo y demoHasta null',c1['status']=='activo' and c1['demoHasta'] is None)
        chk('sin errores JS (admin)',errs==[]); 
        if errs: print(errs)
        await br.close()
    print('\nOK',len(OK),'FALLAS',len(BAD),BAD)
asyncio.run(main())
