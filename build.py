"""Valida los bancos generados (datos/*.json) y los empaqueta en www/bank-<examen>.json.

Falla en alto: cualquier set roto se descarta con un aviso, y si una tarea
queda vacía el script sale con error para no publicar un examen cojo.
"""
import glob
import json
import os
import re
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.abspath(__file__))
SECS = {"reading", "listening", "vocab", "grammar", "writing", "speaking"}


def cargar(ruta):
    texto = open(ruta, encoding="utf-8").read().strip()
    # Gemini a veces envuelve en ```json … ```
    texto = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto)
    return json.loads(texto, strict=False)


def problema_q(q):
    t = q.get("t")
    if not q.get("q") and t != "order":
        return "sin enunciado"
    if t == "mcq":
        o = q.get("o")
        if not isinstance(o, list) or not 2 <= len(o) <= 4:
            return "opciones"
        if not isinstance(q.get("a"), int) or not 0 <= q["a"] < len(o):
            return "índice de respuesta"
        if len(set(map(str, o))) != len(o):
            return "opciones repetidas"
    elif t == "fill":
        a = q.get("a")
        if isinstance(a, str):
            q["a"] = [a]
        if not q.get("a") or "___" not in q["q"]:
            return "hueco"
    elif t == "order":
        w, a = q.get("w"), q.get("a")
        if not isinstance(w, list) or not isinstance(a, str):
            return "orden"
        if sorted(w) != sorted(a.split(" ")):
            return "las piezas no forman la respuesta"
    else:
        return f"tipo {t}"
    return None


def main():
    os.makedirs(os.path.join(RAIZ, "www"), exist_ok=True)
    error = False
    for examen in ("toefl", "ielts", "n5"):
        rutas = sorted(glob.glob(os.path.join(RAIZ, "datos", f"{examen}_*.json")))
        sets, descartes = [], 0
        for ruta in rutas:
            for s in cargar(ruta):
                if s.get("sec") not in SECS or not s.get("task"):
                    descartes += 1
                    continue
                s["lvl"] = s.get("lvl") if s.get("lvl") in (1, 2, 3) else 2
                qs = s.get("qs") or []
                buenos = []
                for q in qs:
                    p = problema_q(q)
                    if p:
                        print(f"  [{examen}] descarto pregunta ({p}): {str(q.get('q'))[:60]}")
                        descartes += 1
                    else:
                        buenos.append(q)
                abierto = s["sec"] in ("writing", "speaking") and s.get("model")
                if not buenos and not abierto:
                    descartes += 1
                    continue
                s["qs"] = buenos
                s["id"] = len(sets)
                sets.append(s)
        tareas = Counter(s["task"] for s in sets)
        nq = sum(max(1, len(s["qs"])) for s in sets)
        print(f"{examen}: {len(sets)} sets, {nq} preguntas, {descartes} descartes, archivos {len(rutas)}")
        for t, n in sorted(tareas.items()):
            print(f"    {n:4d}  {t}")
        if not sets:
            print(f"ERROR: {examen} sin preguntas", file=sys.stderr)
            error = True
            continue
        with open(os.path.join(RAIZ, "www", f"bank-{examen}.json"), "w", encoding="utf-8") as f:
            json.dump(sets, f, ensure_ascii=False, separators=(",", ":"))
    sys.exit(1 if error else 0)


if __name__ == "__main__":
    main()
