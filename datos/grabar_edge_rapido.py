"""Graba el motor edge de grabar_voces.py con 8 hilos: 2 minutos en vez de una hora.
Uso: .venv-tts/bin/python datos/grabar_edge_rapido.py"""
import os, sys, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grabar_voces as g
t = [x for x in g.trabajos("edge") if not os.path.exists(os.path.join(g.WWW, "voz", x[0], g.fnv(x[1]) + ".m4a"))]
print("faltan", len(t), flush=True)
def uno(x):
    pq, texto, voz, ritmo = x
    for intento in range(3):
        try:
            g.a_m4a(g.edge(texto, voz, ritmo), os.path.join(g.WWW, "voz", pq, g.fnv(texto) + ".m4a")); return None
        except Exception as e:
            err = e
    return f"{pq} {texto[:30]}: {err}"
with cf.ThreadPoolExecutor(8) as ex:
    fallos = [f for f in ex.map(uno, t) if f]
print("hecho; fallos:", len(fallos), *fallos[:5], sep="\n")
