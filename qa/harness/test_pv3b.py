import asyncio,sys,time,datetime
sys.path.insert(0,'/home/claude/gasar/qa/harness')
from fake_modular import install
from playwright.async_api import async_playwright
OK=[];BAD=[]
def chk(n,c):
    (OK if c else BAD).append(n); print(('✓ ' if c else '✗ ')+n)
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(); ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:asyncio.ensure_future(d.accept()))
        await pg.add_init_script("(()=>{const st=window.setTimeout;window.setTimeout=(f,t,...a)=>String(f).includes('reload')?0:st(f,t,...a)})()"); await install(pg); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
        await pg.goto('http://127.0.0.1:8777/index.html'); await pg.wait_for_timeout(800)
        hoy=datetime.date.today().isoformat(); now=int(time.time()*1000)
        # cuenta anterior con Plus Morosidad: 1 cliente de cuotas + 1 de fiado, más un negocio
        await pg.evaluate("""([hoy,now])=>{const D=window.__DB;
          D.set('usuarios/v1',{uid:'v1',email:'v@g.com',rol:'owner',modo:'single',status:'activo',banned:false,features:{morosidad:true,limiteNegocios:1}});
          D.set('negocios/nv',{nombre:'Kiosco',ownerUid:'v1',tipo:'Kiosco',icon:'🏪'});
          D.set('clientes/cu1',{ownerUid:'v1',negocioId:'nv',nombre:'Cliente Cuotas',telefono:'1',montoCuota:1000,frecuencia:'mensual',cuotas:[{id:'c1',fecha:hoy,monto:1000,estado:'pendiente'}],createdAt:{__ts:now-5000}});
          D.set('clientes/cc1',{tipo:'cc',ownerUid:'v1',negocioId:'nv',nombre:'Cliente Fiado',telefono:'2',saldo:2500,createdAt:{__ts:now-1000}});}""",[hoy,now])
        await pg.evaluate("()=>window.__login({uid:'v1',email:'v@g.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=clientes]').click()"); await pg.wait_for_timeout(500)
        t=await pg.evaluate("()=>document.getElementById('page-clientes').innerText")
        chk('Clientes (cuotas) muestra el de cuotas',('Cliente Cuotas' in t))
        chk('Clientes (cuotas) NO mezcla al de fiado',('Cliente Fiado' not in t))
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=fiado]').click()"); await pg.wait_for_timeout(500)
        t=await pg.evaluate("()=>document.getElementById('page-fiado').innerText")
        chk('Fiado muestra al de fiado y su saldo',('Cliente Fiado' in t and '2.500' in t))
        chk('Fiado NO mezcla al de cuotas',('Cliente Cuotas' not in t))
        tt=await pg.evaluate("()=>[document.querySelector('#owner-page-title .tt-main').textContent,document.querySelector('#owner-page-title .tt-sub').textContent]")
        chk('barra: nombre del negocio grande y PuntoVenta chico',tt[0].endswith('Kiosco') and tt[1].startswith('PuntoVenta') and 'Dashboard' not in tt[0]+tt[1])
        # libretita: nota con fecha y hora en la ficha
        await pg.evaluate("()=>document.querySelector('[data-cc=cc1]').click()"); await pg.wait_for_timeout(500)
        await pg.evaluate("()=>document.getElementById('fd-b-nota').click()")
        await pg.fill('#fd-n-txt','Paga el viernes'); await pg.evaluate("()=>document.getElementById('fd-n-ok').click()"); await pg.wait_for_timeout(1200)
        nt=await pg.evaluate("()=>window.__DB.get('clientes/cc1').notas")
        chk('nota guardada con fecha y hora',bool(nt) and nt[0]['t']=='Paga el viernes' and len(nt[0]['f'])==10 and ':' in nt[0]['h'])
        chk('la ficha muestra la nota',await pg.evaluate("()=>document.getElementById('modal-fiado-body').innerText.includes('Paga el viernes')"))
        chk('saldo intacto tras la nota',await pg.evaluate("()=>window.__DB.get('clientes/cc1').saldo")==2500)
        await pg.evaluate("()=>document.getElementById('modal-fiado').classList.remove('open')")
        # dashboard: tarjeta Me deben
        await pg.evaluate("()=>document.querySelector('.mob-item[data-page=dashboard]').click()"); await pg.wait_for_timeout(500)
        chk('dashboard: Me deben $2.500',await pg.evaluate("()=>document.getElementById('page-dashboard').innerText.includes('2.500')"))
        # práctica
        await pg.evaluate("()=>document.getElementById('btn-config-owner-mob')&&0"); 
        await pg.evaluate("()=>window.cargarPractica()"); await pg.wait_for_timeout(2000)
        db=await pg.evaluate("()=>[...window.__DB.entries()].filter(([k,v])=>v&&v._demo===true).map(([k,v])=>k.split('/')[0])")
        chk('práctica crea ventas, gastos y 3 clientes de fiado',db.count('clientes')==3 and db.count('ventas')>20 and db.count('gastos')==4)
        cc=await pg.evaluate("()=>[...window.__DB.entries()].filter(([k,v])=>k.startsWith('clientes/')&&v._demo).map(([k,v])=>[k,v.saldo])")
        ventasFiado=await pg.evaluate("()=>[...window.__DB.values()].filter(v=>v.medio==='fiado'&&v._demo)")
        saldoOk=all(sum(x['importe'] for x in ventasFiado if x['clienteId']==k.split('/')[1])==s for k,s in cc)
        chk('práctica: saldos coinciden con sus fiados',saldoOk and len(cc)==3)
        await pg.evaluate("()=>window.quitarPractica()"); await pg.wait_for_timeout(2000)
        left=await pg.evaluate("()=>[...window.__DB.entries()].filter(([k,v])=>v&&v._demo===true).length")
        chk('quitar práctica borra solo lo marcado',left==0)
        real=await pg.evaluate("()=>[!!window.__DB.get('clientes/cu1'),!!window.__DB.get('clientes/cc1'),window.__DB.get('clientes/cc1').saldo]")
        chk('datos reales intactos (cuotas, fiado y saldo 2500)',real==[True,True,2500])
        chk('sin errores JS',errs==[]); 
        if errs: print(errs)
        await br.close()
    print('OK',len(OK),'FALLAS',BAD)
asyncio.run(main())
