const B = require('./backend.js');
function setup(secure){ B.setSecure(secure); B.store.clear();
 B.seed('usuarios/D',{uid:'D',email:'d@x',status:'activo',banned:false,flotaId:'D',rolFlota:'owner',features:{limiteVehiculos:1,flotaHabilitada:true}});
 B.seed('usuarios/C',{uid:'C',email:'c@x',status:'activo',banned:false,flotaId:'D',rolFlota:'chofer',features:{}});
 B.seed('usuarios/X',{uid:'X',email:'x@x',status:'demo',banned:false,flotaId:'X',rolFlota:'owner',features:{limiteVehiculos:1}});
 B.seed('vehicles/v1',{uid:'D',brand:'a'}); B.seed('invitaciones/I1',{ownerUid:'D',usado:false});
 B.seed('invitaciones/I2',{ownerUid:'D',usado:true,usadoUid:'C'}); }
const A=(u,e)=>({uid:u,email:e||u+'@x'});
const tests=[
 ['cliente lista usuarios ajenos',a=>B.handle(A('X'),'list',{path:'usuarios',where:[]})],
 ['cliente se asigna la flota de otro (sin invitación)',a=>B.handle(A('X'),'update',{path:'usuarios/X',data:{flotaId:'D',rolFlota:'owner'}})],
 ['cliente extiende su demo (status=activo)',a=>B.handle(A('X'),'update',{path:'usuarios/X',data:{status:'activo'}})],
 ['cliente se sube el límite de vehículos',a=>B.handle(A('X'),'update',{path:'usuarios/X',data:{features:{limiteVehiculos:999}}})],
 ['chofer se hace owner (escala permisos)',a=>B.handle(A('C'),'update',{path:'usuarios/C',data:{rolFlota:'owner'}})],
 ['cliente usa invitación YA usada',a=>B.handle(A('X'),'update',{path:'usuarios/X',data:{flotaId:'D',rolFlota:'chofer',inviteId:'I2'}})],
 ['cliente re-abre invitación usada (usado=false)',a=>B.handle(A('X'),'update',{path:'invitaciones/I2',data:{usado:false}})],
 ['cliente cambia dueño de una invitación',a=>B.handle(A('X'),'update',{path:'invitaciones/I1',data:{ownerUid:'X'}})],
 ['cliente edita vehículo ajeno',a=>B.handle(A('X'),'update',{path:'vehicles/v1',data:{brand:'z'}})],
];
const out=[];
for(const sec of [false,true]){ for(const [n,f] of tests){ setup(sec); const r=f(); const bloqueado=!!r.err; out.push([sec,n,bloqueado]); } }
console.log('ataque'.padEnd(58),'reglas actuales','reglas nuevas');
for(const [n] of tests){ const a=out.find(o=>!o[0]&&o[1]===n)[2], b=out.find(o=>o[0]&&o[1]===n)[2]; console.log(n.padEnd(58),(a?'bloqueado ':'PERMITIDO ').padEnd(16),b?'bloqueado':'PERMITIDO'); }
