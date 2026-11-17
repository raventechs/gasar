/* GasAR portal de entrada · Service Worker · v1.0.0 */
const CACHE='gasar-portal-v3';
const SHELL=['./','./index.html','./manifest-gasar.webmanifest','./icon-gasar-192.png','./icon-gasar-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('gasar-portal')&&x!==CACHE).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);
  // Firebase/Google van directo a la red (el SDK maneja su propio offline)
  if(u.hostname.endsWith('googleapis.com')&&!u.hostname.startsWith('fonts'))return;
  if(u.hostname.endsWith('firebaseapp.com')||u.hostname.endsWith('firebaseio.com'))return;
  e.respondWith(
    fetch(r).then(res=>{if(res&&res.status===200&&u.origin===location.origin){const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c))}return res})
      .catch(()=>caches.match(r).then(m=>m||(r.mode==='navigate'&&/\/gasar\/(index\.html)?$/.test(u.pathname)?caches.match('./index.html'):undefined)))
  );
});
