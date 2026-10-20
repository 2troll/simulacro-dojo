"""Graba con AivisSpeech (gratis, en local) todo lo que la sección de kana y palabras
pronuncia, para que en la web suene una voz japonesa de anime y no la del sistema.

Necesita AivisSpeech encendido (comando `aivis`, puerto 10101) y ffmpeg.
Uso: python3 datos/grabar_voces.py   (solo graba lo que falta; borra www/voz/ para regrabar)
Salida: www/voz/<hash>.m4a y www/voces.json {texto: archivo}
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "http://localhost:10101"

# Voces (ACML 1.0, de AivisHub): cambia el id y vuelve a grabar borrando www/voz/
PALABRA = 888753762   # まお · あまあま: kana, kanji y palabras
BURLA = 888753764     # まお · からかい: frases sarcásticas y Kansai-ben
MATON = 1310138981    # 阿井田 茂 · Shout: el matón de película


def textos():
    """Cada texto que la página manda a sayJa(), con la voz que le toca."""
    d = json.load(open(os.path.join(RAIZ, "www", "kana.json"), encoding="utf-8"))
    voz = lambda c: c.replace(" / ", "、").replace("〜", "")
    out = {}
    for k in ("hira", "kata"):
        for it in d[k]:
            out[it["c"]] = PALABRA
    for it in d["kanji"]:
        out[it["wr"]] = PALABRA
        out[it["c"]] = PALABRA  # el lienzo de dibujo pronuncia el kanji suelto
    for it in d["vocab"]:
        out[voz(it["c"])] = PALABRA
        out[it["f"]] = BURLA
    for it in d["kansai"]:
        out[voz(it["c"])] = MATON if it["g"] == "calle" else BURLA
    return out


def sintetiza(texto, voz, destino):
    q = urllib.request.urlopen(urllib.request.Request(
        f"{URL}/audio_query?speaker={voz}&text={urllib.parse.quote(texto)}", method="POST"), timeout=60).read()
    wav = urllib.request.urlopen(urllib.request.Request(
        f"{URL}/synthesis?speaker={voz}", data=q, headers={"Content-Type": "application/json"}, method="POST"), timeout=120).read()
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        t.write(wav); t.flush()
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", t.name, "-ac", "1", "-c:a", "aac", "-b:a", "48k", destino], check=True)


def main():
    try:
        urllib.request.urlopen(URL + "/version", timeout=5)
    except OSError:
        sys.exit("AivisSpeech no responde en :10101. Enciéndelo con `aivis` y repite.")
    carpeta = os.path.join(RAIZ, "www", "voz")
    os.makedirs(carpeta, exist_ok=True)
    mapa, nuevos, fallos = {}, 0, []
    todo = textos()
    for n, (texto, voz) in enumerate(todo.items(), 1):
        nombre = hashlib.sha1(f"{voz}:{texto}".encode()).hexdigest()[:14] + ".m4a"
        ruta = os.path.join(carpeta, nombre)
        if not os.path.exists(ruta):
            try:
                sintetiza(texto, voz, ruta); nuevos += 1
            except Exception as e:  # sigue con el resto y avisa al final
                fallos.append(f"{texto}: {e}"); continue
        mapa[texto] = "voz/" + nombre
        if n % 50 == 0:
            print(f"{n}/{len(todo)}", flush=True)
    # Fuera los audios que ya no usa nadie (p. ej. tras cambiar de voz)
    usados = {os.path.basename(v) for v in mapa.values()}
    for f in os.listdir(carpeta):
        if f not in usados:
            os.remove(os.path.join(carpeta, f))
    json.dump(mapa, open(os.path.join(RAIZ, "www", "voces.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"voces.json: {len(mapa)} audios ({nuevos} nuevos)")
    if fallos:
        sys.exit("Fallaron:\n" + "\n".join(fallos[:20]))


if __name__ == "__main__":
    main()
