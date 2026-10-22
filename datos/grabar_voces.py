"""Graba gratis y en local todas las voces del Dojo:
- Japonés: 9 voces a elegir (6 de AivisSpeech, licencia ACML 1.0, y 3 de Kokoro, Apache 2.0)
  para kana, kanji, vocabulario y frases. Las frases de «matón» van siempre con Kokoro jm_kumo:
  la ACML no permite usar sus voces para insultar.
- Escucha del N5 (mujer + hombre) y del TOEFL/IELTS en acento americano y británico (Kokoro).
- Español de «Manos libres» (significados y traducciones) y portugués de Portugal con las voces
  neuronales de Microsoft Edge (motor «edge», paquete edge-tts: gratis, sin cuenta ni clave).
- Portugués de Portugal con ElevenLabs (motor «eleven»): plan gratis, sin tarjeta, 10.000 créditos
  al mes; todo el portugués son ~3.200 caracteres. La clave va en .env (ELEVENLABS_API_KEY) y
  nunca llega a la página: se graba aquí y se sirven archivos. El plan gratis pide citar a
  ElevenLabs (está en el pie de la página) y no permite uso comercial.

Necesita AivisSpeech encendido (comando `aivis`) para el motor aivis, y .venv-tts con
kokoro-onnx + misaki[ja] y modelos-tts/ para el motor kokoro (ver README de voces abajo).

Uso:  python3 datos/grabar_voces.py aivis                         (con el python normal)
      .venv-tts/bin/python datos/grabar_voces.py edge              (español y portugués)
      python3 datos/grabar_voces.py eleven [--muestra] [--voces]   (--muestra: 3 pruebas por voz)
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
    # Edge: voces adultas y tranquilas, más graves y con menos volumen (las anime asustaban)
    "nanami": ("edge", "ja-JP-NanamiNeural", "ja-JP-NanamiNeural"),
    "keita": ("edge", "ja-JP-KeitaNeural", "ja-JP-KeitaNeural"),
}
EDGE_JA = "-8%|-12Hz|-20%"
MATON = ("kokoro", "jm_kumo")
# Escucha de los exámenes: paquete → (motor, voz, idioma de Kokoro)
ESCUCHA = {
    "n5w": ("aivis", 1325133120, None), "n5m": ("kokoro", "jm_kumo", "ja"),
    "usw": ("kokoro", "af_heart", "en-us"), "usm": ("kokoro", "am_michael", "en-us"),
    "gbw": ("kokoro", "bf_emma", "en-gb"), "gbm": ("kokoro", "bm_george", "en-gb"),
}
# Español de Manos libres
ES = ("edge", "es-ES-ElviraNeural", "+0%")
PT = ("edge", "pt-PT-RaquelNeural", "-6%")
RU = ("edge", "ru-RU-SvetlanaNeural", "-8%")
# Números al oído: paquete → (idioma en kana.json, voz)
NUM = {"npt": ("pt", "pt-PT-RaquelNeural"), "nru": ("ru", "ru-RU-SvetlanaNeural"), "nja": ("ja", "ja-JP-NanamiNeural")}
# ElevenLabs: voces que suenan a Portugal (cámbialas en .env con ELEVENLABS_VOZ_PT=id1,id2…)
ELEVEN = "https://api.elevenlabs.io/v1"
ELEVEN_MODELO = "eleven_multilingual_v2"


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


def _kana():
    return json.load(open(os.path.join(WWW, "kana.json"), encoding="utf-8"))


def textos_es():
    """Lo que Manos libres dice en español: libSignif() y la traducción de la frase."""
    out = []
    for s, L in _kana().items():
        if not isinstance(L, list):  # «lecturas» y «numeros» no son listas de fichas
            continue
        for it in L:
            out.append("Se lee " + it["r"] if s in ("hira", "kata") else it.get("m", ""))
            out.append(it.get("fe", ""))
    return [t for t in dict.fromkeys(out) if t]


def textos_pt():
    """Igual que kVoice() para los conjuntos de portugués, más sus frases."""
    out = []
    d = _kana()
    for s in ("pt", "ptverbos", "falsos", "tramites"):
        for it in d[s]:
            out += [it["c"].replace(" / ", ", "), it.get("f", "")]
    out += [f["o"] for lec in d.get("lecturas", {}).get("pt", []) for f in lec["f"]]
    return [t for t in dict.fromkeys(out) if t]


def textos_ru():
    """Igual que kVoice() para el ruso (campo v en el alfabeto), más sus frases."""
    out = []
    d = _kana()
    for s in ("cirilico", "ruvocab", "rugram", "ruuni"):
        for it in d[s]:
            out += [it.get("v") or it["c"].replace(" / ", ", "), it.get("f", "")]
    out += [f["o"] for lec in d.get("lecturas", {}).get("ru", []) for f in lec["f"]]
    return [t for t in dict.fromkeys(out) if t]


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
    with tempfile.NamedTemporaryFile() as t:  # ffmpeg reconoce WAV o MP3 por el contenido
        t.write(wav_bytes); t.flush()
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", t.name, "-ac", "1", "-c:a", "aac", "-b:a", "48k", destino], check=True)


def aivis(texto, voz):
    q = urllib.request.urlopen(urllib.request.Request(
        f"{AIVIS}/audio_query?speaker={voz}&text={urllib.parse.quote(texto)}", method="POST"), timeout=60).read()
    return urllib.request.urlopen(urllib.request.Request(
        f"{AIVIS}/synthesis?speaker={voz}", data=q, headers={"Content-Type": "application/json"}, method="POST"), timeout=120).read()


def _env(clave):
    v = os.environ.get(clave)
    if v:
        return v
    ruta = os.path.join(RAIZ, ".env")
    if os.path.exists(ruta):
        for l in open(ruta, encoding="utf-8"):
            if l.startswith(clave + "="):
                return l.split("=", 1)[1].strip().strip('"')
    return ""


def _eleven_get(ruta):
    r = urllib.request.Request(ELEVEN + ruta, headers={"xi-api-key": _env("ELEVENLABS_API_KEY")})
    return json.load(urllib.request.urlopen(r, timeout=30))


def eleven_restante():
    s = _eleven_get("/user/subscription")
    return s["character_limit"] - s["character_count"]


def eleven(texto, voz):
    cuerpo = json.dumps({"text": texto, "model_id": _env("ELEVENLABS_MODELO") or ELEVEN_MODELO,
                         "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.15}}).encode()
    r = urllib.request.Request(f"{ELEVEN}/text-to-speech/{voz}?output_format=mp3_44100_128", data=cuerpo,
                               headers={"xi-api-key": _env("ELEVENLABS_API_KEY"), "Content-Type": "application/json"})
    return urllib.request.urlopen(r, timeout=120).read()


def voces_pt():
    v = [x.strip() for x in _env("ELEVENLABS_VOZ_PT").split(",") if x.strip()]
    if not v:
        sys.exit("Falta ELEVENLABS_VOZ_PT en .env. Elige con `grabar_voces.py eleven --voces` y `--muestra`.")
    return v


def main_eleven(args):
    if not _env("ELEVENLABS_API_KEY"):
        sys.exit("Falta ELEVENLABS_API_KEY en .env (cuenta gratis en elevenlabs.io → Developers → API Keys).")
    if "--voces" in args:
        for v in _eleven_get("/voices")["voices"]:
            l = v.get("labels") or {}
            print(v["voice_id"], v["name"], "·", l.get("gender", ""), l.get("accent", ""), l.get("description", ""))
        return
    if "--muestra" in args:
        dest = os.path.join(RAIZ, ".muestras-eleven"); os.makedirs(dest, exist_ok=True)
        for v in voces_pt():
            for i, t in enumerate(["Olá! Tudo bem?", "Desculpe, onde fica a estação de comboios?", "Obrigado, até amanhã!"]):
                open(os.path.join(dest, f"{v}-{i}.mp3"), "wb").write(eleven(t, v))
        print("Muestras en", dest, "· quedan", eleven_restante(), "caracteres este mes"); return
    vz = voces_pt()
    pend = [t for t in textos_pt() if not os.path.exists(os.path.join(WWW, "voz", "pt", fnv(t) + ".m4a"))]
    gasto = sum(map(len, pend)); queda = eleven_restante()
    print(f"eleven: faltan {len(pend)} audios, {gasto} caracteres; quedan {queda} este mes")
    if gasto > queda:
        print("No cabe todo: grabo lo que quepa y el resto el mes que viene (la página usa la voz del sistema)")
    fallos = []
    for n, t in enumerate(pend):
        if len(t) > queda:
            break
        try:
            a_m4a(eleven(t, vz[n % len(vz)]), os.path.join(WWW, "voz", "pt", fnv(t) + ".m4a")); queda -= len(t)
        except Exception as e:
            fallos.append(f"{t[:40]}: {e}")
            if "401" in str(e) or "quota" in str(e).lower():
                break
    print(f"eleven: hecho · quedan {queda} caracteres")
    if fallos:
        sys.exit("Fallaron:\n" + "\n".join(fallos[:20]))


def edge(texto, voz, ritmo):
    import asyncio
    import edge_tts
    async def _go():
        b = b""
        # ritmo puede ser "rate" o "rate|tono|volumen" (las voces japonesas van más graves y bajas)
        r, tono, vol = (ritmo.split("|") + ["+0Hz", "+0%"])[:3] if "|" in ritmo else (ritmo, "+0Hz", "+0%")
        async for c in edge_tts.Communicate(texto, voz, rate=r, pitch=tono, volume=vol).stream():
            if c["type"] == "audio":
                b += c["data"]
        return b
    b = asyncio.run(_go())
    if not b:
        raise RuntimeError("edge-tts no devolvió audio")
    return b


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
            tareas += [(pq, t, v_burla if burla else v_pal, EDGE_JA if m == "edge" else "ja") for t, burla in ja.items()]
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
    if ES[0] == motor:
        tareas += [("es", t, ES[1], ES[2]) for t in textos_es()]
    if PT[0] == motor:
        tareas += [("pt", t, PT[1], PT[2]) for t in textos_pt()]
    if motor == "edge":
        for pq, (idi, voz) in NUM.items():
            tareas += [(pq, x["t"], voz, "+0%") for x in _kana().get("numeros", {}).get(idi, [])]
    if RU[0] == motor:
        tareas += [("ru", t, RU[1], RU[2]) for t in textos_ru()]
    return list(dict.fromkeys(tareas))


def main():
    motor = sys.argv[1] if len(sys.argv) > 1 else ""
    if motor == "eleven":
        return main_eleven(sys.argv[2:])
    if motor not in ("aivis", "kokoro", "edge"):
        sys.exit("Uso: grabar_voces.py aivis|kokoro|edge|eleven")
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
                a_m4a(aivis(texto, voz) if motor == "aivis" else edge(texto, voz, idioma) if motor == "edge" else kokoro(texto, voz, idioma), ruta); nuevos += 1
            except Exception as e:  # sigue con el resto y avisa al final
                fallos.append(f"{pq} · {texto[:40]}: {e}")
        if n % 100 == 0:
            print(f"{motor}: {n}/{len(tareas)}", flush=True)
    print(f"{motor}: {len(tareas)} audios ({nuevos} nuevos)")
    if fallos:
        sys.exit("Fallaron:\n" + "\n".join(fallos[:20]))


if __name__ == "__main__":
    main()
