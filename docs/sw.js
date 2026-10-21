// Caché para que la web funcione sin conexión (en el metro, en el avión…).
const CACHE = "dojo-3969267051";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png",
  "bank-aws.json", "bank-toefl.json", "bank-ielts.json", "bank-n5.json", "kana.json"];
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
// Red primero (contenido nuevo si hay conexión), caché si no la hay
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match("index.html"))));
});
