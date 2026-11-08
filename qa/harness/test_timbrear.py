import asyncio, json, time
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8769/'
DAY = 86400000
res = []

APP = "export const initializeApp = () => ({});"
FS = """
export const getFirestore = () => ({});
export const doc = (db, ...p) => ({ path: p.join('/') });
export const getDoc = async (r) => { const d = window.__DB[r.path]; return { exists: () => !!d, data: () => d }; };
export const collection = () => ({});
export const query = () => ({});
export const where = () => ({});
export const orderBy = () => ({});
export const onSnapshot = (q, cb) => { try { cb({ docs: [], forEach: () => {}, exists: () => false, data: () => ({}) }); } catch (e) {} return () => {}; };
export const addDoc = async () => ({}); export const getDocs = async () => ({ forEach: () => {} });
export const updateDoc = async () => ({});
export const serverTimestamp = () => Date.now();
"""
AUTH = """
const u = { uid: 'anon1' };
export const getAuth = () => ({ currentUser: u, onAuthStateChanged: (cb) => { cb(u); return () => {}; } });
export const signInAnonymously = async () => u;
export const setPersistence = async () => {};
export const browserLocalPersistence = {};
"""
MSG = "export const getMessaging = () => ({}); export const getToken = async () => null; export const onMessage = () => {};"
STO = "export const getStorage = () => ({}); export const ref = () => ({}); export const uploadBytes = async () => ({}); export const getDownloadURL = async () => '';"


def chk(n, c, x=''):
    res.append(bool(c)); print(('OK    ' if c else 'FALLA ') + n, x)


async def residente(br, edif):
    ctx = await br.new_context(viewport={'width': 390, 'height': 844}); pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)+' @ '+str(getattr(e,'stack','')[:300])))

    async def gs(r):
        u = r.request.url
        body = APP if 'firebase-app.js' in u else FS if 'firestore' in u else AUTH if 'firebase-auth' in u else MSG if 'messaging' in u else STO if 'storage' in u else ''
        await r.fulfill(body=body, content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**', gs)
    await pg.route('**/fonts.g*', lambda r: r.abort())
    await pg.route('**/*sw*.js', lambda r: r.abort())
    await pg.add_init_script("window.__DB=" + json.dumps({'edificios/ed1': edif}) + ";")
    await pg.goto(BASE + 'timbrear-residente.html?edificio=ed1&depto=2B&nombre=Ana&edificioNombre=Torre'); await pg.wait_for_timeout(1500)
    d = await pg.evaluate("""()=>{const b=document.getElementById('barPrueba');const r=b?b.getBoundingClientRect():null;
      return {bar:!!b,cls:b?b.className:'',txt:b?b.textContent:'',pos:b?getComputedStyle(b).position:'',anim:b?getComputedStyle(b).animationName:'',
      inview:r?(r.bottom<=innerHeight&&r.top>0):false,wa:b&&b.querySelector('a')?b.querySelector('a').href:'',cerrar:b?!!b.querySelector('button'):false,
      pantalla:!!document.querySelector('.screen.active')}}""")
    await ctx.close(); return d, errs


async def main():
    now = int(time.time() * 1000)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        d, e = await residente(br, {'nombre': 'Torre Norte', 'demoHasta': now - 2 * DAY})
        chk('edificio vencido: app abierta + cartel rojo titilante fijo', d['pantalla'] and d['bar'] and 'venc' in d['cls'] and d['pos'] == 'fixed' and d['anim'] != 'none' and d['inview'], d)
        chk('sin cerrar, con WhatsApp y nombre del edificio', 'Terminó la prueba' in d['txt'] and not d['cerrar'] and 'wa.me/5491136547592' in d['wa'] and 'Torre%20Norte' in d['wa'])
        chk('sin errores JS', not e, e)
        d, e = await residente(br, {'nombre': 'Torre Norte', 'demoHasta': now + 5 * DAY - 3600000})
        chk('en curso: ámbar con días', d['bar'] and 'curso' in d['cls'] and '5 días' in d['txt'], d['txt'])
        d, e = await residente(br, {'nombre': 'Torre Norte'})
        chk('edificio actual sin demoHasta: sin cartel', not d['bar'] and d['pantalla'])
        d, e = await residente(br, {'nombre': 'Torre Norte', 'demoHasta': None})
        chk('edificio activado (null): sin cartel', not d['bar'])
        await br.close()
    print(f'{sum(res)}/{len(res)}')

asyncio.run(main())
