// Caché para que la web funcione sin conexión (en el metro, en el avión…).
const CACHE = "dojo-5584809082";
// Voces y librerías externas no cambian: van en cachés propias que sobreviven a cada versión
const VOZ = "dojo-voz-1", EXT = "dojo-ext-1";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png",
  "bank-aws.json", "bank-toefl.json", "bank-ielts.json", "bank-n5.json", "kana.json"];
const EXT_HOSTS = /^(cdn\.jsdelivr\.net|unpkg\.com|cdnjs\.cloudflare\.com|fonts\.googleapis\.com|fonts\.gstatic\.com)$/;
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== VOZ && k !== EXT).map(k => caches.delete(k)))).then(() => self.clients.claim())));
const deCache = (nombre, req, guardar) => caches.open(nombre).then(c => c.match(req).then(hit => hit || fetch(req).then(r => { if (guardar(r)) c.put(req, r.clone()).catch(() => {}); return r; })));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const u = new URL(e.request.url);
  if (u.origin !== location.origin) {
    if (EXT_HOSTS.test(u.hostname)) e.respondWith(deCache(EXT, e.request, r => r.ok || r.type === "opaque"));
    return;
  }
  if (u.pathname.startsWith("/api/")) return;   // cuentas y chat: siempre en vivo, nunca de la caché
  // Audio: caché primero; si falta, el servidor devuelve la página (HTML) y eso no se guarda
  if (u.pathname.includes("/voz/")) {
    // el reproductor pide trozos (Range): se pide y guarda el archivo entero
    e.respondWith(deCache(VOZ, new Request(u.href), r => r.status === 200 && (r.headers.get("content-type") || "").startsWith("audio")).catch(() => new Response("", { status: 404 })));
    return;
  }
  // Lo demás: red primero (contenido nuevo si hay conexión), caché si no la hay
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match("index.html"))));
});
