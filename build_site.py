"""Genera docs/ para GitHub Pages: la misma página que el artifact, pero autónoma
(doctype, viewport, manifiesto e iconos) para usarla en el móvil como app.

Uso: python3 build.py && python3 build_site.py
"""
import json
import math
import os
import shutil
import struct
import zlib

RAIZ = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(RAIZ, "www")
DOCS = os.path.join(RAIZ, "docs")

HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Simulacros gratis de AWS Solutions Architect, TOEFL, IELTS y JLPT N5.">
<meta name="theme-color" content="#f6f7fb" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#11141f" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Dojo">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icon-180.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""

# Solo fuera de claude.ai: el visor de artifacts no admite service workers
SW_REG = """<script>
if("serviceWorker" in navigator && location.hostname.endsWith("github.io")){
  navigator.serviceWorker.register("sw.js").catch(function(e){console.warn("Sin modo offline:",e)});
}
</script>
"""

SW = """// Caché para que la web funcione sin conexión (en el metro, en el avión…).
const CACHE = "dojo-%s";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png",
  "bank-aws.json", "bank-toefl.json", "bank-ielts.json", "bank-n5.json"];
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
// Red primero (contenido nuevo si hay conexión), caché si no la hay
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match("index.html"))));
});
"""


def png(size, path):
    """Icono: la burbuja marcada de la hoja de respuestas, en PNG puro (sin Pillow)."""
    bg, ink, dot = (246, 247, 251), (27, 35, 64), (184, 92, 0)
    c = size / 2
    ring_out, ring_in, dot_r = size * 0.36, size * 0.30, size * 0.20
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            # 4 muestras por píxel para suavizar los bordes
            acc = [0, 0, 0]
            for sx, sy in ((.25, .25), (.75, .25), (.25, .75), (.75, .75)):
                d = math.hypot(x + sx - c, y + sy - c)
                col = dot if d <= dot_r else ink if ring_in <= d <= ring_out else bg
                for i in range(3):
                    acc[i] += col[i]
            row += bytes(v // 4 for v in acc)
        rows.append(bytes(row))
    raw = zlib.compress(b"".join(rows), 9)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
                + chunk(b"IDAT", raw) + chunk(b"IEND", b""))


def main():
    os.makedirs(DOCS, exist_ok=True)
    pagina = open(os.path.join(WWW, "index.html"), encoding="utf-8").read()
    # La página del artifact ya trae su <meta charset>; aquí lo pone la cabecera
    pagina = pagina.replace('<meta charset="utf-8">\n', "", 1)
    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(HEAD + pagina + "\n" + SW_REG + "</body>\n</html>\n")
    bancos = sorted(n for n in os.listdir(WWW) if n.startswith("bank-"))
    if len(bancos) != 4:
        raise SystemExit(f"Faltan bancos en www/: {bancos}. Ejecuta antes build.py")
    for n in bancos:
        shutil.copy(os.path.join(WWW, n), DOCS)
    version = str(abs(hash(tuple(os.path.getmtime(os.path.join(WWW, n)) for n in bancos + ["index.html"]))))[:10]
    open(os.path.join(DOCS, "sw.js"), "w").write(SW % version)
    json.dump({"name": "Simulacro Dojo", "short_name": "Dojo", "lang": "es", "start_url": "./", "scope": "./",
               "display": "standalone", "background_color": "#f6f7fb", "theme_color": "#b85c00",
               "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                         {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
              open(os.path.join(DOCS, "manifest.webmanifest"), "w"), ensure_ascii=False)
    for s in (180, 192, 512):
        png(s, os.path.join(DOCS, f"icon-{s}.png"))
    open(os.path.join(DOCS, ".nojekyll"), "w").close()
    print("docs/ listo:", sorted(os.listdir(DOCS)))


if __name__ == "__main__":
    main()
