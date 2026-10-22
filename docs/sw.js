// Caché para que la web funcione sin conexión (en el metro, en el avión…).
const CACHE = "dojo-6695991026";
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
// Avisos al móvil: mensajes, regalos, solicitudes, reto de amigos y recordatorio de racha
self.addEventListener("push", e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (x) { d = { title: "Dojo", body: e.data ? e.data.text() : "" }; }
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(cs => {
    // si está mirando la web en ese momento, el chat ya lo ve en pantalla
    if (d.chat && cs.some(c => c.visibilityState === "visible" && c.focused)) return;
    return self.registration.showNotification(d.title || "Dojo", { body: d.body || "", icon: "icon-192.png", badge: "icon-192.png", tag: d.tag || "dojo", renotify: true, data: { url: d.url || "/" } });
  }));
});
self.addEventListener("notificationclick", e => {
  e.notification.close();
  const url = new URL((e.notification.data && e.notification.data.url) || "/", self.location.origin).href;
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(cs => {
    const c = cs.find(x => x.url.startsWith(self.location.origin));
    return c ? c.focus().then(w => (w || c).navigate(url)) : self.clients.openWindow(url);
  }));
});
