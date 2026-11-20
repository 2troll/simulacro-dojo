"""Revisión de los bancos de las olimpiadas de Rusia 2027 (mat, ingb2, rusa1).

Comprueba la estructura (una sola respuesta por pregunta, opciones distintas,
explicación presente), que no haya caracteres del alfabeto prohibido ni temas no
halal, y saca N preguntas al azar de cada banco para revisarlas a ojo.

Uso: python3 datos/revisar_olimpiadas.py [N]      (N = muestras por banco, por defecto 10)
"""
import json
import os
import random
import re
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
BANCOS = ("mat", "ingb2", "rusa1")
# Bloques Unicode prohibidos por las normas del operador (se construyen con chr para no escribirlos)
PROHIBIDO_ALFABETO = re.compile("[" + chr(0x0590) + "-" + chr(0x05FF) + chr(0xFB1D) + "-" + chr(0xFB4F) + "]")
# Palabras que delatarían temas no halal (alcohol, cerdo, apuestas, intereses/préstamos)
PROHIBIDAS = re.compile(r"\b(alcohol\w*|wine|beer|vodka|whisk(?:e)?y|pub|bars?|pork|bacon|ham|sausage|casino|gambl\w*|bet(?:s|ting)?|lotter\w*|"
                        r"interest rate|loans?|mortgage|credit card|riba|cerdo|vino|cerveza|apuesta\w*|préstamo\w*|"
                        r"пиво|вино|водк\w*|свинин\w*|казино|кредит\w*)\b", re.I)


def textos(s):
    yield s.get("passage", "")
    yield s.get("audio", "")
    for q in s["qs"]:
        yield q["q"]
        yield q["e"]
        yield from map(str, q["o"])


def revisar(examen, n):
    sets = json.load(open(os.path.join(AQUI, f"{examen}_a.json"), encoding="utf-8"))
    errores, pos, nq = [], Counter(), 0
    for s in sets:
        for q in s["qs"]:
            nq += 1
            o, a = q["o"], q["a"]
            if q["t"] != "mcq" or not 2 <= len(o) <= 4 or len(set(o)) != len(o):
                errores.append(f"opciones mal: {q['q'][:60]}")
            if not isinstance(a, int) or not 0 <= a < len(o):
                errores.append(f"índice de respuesta mal: {q['q'][:60]}")
            if len(q.get("e", "")) < 15:
                errores.append(f"explicación corta o vacía: {q['q'][:60]}")
            if len(o) == 4:
                pos[a] += 1
        for t in textos(s):
            if PROHIBIDO_ALFABETO.search(t):
                errores.append(f"alfabeto prohibido en: {t[:60]}")
            m = PROHIBIDAS.search(t)
            if m:
                errores.append(f"palabra a revisar «{m.group(0)}» en: {t[:70]}")
    print(f"\n=== {examen}: {len(sets)} sets, {nq} preguntas · posición de la correcta (4 opciones): {dict(sorted(pos.items()))}")
    for e in errores:
        print("  ERROR", e)
    rnd = random.Random()
    planas = [(s, q) for s in sets for q in s["qs"]]
    for s, q in rnd.sample(planas, min(n, len(planas))):
        ctx = " [con texto]" if s.get("passage") else " [con audio]" if s.get("audio") else ""
        print(f"\n· [{s['task']} · nivel {s['lvl']}]{ctx} {q['q']}")
        for i, op in enumerate(q["o"]):
            print(f"    {'✔' if i == q['a'] else ' '} {chr(65 + i)}) {op}")
        print("    →", q["e"].replace("\n", "\n      "))
    return not errores


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    ok = all([revisar(x, n) for x in BANCOS])
    print("\nRESULTADO:", "todo correcto" if ok else "HAY ERRORES")
    sys.exit(0 if ok else 1)
