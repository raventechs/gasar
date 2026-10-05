/* GasAR admin · Service Worker · v1.3.0-etapa4 */
const CACHE='gasar-admin-v4';
const SHELL=['./gasar-admin.html','./manifest-gasar-admin.webmanifest','./icon-gasar-192.png','./icon-gasar-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==CACHE).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);
  // Firestore/Auth van directo a la red (el SDK maneja su propio offline)
  if(u.hostname.endsWith('googleapis.com')&&!u.hostname.startsWith('fonts'))return;
  if(u.hostname==='identitytoolkit.googleapis.com'||u.hostname==='securetoken.googleapis.com')return;
  e.respondWith(
    fetch(r).then(res=>{if(res&&res.status===200){const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c))}return res})
      .catch(()=>caches.match(r).then(m=>m||(r.mode==='navigate'?caches.match('./gasar-admin.html'):undefined)))
  );
});
