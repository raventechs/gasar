const { chromium } = require('playwright'); const { newCtx, B } = require('./harness');
B.setSecure(true);
const FILE = 'file:///home/claude/vehigest-ar/index.html'; const sleep = ms => new Promise(r => setTimeout(r, ms));
const R = []; const ok = (n, c, x) => R.push([c ? 'OK   ' : 'FALLA', n, x || '']);
(async () => {
  const br = await chromium.launch(); const errs = [];
  const open = async (url) => { const c = await newCtx(br, FILE, { viewport: { width: 390, height: 780 }, isMobile: true, hasTouch: true }); const p = await c.newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept()); await p.goto(url); await sleep(700); return p; };
  const d = await open(FILE);
  await d.click('#toggle-auth'); await d.fill('#login-email', 'dueno@x.com'); await d.fill('#login-pass', 'secreto123'); await d.click('#btn-login'); await sleep(1500);
  B.store.get('usuarios/uid_dueno').features = { limiteVehiculos: 10, flotaHabilitada: true, checklistHabilitado: true }; B.store.get('usuarios/uid_dueno').status = 'activo';
  await d.reload(); await sleep(1500);
  await d.click('#topbar-avatar'); await sleep(200);
  ok('menú móvil muestra «Ajustes y backup» al dueño', await d.isVisible('#btn-ajustes-mob'));
  await d.click('#btn-ajustes-mob'); await sleep(500);
  ok('abre la página Ajustes', await d.isVisible('#page-ajustes'));
  ok('Ajustes muestra Modo Práctica y Backup', /Modo Práctica/.test(await d.innerText('#page-ajustes')) && /Backup de datos/.test(await d.innerText('#page-ajustes')));
  ok('título superior dice Ajustes', (await d.innerText('#topbar-title')).trim() === 'Ajustes');
  ok('el menú se cierra al elegir', !(await d.isVisible('#btn-ajustes-mob')));
  ok('ya no hay error de currentUser', !errs.some(e => /currentUser/.test(e)), errs.join('|'));
  // botón práctica usable desde el celular
  await d.click('button[onclick="cargarPractica()"]'); await sleep(3500);
  ok('práctica se puede cargar desde el celular', [...B.store.keys()].filter(k => /^vehicles\/[^/]+$/.test(k)).length === 5);
  // volver a navegar normal
  await d.click('.mob-nav-item[data-page="vehicles"]'); await sleep(700);
  ok('volver a Vehículos funciona', await d.isVisible('#page-vehicles') || (await d.$$('.vehicle-card')).length > 0);
  // banner instalar
  await d.evaluate(() => { window.__prompted = 0; const e = new Event('beforeinstallprompt'); e.prompt = () => { window.__prompted++; }; e.userChoice = Promise.resolve({ outcome: 'accepted' }); window.dispatchEvent(e); });
  await sleep(2500);
  ok('banner de instalación aparece cuando el navegador lo permite', await d.isVisible('#bannerPWA'));
  await d.click('#bannerPWA button:has-text("Instalar")'); await sleep(400);
  ok('«Instalar» dispara el aviso del navegador', (await d.evaluate(() => window.__prompted)) === 1);
  ok('el banner se oculta tras tocar Instalar', !(await d.isVisible('#bannerPWA')));
  // chofer: no ve Ajustes
  B.store.get('usuarios/uid_dueno'); const inv = await d.evaluate(() => null);
  await d.click('#topbar-avatar'); await d.click('#btn-equipo-mob'); await sleep(500); await d.click('#btn-gen-invite'); await sleep(900);
  const id = [...B.store.keys()].find(k => k.startsWith('invitaciones/')).split('/')[1];
  const c = await open(FILE + '?invite=' + id);
  await c.click('#toggle-auth'); await c.fill('#login-email', 'chofer@x.com'); await c.fill('#login-pass', 'clave12345'); await c.click('#btn-login'); await sleep(2500);
  await c.click('#topbar-avatar'); await sleep(200);
  ok('chofer NO ve «Ajustes y backup» en su menú', !(await c.isVisible('#btn-ajustes-mob')));
  console.log('\n=== RODIX v1.9.3 ==='); R.forEach(r => console.log(r.join(' | ')));
  const f = R.filter(r => r[0].startsWith('FALLA')).length; console.log(f ? `>>> ${f} FALLA(S)` : '>>> TODO OK ' + R.length);
  await br.close();
})().catch(e => { console.error('EXC', e.message); process.exit(2); });
