const B = require('./backend.js'); const fs = require('fs');
const bk = JSON.parse(fs.readFileSync('copia-rodix-real.json', 'utf8'));
const conv = v => { if (v && typeof v === 'object') { if ('__ts' in v) return { __ts: v.__ts[0] * 1000 + Math.floor(v.__ts[1] / 1e6) }; if (Array.isArray(v)) return v.map(conv); const o = {}; for (const k of Object.keys(v)) o[k] = conv(v[k]); return o; } return v; };
const U = { ruben: ['pz9r6IT3SkUhjUgxegMFDu6fOOg1', 'rgaraventa@gmail.com'], gaston: ['elBsiV0nTAeoXNOHVM8rR0Zw5W63', 'gastonframirez1980@gmail.com'], leo: ['SG3rmLmAFzM55a38ytZG4KuMvgC2', 'leogaraventa@gmail.com'] };
const A = n => ({ uid: U[n][0], email: U[n][1] });
const res = [];
for (const secure of [false, true]) {
  B.setSecure(secure); B.store.clear(); bk.documentos.forEach(d => B.seed(d.path, conv(d.data)));
  const r = (n, f) => { const x = f(); res.push([secure, n, !x.err]); };
  const myVeh = n => [...B.store.keys()].find(k => /^vehicles\/[^/]+$/.test(k) && B.store.get(k).uid === U[n][0]);
  for (const n of ['gaston', 'ruben', 'leo']) {
    r(`${n}: lee su propio usuario`, () => B.handle(A(n), 'get', { path: 'usuarios/' + U[n][0] }));
    r(`${n}: lista sus vehículos`, () => B.handle(A(n), 'list', { path: 'vehicles', where: [['uid', '==', U[n][0]]] }));
    r(`${n}: lista sus choferes`, () => B.handle(A(n), 'list', { path: 'usuarios', where: [['flotaId', '==', U[n][0]], ['rolFlota', '==', 'chofer']] }));
    r(`${n}: crea un vehículo`, () => B.handle(A(n), 'add', { path: 'vehicles', data: { uid: U[n][0], plate: 'TEST' } }));
    r(`${n}: genera invitación`, () => B.handle(A(n), 'add', { path: 'invitaciones', data: { ownerUid: U[n][0], ownerEmail: U[n][1], rol: 'chofer', usado: false, createdAt: { __sv: true } } }));
    const v = myVeh(n);
    if (v) {
      r(`${n}: lee docs/services/insumos/revisiones de su vehículo`, () => { for (const s of ['docs', 'services', 'insumos', 'revisiones']) { const x = B.handle(A(n), 'list', { path: v + '/' + s, where: [] }); if (x.err) return x; } return { ok: 1 }; });
      r(`${n}: edita un vehículo suyo`, () => B.handle(A(n), 'update', { path: v, data: { km: 1 } }));
      const ins = [...B.store.keys()].find(k => k.startsWith(v + '/insumos/'));
      if (ins) r(`${n}: tilda un insumo`, () => B.handle(A(n), 'update', { path: ins, data: { presente: true, ultimoCambioPor: U[n][1], ultimoCambioFecha: { __sv: true } } }));
      r(`${n}: confirma revisión`, () => B.handle(A(n), 'set', { path: v + '/revisiones/2099-01-01', data: { fecha: '2099-01-01', hechoPor: U[n][1], completa: true } }));
    }
  }
  r('admin(ruben): lee vehículos de un cliente (panel admin)', () => B.handle(A('ruben'), 'list', { path: 'vehicles', where: [] }));
  r('admin(ruben): lista todos los usuarios', () => B.handle(A('ruben'), 'list', { path: 'usuarios', where: [] }));
  r('admin(ruben): cambia plan de un cliente', () => B.handle(A('ruben'), 'update', { path: 'usuarios/' + U.gaston[0], data: { features: { limiteVehiculos: 6, flotaHabilitada: true, checklistHabilitado: true } } }));
  r('admin(ruben): extiende demo (demoExpiry)', () => B.handle(A('ruben'), 'update', { path: 'usuarios/' + U.gaston[0], data: { demoExpiry: { __ts: 1 } } }));
  // chofer existente: acepta invitación sin usar
  r('nuevo chofer: crea su usuario', () => B.handle({ uid: 'NEW', email: 'nuevo@x.com' }, 'set', { path: 'usuarios/NEW', data: { uid: 'NEW', email: 'nuevo@x.com', banned: false, status: 'demo', demoStart: { __sv: true }, createdAt: { __sv: true }, flotaId: 'NEW', rolFlota: 'owner', features: { limiteVehiculos: 1 } } }));
  r('nuevo chofer: se une con invitación SIN USAR de Gastón/Ruben', () => B.handle({ uid: 'NEW', email: 'nuevo@x.com' }, 'update', { path: 'usuarios/NEW', data: { flotaId: U.ruben[0], rolFlota: 'chofer', inviteId: 'Qcyd1h9UCpLWa32fGFUW' } }));
  r('nuevo chofer: marca la invitación como usada', () => B.handle({ uid: 'NEW', email: 'nuevo@x.com' }, 'update', { path: 'invitaciones/Qcyd1h9UCpLWa32fGFUW', data: { usado: true, usadoPor: 'nuevo@x.com', usadoUid: 'NEW' } }));
  r('chofer nuevo: ve vehículos de la flota', () => B.handle({ uid: 'NEW', email: 'nuevo@x.com' }, 'list', { path: 'vehicles', where: [['uid', '==', U.ruben[0]]] }));
  r('chofer nuevo: lee el usuario del dueño (features)', () => B.handle({ uid: 'NEW', email: 'nuevo@x.com' }, 'get', { path: 'usuarios/' + U.ruben[0] }));
  // ataques con datos reales
  r('ATAQUE: Gastón lee vehículos de Ruben', () => B.handle(A('gaston'), 'list', { path: 'vehicles', where: [['uid', '==', U.ruben[0]]] }));
  r('ATAQUE: Gastón lista usuarios (emails de todos)', () => B.handle(A('gaston'), 'list', { path: 'usuarios', where: [] }));
  r('ATAQUE: Gastón se apropia flota de Leo', () => B.handle(A('gaston'), 'update', { path: 'usuarios/' + U.gaston[0], data: { flotaId: U.leo[0] } }));
  B.store.clear(); bk.documentos.forEach(d => B.seed(d.path, conv(d.data)));
  r('ATAQUE: Gastón se sube límite de vehículos', () => B.handle(A('gaston'), 'update', { path: 'usuarios/' + U.gaston[0], data: { features: { limiteVehiculos: 99, flotaHabilitada: true, checklistHabilitado: true } } }));
}
const names = [...new Set(res.map(x => x[1]))];
console.log('prueba'.padEnd(66), 'actuales  nuevas');
for (const n of names) { const a = res.find(x => !x[0] && x[1] === n)[2], b = res.find(x => x[0] && x[1] === n)[2]; const atk = n.startsWith('ATAQUE'); const flag = atk ? (b && true ? '  <<< ABIERTO' : '') : (!b ? '  <<< SE ROMPE CON REGLAS NUEVAS' : ''); console.log(n.padEnd(66), (a ? 'permite ' : 'bloquea').padEnd(9), (b ? 'permite' : 'bloquea') + flag); }
