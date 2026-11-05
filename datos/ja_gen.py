"""Funde en www/kana.json el japonés práctico y por niveles:
ja_supervivencia.json (primeros pasos, comprar, comer, moverse), ja_gram45.json (gramática N5/N4)
y ja_alto.py (gramática N3-N1, palabras N4/N3). Calcula «r» (romaji) y valida antes de escribir."""
import json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from vocab_gen import romaji  # noqa: E402
import ja_alto  # noqa: E402

ORDEN = ["jaempieza", "jacompra", "jacomer", "jamover", "jagram5", "jagram4", "javocab4", "jagram3", "javocab3", "jagram2", "jagram1"]
CAMPOS = ("c", "m", "f", "fe", "g")


def cargar():
    sets = {}
    for nombre in ("ja_supervivencia.json", "ja_gram45.json"):
        sets.update(json.load(open(os.path.join(AQUI, nombre), encoding="utf-8")))
    gram = lambda L: [dict(c=c, k="", m=m, f=f, fe=fe, t=t, g=g) for (c, m, f, fe, t, g) in L]
    voc = lambda L: [dict(c=c, k=k, m=m, f=f, fe=fe, g=g) for (c, k, m, f, fe, g) in L]
    sets.update(jagram3=gram(ja_alto.GRAM3), jagram2=gram(ja_alto.GRAM2), jagram1=gram(ja_alto.GRAM1),
                javocab4=voc(ja_alto.VOC4), javocab3=voc(ja_alto.VOC3))
    return sets


def preparar(sets, ya):
    """Valida y calcula romaji. «ya» = lecturas que ya están en vocab N5: se quitan de los niveles altos."""
    vistos, fuera = set(), []
    for s in ORDEN:
        assert s in sets, f"falta el conjunto {s}"
        limpio = []
        for it in sets[s]:
            for k in CAMPOS:
                assert it.get(k), f"{s}: falta «{k}» en {it}"
            assert not re.search(r"[a-zA-Z]", it["f"]), f"{s}: romaji en la frase: {it['f']}"
            clave = it["c"].replace(" ", "")
            if clave in vistos or (s.startswith("javocab") and clave in ya):
                fuera.append(f"{s}:{it['c']}")
                continue
            vistos.add(clave)
            it["r"] = romaji(it["c"].replace("〜", " ").strip()).replace("  ", " ")
            limpio.append(it)
        assert len(limpio) >= 15, f"{s}: solo {len(limpio)} fichas"
        sets[s] = limpio
    return fuera


def main():
    ruta = os.path.join(RAIZ, "www", "kana.json")
    datos = json.load(open(ruta, encoding="utf-8"))
    ya = {i["c"].replace(" ", "") for i in datos["vocab"]}
    sets = cargar()
    fuera = preparar(sets, ya)
    for s in ORDEN:
        datos[s] = sets[s]
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    print(" · ".join(f"{s} {len(sets[s])}" for s in ORDEN), f"= {sum(len(sets[s]) for s in ORDEN)} fichas")
    if fuera:
        print("Quitadas por repetidas:", ", ".join(fuera))


if __name__ == "__main__":
    main()
