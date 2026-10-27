const { chromium } = require('playwright'); const { newCtx, B } = require('./harness');
const SECURE = process.argv[2] === 'seguro';
require('./backend.js').setSecure(SECURE);
const FILE = SECURE ? 'file:///tmp/claude-0/-home-claude/eff33411-7c17-5966-8a6f-7369f80c69a4/scratchpad/e2e/rodix-parcheada.html' : 'file:///home/claude/ref/vehigest-ar/index.html';
const findIns=id=>{const k=[...B.store.keys()].find(k=>k.endsWith('/insumos/'+id));return k?B.store.get(k):undefined};
const vehOf=id=>{const k=[...B.store.keys()].find(k=>k.endsWith('/insumos/'+id));return k?k.split('/insumos/')[0]:null};
const R = []; const ok = (n, c, x) => { R.push([c ? 'OK   ' : 'FALLA', n, x || '']); };
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const br = await chromium.launch();
  const errs = [];
  const open = async (url) => { const c = await newCtx(br); const p = await c.newPage(); p.on('pageerror', e => errs.push(e.message + ' @ ' + String(e.stack).split('\n').slice(1,3).join(' ').slice(0,200))); p.on('dialog', d => d.accept()); await p.goto(url); await sleep(500); return { c, p }; };

  // 1) Dueño se registra
  let { c: c1, p: dueno } = await open(FILE);
  await dueno.click('#toggle-auth'); await dueno.fill('#login-email', 'dueno@ambu.com'); await dueno.fill('#login-pass', 'secreto123'); await dueno.click('#btn-login'); await sleep(1500);
  const uD = B.store.get('usuarios/uid_dueno'); 
  ok('registro crea usuario con flotaId propio y rol owner', uD && uD.flotaId === 'uid_dueno' && uD.rolFlota === 'owner' && uD.status === 'demo', JSON.stringify(uD && { s: uD.status, f: uD.features }));
  ok('entra a la app (pantalla principal visible)', await dueno.isVisible('#app-screen'));

  // 2) El admin habilita flota + checklist y sube el límite (lo que hace el panel admin)
  B.store.get('usuarios/uid_dueno').features = { limiteVehiculos: 10, flotaHabilitada: true, checklistHabilitado: true };
  B.store.get('usuarios/uid_dueno').status = 'activo';
  await dueno.reload(); await sleep(1500);
  ok('aparece botón "Mi equipo" al habilitar flota', await dueno.isVisible('#btn-equipo-sidebar'));

  // 3) Modo práctica
  await dueno.click('.nav-item[data-page="ajustes"]'); await sleep(300);
  await dueno.click('text=Cargar datos de práctica'); await sleep(3500);
  const vs = [...B.store.keys()].filter(k => /^vehicles\/[^/]+$/.test(k));
  const amb = vs.filter(k => [...B.store.keys()].some(x => x.startsWith(k + '/insumos/')));
  ok('práctica crea 5 vehículos', vs.length === 5, 'vehículos=' + vs.length);
  const insAmb = amb.length ? [...B.store.keys()].filter(k => k.startsWith(amb[0] + '/insumos/')).length : 0;
  ok('ambulancia recibe checklist de insumos', amb.length >= 1 && insAmb > 0, 'ambulancias=' + amb.length + ' insumos=' + insAmb);

  // 4) Vista del vehículo ambulancia y pestaña insumos
  await dueno.click('.nav-item[data-page="vehicles"]'); await sleep(800);
  const cards = await dueno.$$('#page-vehicles .vehicle-card:not(.add-card)');
  ok('lista de vehículos muestra 5 tarjetas', cards.length === 5, 'tarjetas=' + cards.length);
  const ambCard = await dueno.$('.vehicle-card:has-text("Ambulancia")'); 
  if (ambCard) { await ambCard.click(); await sleep(800); await dueno.click('#tab-insumos'); await sleep(600); }
  const chk = await dueno.$$('[data-insumo-id]');
  ok('pestaña Insumos lista los ítems', chk.length > 0, 'ítems=' + chk.length);
  if (chk.length) {
    const antes = [...B.store.entries()].filter(([k]) => k.startsWith(amb[0] + '/insumos/'));
    const primero = chk[0]; const wasChecked = await primero.isChecked(); await primero.click(); await sleep(800);
    const id = await primero.getAttribute('data-insumo-id');
    ok('tildar/destildar insumo se guarda', (findIns(id)||{}).presente === !wasChecked);
    await dueno.click('#btn-confirmar-revision').catch(() => {}); await sleep(800);
    const rev = [...B.store.keys()].filter(k => k.startsWith(vehOf(id) + '/revisiones/'));
    ok('confirmar revisión diaria crea registro', rev.length === 1, 'revisiones=' + rev.length);
  }
  // alertas de insumos
  await dueno.click('.nav-item[data-page="alerts"]'); await sleep(600);
  ok('Alertas muestra bloque Insumos', /Insumos/.test(await dueno.innerText('#page-alerts')));

  // 5) Invitación de chofer
  await dueno.click('#btn-equipo-sidebar'); await sleep(500);
  await dueno.click('#btn-gen-invite'); await sleep(1000);
  const invKeys = [...B.store.keys()].filter(k => k.startsWith('invitaciones/'));
  ok('generar link crea invitación sin usar', invKeys.length === 1 && B.store.get(invKeys[0]).usado === false && B.store.get(invKeys[0]).ownerUid === 'uid_dueno');
  const linkTxt = (await dueno.innerText('#invite-link-box')) + ' ' + (await dueno.$$eval('#invite-link-box input', i => i.map(x => x.value).join(' '))); const m = linkTxt.match(/\?invite=([A-Za-z0-9_-]+)/);
  ok('el link contiene el id de invitación', !!m && m[1] === invKeys[0].split('/')[1], linkTxt.slice(0, 120));

  [...B.store.keys()].filter(k => k.includes('/revisiones/')).forEach(k => B.store.delete(k));
  // 6) Chofer abre el link, se registra y entra
  const inviteUrl = FILE + '?invite=' + invKeys[0].split('/')[1];
  let { c: c2, p: chofer } = await open(inviteUrl);
  await chofer.click('#toggle-auth'); await chofer.fill('#login-email', 'chofer@ambu.com'); await chofer.fill('#login-pass', 'chofer1234'); await chofer.click('#btn-login'); await sleep(2500);
  const uC = B.store.get('usuarios/uid_chofer');
  ok('chofer queda con rolFlota=chofer y flotaId=dueño', uC && uC.rolFlota === 'chofer' && uC.flotaId === 'uid_dueno', JSON.stringify(uC && { r: uC.rolFlota, f: uC.flotaId }));
  ok('invitación queda marcada como usada', B.store.get(invKeys[0]).usado === true && B.store.get(invKeys[0]).usadoPor === 'chofer@ambu.com');
  ok('chofer entra a la app', await chofer.isVisible('#app-screen'));
  ok('chofer NO ve botón Mi equipo', !(await chofer.isVisible('#btn-equipo-sidebar')));
  await chofer.click('.nav-item[data-page="vehicles"]'); await sleep(1000);
  const cc = await chofer.$$('#page-vehicles .vehicle-card:not(.add-card)');
  ok('chofer ve los vehículos de la flota', cc.length === 5, 'tarjetas=' + cc.length);
  ok('chofer NO ve botón agregar vehículo', (await chofer.$$('#btn-add-vehicle-card')).length === 0);
  const cAmb = await chofer.$('.vehicle-card:has-text("Ambulancia")'); if (cAmb) { await cAmb.click(); await sleep(900); }
  const cChk = await chofer.$$('[data-insumo-id]');
  ok('chofer ve el checklist de insumos de la ambulancia', cChk.length > 0, 'ítems=' + cChk.length);
  ok('chofer NO ve botones de editar vehículo/documentos', (await chofer.$$('#btn-edit-vehicle,#btn-add-doc')).length === 0);
  if (cChk.length) {
    const was = await cChk[1].isChecked(); await cChk[1].click(); await sleep(900);
    const id = await cChk[1].getAttribute('data-insumo-id');
    ok('chofer puede tildar insumos', (findIns(id)||{}).presente === !was);
    const rb = await chofer.$('#btn-confirmar-revision'); if (rb && !(await rb.isDisabled())) { await rb.click(); await sleep(900); }
    const rv = [...B.store.entries()].filter(([k]) => k.startsWith(vehOf(id) + '/revisiones/'));
    ok('chofer confirma la revisión (queda su email)', rv.some(([, v]) => v.hechoPor === 'chofer@ambu.com'), 'revisiones=' + rv.map(([, v]) => v.hechoPor).join(','));
  }
  // chofer: dashboard solo insumos
  await chofer.click('.nav-item[data-page="dashboard"]'); await sleep(600);
  const dtxt = await chofer.innerText('#page-dashboard');
  ok('chofer en Inicio ve solo Insumos (no Documentos/Services)', /Insumos/.test(dtxt) && !/Seguro|VTV|Licencia/i.test(dtxt), dtxt.slice(0, 100).replace(/\n/g, ' '));

  // 7) Reuso del link
  let { c: c3, p: otro } = await open(inviteUrl);
  await otro.click('#toggle-auth'); await otro.fill('#login-email', 'otro@x.com'); await otro.fill('#login-pass', 'otro123456'); await otro.click('#btn-login'); await sleep(2500);
  const uO = B.store.get('usuarios/uid_otro');
  ok('link usado no suma a un segundo chofer', uO && uO.rolFlota === 'owner' && uO.flotaId === 'uid_otro', JSON.stringify(uO && { r: uO.rolFlota, f: uO.flotaId }));

  // 8) Dueño quita al chofer
  await dueno.reload(); await sleep(1200); await dueno.click('#btn-equipo-sidebar'); await sleep(1000);
  const rm = await dueno.$('[data-remove-chofer]'); ok('dueño ve al chofer en su equipo', !!rm);
  if (rm) { await rm.click(); await sleep(1000); const uC2 = B.store.get('usuarios/uid_chofer'); ok('quitar chofer lo devuelve a owner de su propia flota', uC2.rolFlota === 'owner' && uC2.flotaId === 'uid_chofer', JSON.stringify({ r: uC2.rolFlota, f: uC2.flotaId })); }

  // 9) Seguridad (reglas): ataques desde un usuario cualquiera
  const H = require('./backend.js');
  const att = H.handle({ uid: 'uid_otro', email: 'otro@x.com' }, 'list', { path: 'usuarios', where: [] });
  ok('SEGURIDAD: usuario común NO debería poder listar todos los usuarios (emails/uids)', !!att.err, att.docs ? 'lista ' + att.docs.length + ' usuarios con emails' : '');
  const hij = H.handle({ uid: 'uid_otro', email: 'otro@x.com' }, 'update', { path: 'usuarios/uid_otro', data: { flotaId: 'uid_dueno', rolFlota: 'owner' } });
  const vv = H.handle({ uid: 'uid_otro', email: 'otro@x.com' }, 'list', { path: 'vehicles', where: [['uid', '==', 'uid_dueno']] });
  ok('SEGURIDAD: usuario común NO debería poder apropiarse de otra flota sin invitación', !!hij.err || !!vv.err, 'update=' + (hij.err || 'PERMITIDO') + ' | lectura vehículos ajenos=' + (vv.err || (vv.docs ? 'PERMITIDA (' + vv.docs.length + ')' : '')));
  const esc = H.handle({ uid: 'uid_chofer2', email: 'c2@x.com' }, 'op', {});
  console.log('\n=== RODIX E2E ' + (SECURE ? '(reglas endurecidas + app parcheada)' : '(reglas actuales)') + ' ==='); R.forEach(r => console.log(r.join(' | ')));
  const f = R.filter(r => r[0].startsWith('FALLA')).length; console.log(f ? `>>> ${f} FALLA(S) de ${R.length}` : '>>> TODO OK ' + R.length);
  console.log('errores JS en página:', [...new Set(errs)].slice(0, 6));
  await br.close();
})().catch(e => { console.error('EXC', e); process.exit(2); });
