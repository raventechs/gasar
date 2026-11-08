import re,sys
app,ver,verline,cache_file,cache_old,cache_new,nombre_app=sys.argv[1:8]
p=f'/home/claude/{app}/index.html'; s=open(p,encoding='utf8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:80],s.count(a)); s=s.replace(a,b)
# 1) estado + col()
rep("  function col(n){ if(!OWNER) throw new Error('Sin negocio activo'); return db.collection('negocios').doc(OWNER).collection(n); }",
"""  /* Sucursales (adicional): ventas, gastos, cierres y comandas son de cada sucursal; productos, insumos y configuración son del negocio (compartidos). 'principal' = la ruta de siempre, sin cambios. */
  let SUC='principal', rtSucursales=[], rtLimiteSuc=1;
  const RT_SUC_COMPARTIDAS=['productos','insumos','configuracion','recetas'];
  function col(n){ if(!OWNER) throw new Error('Sin negocio activo'); const base=db.collection('negocios').doc(OWNER);
    if(SUC && SUC!=='principal' && RT_SUC_COMPARTIDAS.indexOf(n)<0) return base.collection('sucursales').doc(SUC).collection(n);
    return base.collection(n); }""")
# 2) link de cajero con sucursal
rep("""if(q && /^[A-Za-z0-9]{10,40}$/.test(q)) localStorage.setItem('rt_negocio',q); }catch(_){}""",
"""if(q && /^[A-Za-z0-9]{10,40}$/.test(q)){ localStorage.setItem('rt_negocio',q); const sq=new URLSearchParams(location.search).get('s'); if(sq && /^[A-Za-z0-9]{10,40}$/.test(sq)) localStorage.setItem('rt_suc',sq); else localStorage.removeItem('rt_suc'); } }catch(_){}""")
# 3) dueño: cargar sucursales
rep("        rtChkPintar();\n        return true;","        await rtCargarSucursales(user);\n        rtChkPintar();\n        return true;")
# cajero: sucursal desde el link
rep("      OWNER = n;\n","      OWNER = n;\n      SUC='principal'; try{ const sq=localStorage.getItem('rt_suc'); if(sq && /^[A-Za-z0-9]{10,40}$/.test(sq)) SUC=sq; }catch(_){}\n")
# 4) funciones
js = r'''
  /* ── Sucursales: lista, cambio, alta y links de cajero. El límite lo fija el admin (usuarios/{uid}.limiteSucursales, con botones); sin campo = 1 = sin sucursales. ── */
  async function rtCargarSucursales(user){
    try{
      let lim=1; try{ const us=await db.collection('usuarios').doc(user.uid).get(); const l=us.exists?us.data().limiteSucursales:undefined; if(l>0) lim=l; }catch(_){}
      if(window.rtIsAdmin&&window.rtIsAdmin()) lim=99;
      rtLimiteSuc=lim;
      const snap=await db.collection('negocios').doc(OWNER).collection('sucursales').get();
      rtSucursales=snap.docs.map(d=>Object.assign({id:d.id},d.data()));
      let want='principal'; try{ want=localStorage.getItem('rt_suc_'+user.uid)||'principal'; }catch(_){}
      SUC=(want!=='principal'&&rtSucursales.some(x=>x.id===want))?want:'principal';
    }catch(_){ SUC='principal'; }
    rtSucPintar();
  }
  function rtSucNombre(id){ if(id==='principal') return 'Principal'; const x=rtSucursales.find(z=>z.id===id); return x?(x.nombre||'Sucursal'):'Sucursal'; }
  function rtSucPintar(){
    try{
      const bd=document.getElementById('rtSucBadge'), sec=document.getElementById('rtSucSection'), cont=document.getElementById('rtSucLista');
      const habilitada=(rtLimiteSuc>1||rtSucursales.length>0)&&rolActual==='dueño';
      if(bd){ if(habilitada&&SUC!=='principal'){ bd.style.display=''; bd.textContent='🏪 '+rtSucNombre(SUC); } else bd.style.display='none'; }
      if(!sec||!cont) return;
      sec.style.display=habilitada?'':'none'; if(!habilitada) return;
      const filas=[{id:'principal',nombre:'Principal'}].concat(rtSucursales);
      cont.innerHTML=filas.map(function(x){ const act=x.id===SUC; const nom=String(x.nombre||'Sucursal').replace(/</g,'&lt;');
        return '<div style="display:flex;align-items:center;justify-content:space-between;gap:6px;flex-wrap:wrap;border:1px solid var(--border);border-radius:12px;padding:8px 10px;margin-bottom:6px"><div style="font-weight:700">'+nom+(act?' <span style="font-size:11px;color:#27ae60">● estás acá</span>':'')+'</div><div style="display:flex;gap:6px;flex-wrap:wrap">'
          +(act?'':'<button class="btn-secondary" style="width:auto;padding:6px 12px" onclick="rtSucCambiar(\''+x.id+'\')">Entrar</button>')
          +'<button class="btn-secondary" style="width:auto;padding:6px 12px" onclick="rtSucLink(\''+x.id+'\')">📋 Link de cajero</button></div></div>'; }).join('');
      const usadas=rtSucursales.length+1, info=document.getElementById('rtSucInfo');
      if(info) info.textContent=usadas+' de '+(rtLimiteSuc>=99?'ilimitadas':rtLimiteSuc)+' sucursales';
      const nb=document.getElementById('rtSucNueva'); if(nb) nb.style.display=(usadas<rtLimiteSuc)?'':'none';
    }catch(_){}
  }
  window.rtSucCambiar=function(id){ try{ localStorage.setItem('rt_suc_'+auth.currentUser.uid,id); }catch(_){} location.reload(); };
  window.rtSucLink=function(id){
    const url=location.origin+location.pathname+'?n='+OWNER+(id==='principal'?'':'&s='+id);
    (navigator.clipboard?navigator.clipboard.writeText(url):Promise.reject()).then(()=>toast('Link copiado'),()=>{ try{ prompt('Copiá el link:',url); }catch(_){} });
  };
  window.rtSucNueva=async function(){
    if(rtSucursales.length+1>=rtLimiteSuc){ toast('Llegaste al límite de sucursales'); return; }
    const nombre=(prompt('Nombre de la sucursal:')||'').trim(); if(!nombre) return;
    try{ const ref=await db.collection('negocios').doc(OWNER).collection('sucursales').add({nombre:nombre,creadoEn:firebase.firestore.FieldValue.serverTimestamp()});
      rtSucursales.push({id:ref.id,nombre:nombre}); rtSucPintar(); toast('Sucursal creada ✅');
    }catch(e){ toast('No se pudo crear la sucursal'); }
  };
  window.rtAdmLim=async function(uid,v){ try{ await db.collection('usuarios').doc(uid).update({limiteSucursales:v}); toast('Sucursales: '+(v>=99?'sin límite':v)); rtAdmClientes(); }catch(e){ toast('No se pudo actualizar'); } };
'''
rep("  window.rtAdmSet=async function(uid,acc){", js+"  window.rtAdmSet=async function(uid,acc){")
# 5) menú admin: botones por cliente
m=re.search(r"h\+='<div style=\"border:1px solid #4443;border-radius:10px;padding:8px;margin-bottom:6px\">.*?\+'<button onclick=\"rtAdmSet\(\\''\+d\.id\+'\\',30\)\".*?</button></div>';",s,re.S)
assert m, 'bloque cliente admin no encontrado'
blk=m.group(0); assert blk.endswith("</button></div>';")
lim="(u.limiteSucursales>0?u.limiteSucursales:1)"
btns="+'<div style=\"margin-top:6px;font-size:12px\">🏪 Sucursales: '+[[1,'1'],[3,'Hasta 3'],[99,'Todas']].map(function(o){const a=("+lim+"===o[0]);return '<button onclick=\"rtAdmLim(\\''+d.id+'\\','+o[0]+')\" style=\"padding:5px 9px;margin-right:4px;border-radius:8px;border:1.5px solid '+(a?'#E03C26':'#4446')+';background:'+(a?'#E03C2622':'transparent')+';color:inherit;font-weight:'+(a?'700':'500')+'\">'+o[1]+'</button>';}).join('')+'</div></div>';"
new_blk=blk[:-len("</div>';")]+"</div>'"+btns
s=s.replace(blk,new_blk)
# 6) UI: badge y sección de config
tb=re.search(r'(<span class="topbar-title">.*?</span></span>)',s); assert tb
s=s.replace(tb.group(1),tb.group(1)+'\n      <span id="rtSucBadge" style="display:none;margin-left:8px;font-size:11px;font-weight:700;padding:3px 8px;border-radius:99px;background:rgba(37,99,235,.18);color:#60a5fa"></span>',1)
sec='''<div class="config-section" id="rtSucSection" style="display:none">
        <h4>🏪 Sucursales</h4>
        <p style="font-size:0.78rem;color:var(--muted);margin-bottom:8px">Cada sucursal tiene sus propias ventas, gastos y cierres; el menú y el stock son compartidos. Cada cajero entra con el link de su sucursal.</p>
        <div id="rtSucLista"></div>
        <p style="font-size:0.75rem;color:var(--muted);margin:6px 0" id="rtSucInfo"></p>
        <button class="btn-tomate" id="rtSucNueva" onclick="rtSucNueva()">+ Nueva sucursal</button>
      </div>
      '''
mm=re.search(r'<div class="config-section">\s*<h4>🎓 Modo Práctica</h4>',s); assert mm
s=s[:mm.start()]+sec+s[mm.start():]
# 7) versión
open(p,'w',encoding='utf8').write(s)
print('ok',app)
