import asyncio, json, time
from playwright.async_api import async_playwright
FAKE = open('/home/claude/tw/fake_firebase_tw.js', encoding='utf-8').read().replace('signOut: async', 'getRedirectResult: async()=>null, signOut: async', 1).replace('initializeApp() {}', 'initializeApp() { return {}; }')
BASE = 'http://127.0.0.1:8768/'
res = []
DAY = 86400000


def chk(n, c, x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ') + n, x)


async def nueva(br, pagina, seed=''):
    ctx = await br.new_context(viewport={'width': 390, 'height': 844}); pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: print('CON', m.text[:700]) if 'STACK' in m.text else None)
    pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))

    async def gs(r):
        if 'firebase-app-compat' in r.request.url:
            await r.fulfill(body=FAKE, content_type='application/javascript')
        else:
            await r.fulfill(body='', content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**', gs)
    await pg.route('**/fonts.g*', lambda r: r.abort())
    await pg.route('**/sw.js', lambda r: r.abort())
    await pg.route('**/unpkg.com/**', lambda r: r.fulfill(body='', content_type='application/javascript'))
    if seed: await pg.add_init_script('window.__DB=new Map();'+seed)
    await pg.goto(BASE + pagina); await pg.wait_for_timeout(900)
    return ctx, pg, errs


async def empresa(br, e1):
    seed = ("const P='tenants/garrafas-agua';__DB.set(P,{nombre:'Garrafas',slug:'garrafas-agua'});"
            "__DB.set(P+'/empresas/e1',Object.assign({nombre:'Gas Uno',activa:true,plan:'basico'},"+json.dumps(e1)+"));"
            "__DB.set(P+'/usuarios/u1',{rol:'empresa',empresaId:'e1',email:'emp@test.com'});")
    ctx, pg, errs = await nueva(br, 'empresa.html', seed)
    await pg.evaluate("()=>window.__login({uid:'u1',email:'emp@test.com',emailVerified:true})"); await pg.wait_for_timeout(2200)
    d = await pg.evaluate("""()=>{const b=document.getElementById('barPrueba');const r=b?b.getBoundingClientRect():null;
     return {bar:!!b,cls:b?b.className:'',txt:b?b.textContent:'',pos:b?getComputedStyle(b).position:'',anim:b?getComputedStyle(b).animationName:'',inview:r?(r.bottom<=innerHeight&&r.top>0):false,
     wa:b&&b.querySelector('a')?b.querySelector('a').href:'',cerrar:b?!!b.querySelector('button'):false,panel:getComputedStyle(document.getElementById('panel')).display!=='none'}}""")
    await ctx.close(); return d, errs


async def main():
    now = int(time.time() * 1000)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        d, e = await empresa(br, {'demoHasta': now - 2 * DAY})
        chk('empresa vencida: panel abierto + cartel rojo titilante fijo', d['panel'] and d['bar'] and 'venc' in d['cls'] and d['pos'] == 'fixed' and d['anim'] != 'none' and d['inview'], d)
        chk('sin cerrar, con WhatsApp', 'Terminó tu prueba' in d['txt'] and not d['cerrar'] and 'wa.me/5491136547592' in d['wa'])
        chk('sin errores JS', not e, e)
        d, e = await empresa(br, {'demoHasta': now + 6 * DAY + 3600000})
        chk('en curso: ámbar con días', d['panel'] and d['bar'] and 'curso' in d['cls'] and '7 días' in d['txt'], d['txt'])
        d, e = await empresa(br, {})
        chk('empresa sin demoHasta (existente): sin cartel', d['panel'] and not d['bar'])
        d, e = await empresa(br, {'demoHasta': None})
        chk('empresa activada (null): sin cartel', d['panel'] and not d['bar'])
        seed = ("const P='tenants/garrafas-agua';__DB.set(P,{nombre:'Garrafas',slug:'garrafas-agua'});"
                "__DB.set(P+'/empresas/e1',{nombre:'Vencida',activa:true,demoHasta:%d});__DB.set(P+'/empresas/e2',{nombre:'Nueva',activa:true});"
                "__DB.set(P+'/empresas/e3',{nombre:'Real',activa:true,demoHasta:null});__DB.set(P+'/empresas/e4',{nombre:'EnCurso',activa:true,demoHasta:%d});" % (now - DAY, now + 4 * DAY))
        ctx, pg, errs = await nueva(br, 'admin.html', seed)
        await pg.evaluate("()=>window.__login({uid:'adm',email:'rgaraventa@gmail.com',emailVerified:true})"); await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>{const b=document.querySelector('[data-tab=tEmpresas],[data-tab=empresas]');if(b)b.click()}"); await pg.wait_for_timeout(800)
        txt = await pg.evaluate("document.getElementById('listaEmpresas').innerText")
        chk('admin: etiquetas PRUEBA VENCIDA / PRUEBA · 4 d', 'PRUEBA VENCIDA' in txt and 'PRUEBA · 4 d' in txt, txt.replace('\n', ' | ')[:250])
        cnt = await pg.evaluate("({ini:document.querySelectorAll('[data-prueba=iniciar]').length,act:document.querySelectorAll('[data-prueba=activar]').length,mas:document.querySelectorAll('[data-prueba=mas]').length})")
        chk('admin: Iniciar solo en la que no tiene (1), Activar y +7 solo en las 2 en prueba', cnt == {'ini': 1, 'act': 2, 'mas': 2}, cnt)
        await pg.evaluate("()=>document.querySelector('[data-prueba=iniciar]').click()"); await pg.wait_for_timeout(600)
        await pg.evaluate("()=>document.querySelector('[data-prueba=activar][data-pe=e1]').click()"); await pg.wait_for_timeout(600)
        db = await pg.evaluate("()=>['e1','e2','e3','e4'].map(k=>{const v=window.__DB.get('tenants/garrafas-agua/empresas/'+k);return [k,v.demoHasta===null?'null':(v.demoHasta?Math.round((v.demoHasta-Date.now())/86400000):'-')]})")
        chk('admin: iniciar=14 días, activar=null, el resto intacto', db == [['e1', 'null'], ['e2', 14], ['e3', 'null'], ['e4', 4]], db)
        chk('admin: sin errores JS', not errs, errs)
        await br.close()
    print(f'{sum(res)}/{len(res)}')

asyncio.run(main())
