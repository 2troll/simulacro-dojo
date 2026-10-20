"""Graba gratis y en local todas las voces del Dojo:
- Japonés: 9 voces a elegir (6 de AivisSpeech, licencia ACML 1.0, y 3 de Kokoro, Apache 2.0)
  para kana, kanji, vocabulario y frases. Las frases de «matón» van siempre con Kokoro jm_kumo:
  la ACML no permite usar sus voces para insultar.
- Escucha del N5 (mujer + hombre) y del TOEFL/IELTS en acento americano y británico (Kokoro).

Necesita AivisSpeech encendido (comando `aivis`) para el motor aivis, y .venv-tts con
kokoro-onnx + misaki[ja] y modelos-tts/ para el motor kokoro (ver README de voces abajo).

Uso:  python3 datos/grabar_voces.py aivis                         (con el python normal)
      .venv-tts/bin/python datos/grabar_voces.py kokoro            (en paralelo, otra terminal)
Solo graba lo que falta. Salida: www/voz/<paquete>/<fnv>.m4a — el nombre es el hash FNV-1a del
texto, el mismo que calcula hashStr() en la página, así no hace falta índice.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WWW = os.path.join(RAIZ, "www")
AIVIS = "http://localhost:10101"

# paquete: (motor, voz para palabras, voz para frases con burla). Debe coincidir con VOZ_JA en index.html
VOCES_JA = {
    "mao": ("aivis", 888753762, 888753764),       # まお · あまあま / からかい
    "kohaku": ("aivis", 1878365377, 1878365376),  # コハク · あまあま / ノーマル
    "runa": ("aivis", 345585728, 345585728),      # るな
    "sakurane": ("aivis", 376644064, 376644064),  # 桜音
    "kanon": ("aivis", 1325133120, 1325133120),   # 花音
    "eru": ("aivis", 1388823427, 1388823424),     # 凛音エル · Happy / ノーマル
    "alpha": ("kokoro", "jf_alpha", "jf_alpha"),
    "nezumi": ("kokoro", "jf_nezumi", "jf_nezumi"),
    "kumo": ("kokoro", "jm_kumo", "jm_kumo"),     # voz de chico
}
MATON = ("kokoro", "jm_kumo")
# Escucha de los exámenes: paquete → (motor, voz, idioma de Kokoro)
ESCUCHA = {
    "n5w": ("aivis", 1325133120, None), "n5m": ("kokoro", "jm_kumo", "ja"),
    "usw": ("kokoro", "af_heart", "en-us"), "usm": ("kokoro", "am_michael", "en-us"),
    "gbw": ("kokoro", "bf_emma", "en-gb"), "gbm": ("kokoro", "bm_george", "en-gb"),
}


def fnv(texto):
    """Igual que hashStr() de la página (FNV-1a de 32 bits sobre unidades UTF-16)."""
    x = 2166136261
    for ch in texto:
        o = ord(ch)
        x ^= (0xD800 + ((o - 0x10000) >> 10)) if o > 0xFFFF else o
        x = (x * 16777619) & 0xFFFFFFFF
    return format(x, "08x")


def voz_de(c):
    return c.replace(" / ", "、").replace("〜", "")


def textos_ja():
    """(texto, ¿es frase con burla?) de todo lo que pronuncia la sección de kana y palabras."""
    d = json.load(open(os.path.join(WWW, "kana.json"), encoding="utf-8"))
    out, maton = {}, set()
    for k in ("hira", "kata"):
        for it in d[k]:
            out[it["c"]] = False
    for it in d["kanji"]:
        out[it["wr"]] = False
        out[it["c"]] = False
    for it in d["vocab"]:
        out[voz_de(it["c"])] = False
        out[it["f"]] = True
    out["こんにちは！いっしょに がんばろうね。"] = False  # el botón «Probar» del selector de voz
    for it in d["kansai"]:
        if it["g"] == "calle":
            maton.add(voz_de(it["c"]))
        else:
            out[voz_de(it["c"])] = True
    return out, maton


def lineas(examen):
    """Las líneas de escucha tal como las corta speak() en la página: (texto, 'W'|'M')."""
    out = {}
    for s in json.load(open(os.path.join(WWW, f"bank-{examen}.json"), encoding="utf-8")):
        for l in re.split(r"\n+", s.get("audio") or ""):
            l = l.strip()
            if not l:
                continue
            m = re.match(r"^(M|W|男|女)\s*[:：]\s*(.*)$", l)
            g, t = ("M" if m.group(1) in ("M", "男") else "W", m.group(2)) if m else ("W", l)
            out[t] = g
    if examen != "n5":  # el botón «Probar» del inglés
        out.update({"Hi! Shall we practise together?": "W", "Sure, let's go.": "M"})
    return out


def a_m4a(wav_bytes, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        t.write(wav_bytes); t.flush()
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", t.name, "-ac", "1", "-c:a", "aac", "-b:a", "48k", destino], check=True)


def aivis(texto, voz):
    q = urllib.request.urlopen(urllib.request.Request(
        f"{AIVIS}/audio_query?speaker={voz}&text={urllib.parse.quote(texto)}", method="POST"), timeout=60).read()
    return urllib.request.urlopen(urllib.request.Request(
        f"{AIVIS}/synthesis?speaker={voz}", data=q, headers={"Content-Type": "application/json"}, method="POST"), timeout=120).read()


_kk = _g2p = None


def kokoro(texto, voz, idioma):
    global _kk, _g2p
    import io
    import soundfile as sf
    from kokoro_onnx import Kokoro
    if _kk is None:
        _kk = Kokoro(os.path.join(RAIZ, "modelos-tts", "kokoro-v1.0.onnx"), os.path.join(RAIZ, "modelos-tts", "voices-v1.0.bin"))
    if idioma == "ja":
        if _g2p is None:
            from misaki import ja
            _g2p = ja.JAG2P()
        ph = _g2p(texto)
        audio, sr = _kk.create(ph[0] if isinstance(ph, tuple) else ph, voice=voz, is_phonemes=True)
    else:
        audio, sr = _kk.create(texto, voice=voz, lang=idioma)
    b = io.BytesIO(); sf.write(b, audio, sr, format="WAV")
    return b.getvalue()


def trabajos(motor):
    """Lista de (paquete, texto, voz, idioma) que le tocan a este motor."""
    ja, maton = textos_ja()
    tareas = []
    for pq, (m, v_pal, v_burla) in VOCES_JA.items():
        if m == motor:
            tareas += [(pq, t, v_burla if burla else v_pal, "ja") for t, burla in ja.items()]
    if MATON[0] == motor:
        tareas += [("maton", t, MATON[1], "ja") for t in maton]
    for ex, (w, mm) in (("n5", ("n5w", "n5m")), ("toefl", ("usw", "usm")), ("ielts", ("gbw", "gbm"))):
        for t, g in lineas(ex).items():
            pares = [(w, mm)] if ex == "n5" else [("usw", "usm"), ("gbw", "gbm")]  # inglés en los dos acentos
            for pw, pm in pares:
                pq = pw if g == "W" else pm
                m, v, idi = ESCUCHA[pq]
                if m == motor:
                    tareas.append((pq, t, v, idi or "ja"))
    return list(dict.fromkeys(tareas))


def main():
    motor = sys.argv[1] if len(sys.argv) > 1 else ""
    if motor not in ("aivis", "kokoro"):
        sys.exit("Uso: grabar_voces.py aivis|kokoro")
    if motor == "aivis":
        try:
            urllib.request.urlopen(AIVIS + "/version", timeout=5)
        except OSError:
            sys.exit("AivisSpeech no responde en :10101. Enciéndelo con `aivis` y repite.")
    tareas = trabajos(motor)
    vistos, fallos, nuevos = {}, [], 0
    for n, (pq, texto, voz, idioma) in enumerate(tareas, 1):
        h = fnv(texto)
        if vistos.setdefault((pq, h), texto) != texto:
            fallos.append(f"colisión de hash en {pq}: {texto} / {vistos[(pq, h)]}"); continue
        ruta = os.path.join(WWW, "voz", pq, h + ".m4a")
        if not os.path.exists(ruta):
            try:
                a_m4a(aivis(texto, voz) if motor == "aivis" else kokoro(texto, voz, idioma), ruta); nuevos += 1
            except Exception as e:  # sigue con el resto y avisa al final
                fallos.append(f"{pq} · {texto[:40]}: {e}")
        if n % 100 == 0:
            print(f"{motor}: {n}/{len(tareas)}", flush=True)
    print(f"{motor}: {len(tareas)} audios ({nuevos} nuevos)")
    if fallos:
        sys.exit("Fallaron:\n" + "\n".join(fallos[:20]))


if __name__ == "__main__":
    main()
