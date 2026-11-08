// sw-tablero.js — Service Worker del Tablero RavenTechs (red primero; la copia guardada solo si no hay conexión)
const CACHE = 'tablero-v2';
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.add('/gasar/raventechs-tablero.html').catch(() => {})));
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('tablero-') && k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).then(res => {
      if (res && res.status === 200 && new URL(e.request.url).origin === self.location.origin) {
        const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy));
      }
      return res;
    }).catch(() => caches.match(e.request).then(c => c || (e.request.mode === 'navigate' ? caches.match('/gasar/raventechs-tablero.html') : undefined)))
  );
});
