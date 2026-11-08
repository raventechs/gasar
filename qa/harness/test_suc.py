import asyncio,sys
from playwright.async_api import async_playwright
APP,PORT,NOMBRE=sys.argv[1],sys.argv[2],sys.argv[3]
FAKE=open('/home/claude/tw/fake_firebase_tw.js',encoding='utf-8').read().replace('collection: n => new ColRef(n),','collection: n => new ColRef(n), enablePersistence: async()=>{},',1).replace('signOut: async','getRedirectResult: async()=>null, signOut: async',1)
res=[]
def chk(n,c,x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ')+n,x)
async def caso(br,lim,sucs=(),admin=False,suc_sel=None):
    ctx=await br.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    async def gs(r):
        if 'firebase-app-compat' in r.request.url: await r.fulfill(body=FAKE,content_type='application/javascript')
        else: await r.fulfill(body='',content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',gs); await pg.route('**/fonts.g*',lambda r:r.abort()); await pg.route('**/sw*.js',lambda r:r.abort())
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(1200)
    await pg.evaluate("""([lim,sucs,sel,admin])=>{const u={email:'p@t.com',demoHasta:null,app:'%s'}; if(lim) u.limiteSucursales=lim; window.__DB.set('usuarios/u1',u);
      sucs.forEach(([id,n])=>window.__DB.set('negocios/u1/sucursales/'+id,{nombre:n}));
      if(sel) localStorage.setItem('rt_suc_u1',sel); if(admin) localStorage.setItem('rt_admin','1');}"""%NOMBRE,[lim,[list(x) for x in sucs],suc_sel,admin])
    await pg.evaluate("()=>window.__login({uid:'u1',email:'p@t.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
    return ctx,pg,errs
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch()
        ctx,pg,e=await caso(br,None)
        r=await pg.evaluate("()=>({suc:SUC,vis:getComputedStyle(document.getElementById('rtSucSection')).display,path:col('ventas').path||col('ventas')._path||String(col('ventas').parent||'')})")
        chk('cliente sin adicional → sin sucursales, ruta de siempre',r['suc']=='principal' and r['vis']=='none',r)
        pth=await pg.evaluate("()=>{const c=col('ventas');return JSON.stringify(c._p||c.path||c.n||c)}"); print('   ruta ventas:',pth)
        chk('sin errores JS',not e,e); await ctx.close()
        ctx,pg,e=await caso(br,3)
        v=await pg.evaluate("()=>({vis:getComputedStyle(document.getElementById('rtSucSection')).display,info:document.getElementById('rtSucInfo').textContent,nueva:getComputedStyle(document.getElementById('rtSucNueva')).display})")
        chk('con adicional (hasta 3) → sección visible, 1 de 3, botón nueva',v['vis']!='none' and '1 de 3' in v['info'] and v['nueva']!='none',v)
        await pg.evaluate("()=>{window.prompt=()=>'Centro'}"); await pg.evaluate("()=>rtSucNueva()"); await pg.wait_for_timeout(500)
        k=await pg.evaluate("()=>[...window.__DB.keys()].filter(k=>k.startsWith('negocios/u1/sucursales/'))"); chk('crea la sucursal',len(k)==1,k)
        await pg.evaluate("()=>{window.prompt=()=>'Norte'}"); await pg.evaluate("()=>rtSucNueva()"); await pg.wait_for_timeout(500)
        await pg.evaluate("()=>{window.prompt=()=>'Sur'}"); await pg.evaluate("()=>rtSucNueva()"); await pg.wait_for_timeout(500)
        k=await pg.evaluate("()=>[...window.__DB.keys()].filter(k=>k.startsWith('negocios/u1/sucursales/'))"); chk('tope: con límite 3 no deja pasar de 2 sucursales + principal',len(k)==2,k)
        chk('sin errores JS',not e,e); await ctx.close()
        ctx,pg,e=await caso(br,3,[('sucA','Centro')],suc_sel='sucA')
        r=await pg.evaluate("()=>({suc:SUC,badge:document.getElementById('rtSucBadge').textContent,vis:getComputedStyle(document.getElementById('rtSucBadge')).display})")
        chk('entra a la sucursal elegida y muestra la etiqueta',r['suc']=='sucA' and 'Centro' in r['badge'] and r['vis']!='none',r)
        ok=await pg.evaluate("""async()=>{await col('ventas').add({total:111,x:1}); await col('productos').doc('p9').set({nombre:'Muzza'},{merge:true});
          const keys=[...window.__DB.keys()]; return {suc:keys.some(k=>k.startsWith('negocios/u1/sucursales/sucA/ventas/')),prin:keys.some(k=>k.startsWith('negocios/u1/ventas/')),prod:keys.includes('negocios/u1/productos/p9')}}""")
        chk('ventas van a la sucursal, producto queda compartido en el principal',ok['suc'] and not ok['prin'] and ok['prod'],ok)
        await pg.evaluate("()=>{localStorage.setItem('rt_suc_u1','principal')}")
        await ctx.close()
        ctx,pg,e=await caso(br,None,[('sucA','Centro')],suc_sel='sucA')
        r=await pg.evaluate("()=>({suc:SUC,vis:getComputedStyle(document.getElementById('rtSucSection')).display})")
        chk('con sucursales ya creadas y límite 1 → sigue viéndolas (no pierde acceso)',r['suc']=='sucA' and r['vis']!='none',r); await ctx.close()
        # admin: botones por cliente
        ctx,pg,e=await caso(br,None,admin=True)
        await pg.evaluate("()=>{window.__DB.set('usuarios/c2',{email:'c2@x.com',app:'%s',demoHasta:null})}"%NOMBRE)
        await pg.evaluate("()=>rtAdmClientes()"); await pg.wait_for_timeout(500)
        h=await pg.evaluate("document.getElementById('rtAdmClientes').innerText"); chk('menú admin: botones de Sucursales por cliente','Sucursales' in h and 'Hasta 3' in h and 'Todas' in h)
        await pg.evaluate("()=>rtAdmLim('c2',3)"); await pg.wait_for_timeout(300)
        d=await pg.evaluate("()=>window.__DB.get('usuarios/c2')"); chk('botón guarda limiteSucursales=3 sin tocar demoHasta',d['limiteSucursales']==3 and d['demoHasta'] is None,d)
        chk('sin errores JS',not e,e); await ctx.close(); await br.close()
    print(f'{sum(res)}/{len(res)}')
asyncio.run(main())
