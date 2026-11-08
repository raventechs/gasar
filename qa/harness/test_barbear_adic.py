import asyncio
exec(open('/home/claude/tw/test_barbear.py').read().split('TXT=')[0])
async def run(br,lim,activos):
    ctx,pg,e=await caso(br,'null')
    await pg.evaluate("""([lim,n])=>{const c=window.__DB.get('clientes/l@t.com'); if(lim!==null)c.limiteBarberos=lim; window.__DB.set('clientes/l@t.com',c);
      for(let i=0;i<n;i++) window.__DB.set('negocios/u1/barberos/b'+i,{nombre:'B'+i,activo:true});}""",[lim,activos])
    return ctx,pg,e
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        # cliente nuevo con limite 1 y 1 barbero activo -> bloquea y ofrece WhatsApp
        ctx,pg,e=await caso(br,'null')
        await pg.evaluate("""()=>{const c=window.__DB.get('clientes/l@t.com'); c.limiteBarberos=1; window.__DB.set('clientes/l@t.com',c); window.__DB.set('negocios/u1/barberos/b0',{nombre:'B0',activo:true});}""")
        await pg.reload(); await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>window.__login({uid:'u1',email:'l@t.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        r=await pg.evaluate("""async()=>{window.__conf=0;window.__opens=[];window.__prompt=0;window.confirm=()=>{window.__conf++;return true};window.open=u=>{window.__opens.push(u)};window.prompt=()=>{window.__prompt++;return 'Nuevo'};
          await agregarBarbero(); return {conf:window.__conf,wa:window.__opens[0]||'',prompt:window.__prompt,lim:limiteBarberos}}""")
        chk('limite 1 con 1 barbero activo → bloquea y ofrece WhatsApp',r['conf']==1 and 'wa.me/5491136547592' in r['wa'] and r['prompt']==0 and r['lim']==1,r)
        await ctx.close()
        ctx,pg,e=await caso(br,'null')
        await pg.evaluate("""()=>{window.__DB.set('negocios/u1/barberos/b0',{nombre:'B0',activo:true});window.__DB.set('negocios/u1/barberos/b1',{nombre:'B1',activo:true})}""")
        r=await pg.evaluate("""async()=>{window.__prompt=0;window.confirm=()=>true;window.prompt=()=>{window.__prompt++;return 'Otro'};await agregarBarbero();return {prompt:window.__prompt,lim:String(limiteBarberos)}}""")
        chk('cliente existente (sin campo) con 2 barberos → sin límite, deja agregar',r['prompt']==1 and r['lim']=='Infinity',r)
        n=await pg.evaluate("()=>[...window.__DB.keys()].filter(k=>k.startsWith('negocios/u1/barberos/')).length"); chk('se guardó el nuevo y no se borró ninguno',n>=3 and await pg.evaluate("[...window.__DB.entries()].some(([k,v])=>k.startsWith('negocios/u1/barberos/')&&v.nombre==='Otro')")&&await pg.evaluate("window.__DB.has('negocios/u1/barberos/b0')&&window.__DB.has('negocios/u1/barberos/b1')"),n)
        chk('sin errores JS',not e,e); await ctx.close()
        # admin: botones y setLimiteCliente
        ctx,pg,e=await caso(br,'null')
        await pg.evaluate("""()=>{window.__DB.set('clientes/c1@x.com',{email:'c1@x.com',nombre:'Cli',plan:'basico',activo:true,features:{},limiteSucursales:1,creadoEn:firebase.firestore.Timestamp.now()});document.body.insertAdjacentHTML('beforeend','<div id="misClientesList"></div>')}""")
        await pg.evaluate("()=>cargarMisClientes()"); await pg.wait_for_timeout(500)
        h=await pg.evaluate("document.getElementById('misClientesList').innerText")
        chk('admin muestra ADICIONALES con Sucursales y Barberos','ADICIONALES' in h and 'Sucursales' in h and 'Barberos' in h and 'Hasta 3' in h and 'Escáner' not in h)
        await pg.evaluate("()=>setLimiteCliente('c1@x.com','limiteBarberos',3)"); await pg.wait_for_timeout(300)
        v=await pg.evaluate("window.__DB.get('clientes/c1@x.com').limiteBarberos"); chk('botón guarda limiteBarberos=3 sin tocar lo demás',v==3 and await pg.evaluate("window.__DB.get('clientes/c1@x.com').limiteSucursales")==1)
        await pg.evaluate("()=>cambiarPlan('c1@x.com','pro')"); await pg.wait_for_timeout(300)
        chk('cambiar plan no pisa sucursales',await pg.evaluate("window.__DB.get('clientes/c1@x.com').limiteSucursales")==1)
        await ctx.close(); await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
