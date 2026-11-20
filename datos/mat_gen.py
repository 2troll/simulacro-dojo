"""Matemáticas en inglés para las olimpiadas de Rusia 2027 (HSE test 1 y Financiera · Economics).

Genera datos/mat_a.json. Cada pregunta trae sus opciones con un VALOR y un juez
`ok(valor)` que recalcula la respuesta por otro camino (fuerza bruta, raíces
numéricas, coordenadas…). El script falla en alto si alguna pregunta no tiene
exactamente una opción correcta o si la correcta no es la marcada.

Estilo tomado de la prueba HSE International Olympiad 2024 (11.º) y de las
recomendaciones oficiales de la Financiera (8 problemas, 90 min).

Uso: python3 datos/mat_gen.py
"""
import itertools
import json
import math
import os
import random
import re
from fractions import Fraction as Fr

AQUI = os.path.dirname(os.path.abspath(__file__))
TASK = {
    "algebra": "Algebra: equations and inequalities",
    "funcs": "Functions and graphs",
    "logs": "Exponents and logarithms",
    "seqs": "Sequences",
    "trig": "Trigonometry",
    "geom": "Plane geometry",
    "prob": "Combinatorics and probability",
    "words": "Word problems",
}
PROBS = []
PI, R3 = math.pi, math.sqrt(3)


def P(sec, lvl, q, opts, e, ok):
    """opts: lista de (texto, valor); la PRIMERA es la correcta."""
    PROBS.append(dict(sec=sec, lvl=lvl, q=q, opts=opts, e=e, ok=ok))


# ---------- jueces y utilidades de comprobación ----------
def near(x, tol=1e-9):
    return lambda v: abs(float(v) - float(x)) < tol


def raices(f, a, b, n=400000):
    """Raíces reales de f en [a, b]: cambios de signo + bisección, descartando polos
    (donde |f| no se acerca a 0) y puntos fuera del dominio."""
    def ev(x):
        try:
            y = f(x)
            return y if isinstance(y, (int, float)) and math.isfinite(y) else None
        except (ValueError, ZeroDivisionError, OverflowError):
            return None
    out, h = [], (b - a) / n
    x0, y0 = a, ev(a)
    for i in range(1, n + 1):
        x1 = a + i * h
        y1 = ev(x1)
        if y0 is not None and y1 is not None:
            if y0 == 0:
                out.append(x0)
            elif y0 * y1 < 0:
                lo, hi, ylo = x0, x1, y0
                for _ in range(80):
                    mid = (lo + hi) / 2
                    ym = ev(mid)
                    if ym is None:
                        break
                    if ylo * ym <= 0:
                        hi = mid
                    else:
                        lo, ylo = mid, ym
                r = (lo + hi) / 2
                if ev(r) is not None and abs(ev(r)) < 1e-6:
                    out.append(r)
        x0, y0 = x1, y1
    limpio = []
    for r in sorted(out):
        if not limpio or abs(r - limpio[-1]) > 1e-6:
            limpio.append(r)
    return limpio


def mismo_conjunto(a, b, tol=1e-6):
    a, b = sorted(a), sorted(b)
    return len(a) == len(b) and all(abs(x - y) < tol for x, y in zip(a, b))


def misma_region(pred, verdad, puntos):
    return all(bool(pred(x)) == bool(verdad(x)) for x in puntos)


def define(f):
    """Devuelve una función que da False si f no está definida en x."""
    def g(x):
        try:
            return f(x)
        except (ValueError, ZeroDivisionError):
            return False
    return g


MUESTRA = sorted(set([i / 8 for i in range(-160, 161)] + [-2, 3, 2, 10, 8, 6, -3, 0]))


def misma_funcion(f, g, xs=(1.3, 2.7, 5.1, -1.7, 7.9, -4.4, 0.6)):
    return all(abs(f(x) - g(x)) < 1e-9 for x in xs)


def maximo(f, a, b, n=200000):
    """Máximo numérico de f en [a, b] por rejilla fina + refinado ternario."""
    h = (b - a) / n
    xb = max((a + i * h for i in range(n + 1)), key=f)
    lo, hi = xb - h, xb + h
    for _ in range(200):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(m1) < f(m2):
            lo = m1
        else:
            hi = m2
    return f((lo + hi) / 2)


def area(*pts):
    s = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


# =====================================================================
# ÁLGEBRA: ecuaciones e inecuaciones
# =====================================================================
P("algebra", 1, "Solve the equation 3(x − 2) + 5 = 2x + 7.",
  [("x = 8", 8), ("x = 6", 6), ("x = 4", 4), ("x = 10", 10)],
  "Quita paréntesis: 3x − 6 + 5 = 2x + 7 → 3x − 1 = 2x + 7 → x = 8.\nComprueba: 3·6 + 5 = 23 y 2·8 + 7 = 23.",
  lambda v: 3 * (v - 2) + 5 == 2 * v + 7)

P("algebra", 1, "Find the product of the roots of the equation 2x² − 9x + 4 = 0.",
  [("2", 2), ("4", 4), ("9/2", 4.5), ("−2", -2)],
  "Vieta: el producto de las raíces de ax² + bx + c = 0 es c/a = 4/2 = 2.\n(Las raíces son 4 y 1/2, y 4 · 1/2 = 2.)",
  lambda v: abs(math.prod(raices(lambda x: 2 * x * x - 9 * x + 4, -50, 50)) - v) < 1e-6)

P("algebra", 1, "Find the sum of all solutions of the equation |2x − 5| = 7.",
  [("5", 5), ("6", 6), ("7", 7), ("−1", -1)],
  "Dos casos: 2x − 5 = 7 → x = 6; 2x − 5 = −7 → x = −1.\nSuma: 6 + (−1) = 5.",
  lambda v: abs(sum(raices(lambda x: abs(2 * x - 5) - 7, -100, 100)) - v) < 1e-6)

P("algebra", 2, "How many integers x satisfy the inequality x² − 5x − 14 ≤ 0?",
  [("10", 10), ("9", 9), ("8", 8), ("11", 11)],
  "x² − 5x − 14 = (x − 7)(x + 2) ≤ 0 → −2 ≤ x ≤ 7.\nEnteros de −2 a 7: 7 − (−2) + 1 = 10.",
  lambda v: v == sum(1 for x in range(-1000, 1001) if x * x - 5 * x - 14 <= 0))

P("algebra", 2, "Solve the equation √(x + 7) = x + 1.",
  [("x = 2", (2,)), ("x = −3", (-3,)), ("x = 2 or x = −3", (2, -3)), ("no real solution", ())],
  "Eleva al cuadrado: x + 7 = x² + 2x + 1 → x² + x − 6 = 0 → x = 2 o x = −3.\nComprueba en la ecuación original: con x = −3 el lado derecho vale −2, y una raíz cuadrada nunca es negativa. Solo vale x = 2.",
  lambda v: mismo_conjunto(v, raices(lambda x: math.sqrt(x + 7) - (x + 1), -7, 100)))

P("algebra", 1, "Given the system 2x + 3y = 12 and x − y = 1, find the value of xy.",
  [("6", 6), ("5", 5), ("8", 8), ("4", 4)],
  "De la segunda, x = y + 1. Sustituye: 2(y + 1) + 3y = 12 → 5y = 10 → y = 2 y x = 3.\nProducto: xy = 6.",
  # Cramer, otro camino distinto de la sustitución
  lambda v: (lambda d: v == (Fr(12 * -1 - 3 * 1, d) * Fr(2 * 1 - 12 * 1, d)))(2 * -1 - 3 * 1))

P("algebra", 2, "Solve the inequality (x − 3)/(x + 2) ≤ 0.",
  [("−2 < x ≤ 3", lambda x: -2 < x <= 3), ("−2 ≤ x ≤ 3", lambda x: -2 <= x <= 3),
   ("x < −2 or x ≥ 3", lambda x: x < -2 or x >= 3), ("−2 ≤ x < 3", lambda x: -2 <= x < 3)],
  "Puntos clave: x = 3 (anula el numerador) y x = −2 (anula el denominador: prohibido).\nTabla de signos: entre −2 y 3 la fracción es negativa; en x = 3 vale 0 y entra; en x = −2 no existe y no entra.\nSolución: −2 < x ≤ 3.",
  lambda p: misma_region(p, define(lambda x: (x - 3) / (x + 2) <= 0), MUESTRA))

P("algebra", 3, "Find the sum of all integer solutions of the inequality (x² − 4x − 12)/(x² + 1) < 0.",
  [("14", 14), ("18", 18), ("20", 20), ("15", 15)],
  "El denominador x² + 1 siempre es positivo, así que basta con x² − 4x − 12 = (x − 6)(x + 2) < 0 → −2 < x < 6.\nEnteros: −1, 0, 1, 2, 3, 4, 5. Suma: 14.\nOjo: la desigualdad es estricta, así que −2 y 6 no entran (con ellos saldría 18).",
  lambda v: v == sum(x for x in range(-1000, 1001) if (x * x - 4 * x - 12) / (x * x + 1) < 0))

P("algebra", 2, "Let x₁ and x₂ be the roots of x² − 6x + 4 = 0. Find x₁² + x₂².",
  [("28", 28), ("36", 36), ("32", 32), ("20", 20)],
  "Vieta: x₁ + x₂ = 6 y x₁x₂ = 4.\nx₁² + x₂² = (x₁ + x₂)² − 2x₁x₂ = 36 − 8 = 28. No hace falta calcular las raíces.",
  lambda v: abs(sum(r * r for r in raices(lambda x: x * x - 6 * x + 4, -50, 50)) - v) < 1e-6)


def dos_positivas(a):
    d = 4 * a * a - 4 * (a + 6)
    if d <= 0:
        return False
    r1, r2 = (2 * a - math.sqrt(d)) / 2, (2 * a + math.sqrt(d)) / 2
    return r1 > 0 and r2 > 0


P("algebra", 3, "For which values of the parameter a does the equation x² − 2ax + a + 6 = 0 have two distinct positive roots?",
  [("a > 3", lambda a: a > 3), ("a < −2 or a > 3", lambda a: a < -2 or a > 3),
   ("a > 0", lambda a: a > 0), ("−6 < a < −2", lambda a: -6 < a < -2)],
  "Tres condiciones a la vez:\n1) Discriminante positivo: 4a² − 4(a + 6) > 0 → a² − a − 6 > 0 → a < −2 o a > 3.\n2) Suma de raíces 2a > 0 → a > 0.\n3) Producto a + 6 > 0 → a > −6.\nLas tres juntas: a > 3.",
  lambda p: misma_region(p, dos_positivas, [i / 20 for i in range(-400, 401)]))

P("algebra", 1, "Simplify (x² − 9)/(x² + 3x) for x ≠ 0 and x ≠ −3.",
  [("(x − 3)/x", lambda x: (x - 3) / x), ("(x + 3)/x", lambda x: (x + 3) / x),
   ("x − 3", lambda x: x - 3), ("(x − 3)/(x + 3)", lambda x: (x - 3) / (x + 3))],
  "Factoriza: x² − 9 = (x − 3)(x + 3) y x² + 3x = x(x + 3).\nSe simplifica (x + 3) y queda (x − 3)/x.",
  lambda g: misma_funcion(g, lambda x: (x * x - 9) / (x * x + 3 * x)))

P("algebra", 2, "Find the smallest positive integer n such that 7n + 3 is divisible by 11.",
  [("9", 9), ("3", 3), ("5", 5), ("8", 8)],
  "Prueba n = 1, 2, 3…: 7n + 3 da 10, 17, 24, 31, 38, 45, 52, 59, 66. El primer múltiplo de 11 es 66, con n = 9.\nCon congruencias: 7n ≡ 8 (mód 11); como 7·8 = 56 ≡ 1, n ≡ 8·8 = 64 ≡ 9.",
  lambda v: v == next(n for n in range(1, 1000) if (7 * n + 3) % 11 == 0))

P("algebra", 1, "Compute 1001² − 999².",
  [("4000", 4000), ("2000", 2000), ("4", 4), ("40000", 40000)],
  "Diferencia de cuadrados: a² − b² = (a − b)(a + b) = 2 · 2000 = 4000.",
  lambda v: v == 1001 ** 2 - 999 ** 2)

P("algebra", 3, "How many pairs of positive integers (x, y) satisfy x⁴y⁴ − 10x²y² + 9 = 0?",
  [("3", 3), ("2", 2), ("4", 4), ("1", 1)],
  "Llama t = x²y²: t² − 10t + 9 = 0 → t = 1 o t = 9, es decir, xy = 1 o xy = 3.\nPares: (1, 1), (1, 3) y (3, 1). Total: 3.",
  lambda v: v == sum(1 for x in range(1, 60) for y in range(1, 60) if x ** 4 * y ** 4 - 10 * x * x * y * y + 9 == 0))

P("algebra", 2, "Solve the equation x/(x − 2) − 8/(x² − 4) = 1.",
  [("no solution", ()), ("x = 2", (2,)), ("x = −2", (-2,)), ("x = 4", (4,))],
  "Multiplica por x² − 4 = (x − 2)(x + 2): x(x + 2) − 8 = x² − 4 → 2x − 8 = −4 → x = 2.\nPero x = 2 anula el denominador: no está en el dominio. La ecuación no tiene solución.\nTruco: escribe siempre el dominio (x ≠ ±2) ANTES de quitar denominadores.",
  lambda v: mismo_conjunto(v, raices(lambda x: x / (x - 2) - 8 / (x * x - 4) - 1, -50, 50)))

P("algebra", 3, "The sum of all integer solutions of the inequality x² − (a + 1)x + a ≤ 0 equals 15. Find a, if a is a positive integer.",
  [("5", 5), ("6", 6), ("4", 4), ("15", 15)],
  "x² − (a + 1)x + a = (x − 1)(x − a) ≤ 0 → 1 ≤ x ≤ a.\nSuma de 1 a a: a(a + 1)/2 = 15 → a(a + 1) = 30 → a = 5.",
  lambda v: [a for a in range(1, 100) if sum(x for x in range(-200, 201) if x * x - (a + 1) * x + a <= 0) == 15] == [v])

P("algebra", 1, "Solve the inequality 5 − 2x > 11.",
  [("x < −3", lambda x: x < -3), ("x > −3", lambda x: x > -3), ("x < 3", lambda x: x < 3), ("x > 8", lambda x: x > 8)],
  "5 − 2x > 11 → −2x > 6 → al dividir entre un número negativo el signo se da la vuelta: x < −3.",
  lambda p: misma_region(p, lambda x: 5 - 2 * x > 11, MUESTRA))


def resto(coef, r):
    """Resto de dividir el polinomio (coeficientes de mayor a menor) entre (x − r), por Ruffini."""
    acc = 0
    for c in coef:
        acc = acc * r + c
    return acc


P("algebra", 2, "When the polynomial P(x) = x³ + ax − 6 is divided by (x − 2), the remainder is 4. Find a.",
  [("1", 1), ("−1", -1), ("2", 2), ("5", 5)],
  "Teorema del resto: el resto de dividir entre (x − 2) es P(2) = 8 + 2a − 6 = 2a + 2.\n2a + 2 = 4 → a = 1.",
  lambda v: resto([1, 0, v, -6], 2) == 4)

P("algebra", 1, "The equation x² + px + q = 0 has roots 3 and −5. Find p + q.",
  [("−13", -13), ("17", 17), ("−17", -17), ("13", 13)],
  "(x − 3)(x + 5) = x² + 2x − 15, así que p = 2 y q = −15. p + q = −13.\n(Por Vieta: p = −(3 + (−5)) = 2 y q = 3·(−5) = −15.)",
  lambda v: v == (lambda c: c[1] + c[2])([1, -3 + 5, -3 * 5]))

P("algebra", 3, "How many pairs of integers (x, y) satisfy x² − y² = 15?",
  [("8", 8), ("4", 4), ("2", 2), ("6", 6)],
  "(x − y)(x + y) = 15. Los dos factores pueden ser 1 y 15, 3 y 5, 5 y 3, 15 y 1, y lo mismo con signo negativo: 8 posibilidades.\nTodas dan x e y enteros porque los dos factores son impares (por ejemplo, 1 y 15 → x = 8, y = 7). Total: 8 pares.",
  lambda v: v == sum(1 for x in range(-100, 101) for y in range(-100, 101) if x * x - y * y == 15))

P("algebra", 2, "Find the product of all real solutions of x² − |x| − 6 = 0.",
  [("−9", -9), ("9", 9), ("−6", -6), ("6", 6)],
  "Como x² = |x|², llama t = |x| ≥ 0: t² − t − 6 = 0 → t = 3 (t = −2 no vale).\n|x| = 3 → x = 3 o x = −3. Producto: −9.",
  lambda v: abs(math.prod(raices(lambda x: x * x - abs(x) - 6, -50, 50)) - v) < 1e-6)

# =====================================================================
# FUNCIONES Y GRÁFICAS
# =====================================================================
P("funcs", 1, "Given f(x) = 2x² − 3x + 1, find f(−2).",
  [("15", 15), ("3", 3), ("−1", -1), ("11", 11)],
  "f(−2) = 2·4 − 3·(−2) + 1 = 8 + 6 + 1 = 15.\nOjo con el signo: −3·(−2) = +6 (si pones −6 sale 3).",
  lambda v: v == 2 * 4 - 3 * (-2) + 1)

P("funcs", 1, "Find the domain of the function f(x) = √(6 − 2x).",
  [("x ≤ 3", lambda x: x <= 3), ("x ≥ 3", lambda x: x >= 3), ("x < 3", lambda x: x < 3), ("x ≤ 6", lambda x: x <= 6)],
  "Lo de dentro de la raíz no puede ser negativo: 6 − 2x ≥ 0 → x ≤ 3. El 3 sí entra, porque √0 = 0.",
  lambda p: misma_region(p, define(lambda x: math.sqrt(6 - 2 * x) >= 0), MUESTRA))

P("funcs", 2, "Find the vertex of the parabola y = x² − 8x + 13.",
  [("(4, −3)", (4, -3)), ("(−4, −3)", (-4, -3)), ("(4, 3)", (4, 3)), ("(8, 13)", (8, 13))],
  "x del vértice = −b/(2a) = 8/2 = 4; y = 16 − 32 + 13 = −3. Vértice (4, −3).\nTambién completando el cuadrado: x² − 8x + 13 = (x − 4)² − 3.",
  lambda v: abs(v[1] - (-maximo(lambda x: -(x * x - 8 * x + 13), -50, 50))) < 1e-6 and abs(v[0] ** 2 - 8 * v[0] + 13 - v[1]) < 1e-9)

P("funcs", 2, "Find the maximum value of f(x) = −2x² + 12x − 7.",
  [("11", 11), ("3", 3), ("−7", -7), ("25", 25)],
  "Vértice en x = −12/(2·(−2)) = 3. f(3) = −18 + 36 − 7 = 11.\nComo el coeficiente de x² es negativo, la parábola abre hacia abajo y 11 es el máximo (3 es dónde se alcanza, no el valor).",
  lambda v: abs(maximo(lambda x: -2 * x * x + 12 * x - 7, -50, 50) - v) < 1e-6)

P("funcs", 1, "Let f(x) = 3x − 4 and g(x) = x² + 1. Find f(g(2)).",
  [("11", 11), ("5", 5), ("17", 17), ("9", 9)],
  "Primero lo de dentro: g(2) = 4 + 1 = 5. Luego f(5) = 15 − 4 = 11.\n(g(f(2)) = g(2) = 5 es otra cosa: el orden importa.)",
  lambda v: v == (lambda g: 3 * g - 4)(2 ** 2 + 1))

P("funcs", 2, "Find the inverse of the function f(x) = (2x + 1)/(x − 3).",
  [("(3x + 1)/(x − 2)", lambda x: (3 * x + 1) / (x - 2)), ("(x − 3)/(2x + 1)", lambda x: (x - 3) / (2 * x + 1)),
   ("(3x − 1)/(x + 2)", lambda x: (3 * x - 1) / (x + 2)), ("(x + 1)/(2x − 3)", lambda x: (x + 1) / (2 * x - 3))],
  "Escribe y = (2x + 1)/(x − 3) y despeja x: y(x − 3) = 2x + 1 → yx − 2x = 3y + 1 → x = (3y + 1)/(y − 2).\nCambia el nombre de la variable: f⁻¹(x) = (3x + 1)/(x − 2).\nComprueba: f(0) = −1/3 y f⁻¹(−1/3) = 0.",
  lambda g: misma_funcion(lambda x: (2 * g(x) + 1) / (g(x) - 3), lambda x: x))

P("funcs", 3, "Find the maximum value of f(x) = (x² + 2x + 5)/(x² + 2x + 2) over all real x.",
  [("4", 4), ("5/2", 2.5), ("5", 5), ("3", 3)],
  "Llama t = x² + 2x + 2 = (x + 1)² + 1 ≥ 1. Entonces f = (t + 3)/t = 1 + 3/t, que crece cuando t se hace pequeño.\nEl menor t es 1 (en x = −1) y da f = 1 + 3 = 4. (5/2 es f(0), no el máximo.)",
  lambda v: abs(maximo(lambda x: (x * x + 2 * x + 5) / (x * x + 2 * x + 2), -50, 50) - v) < 1e-6)

P("funcs", 2, "How many common points do the graphs of y = x² and y = |x| + 2 have?",
  [("2", 2), ("1", 1), ("0", 0), ("4", 4)],
  "x² = |x| + 2 → con t = |x| ≥ 0: t² − t − 2 = 0 → t = 2 (t = −1 no vale).\nx = 2 o x = −2: dos puntos, (2, 4) y (−2, 4).",
  lambda v: v == len(raices(lambda x: x * x - abs(x) - 2, -50, 50)))

P("funcs", 2, "Which of these functions is even?",
  [("f(x) = x⁴ − 3x² + 1", lambda x: x ** 4 - 3 * x * x + 1), ("f(x) = x³ + x", lambda x: x ** 3 + x),
   ("f(x) = x² + x", lambda x: x * x + x), ("f(x) = 2ˣ", lambda x: 2 ** x)],
  "Par significa f(−x) = f(x): la gráfica es simétrica respecto al eje y.\nEn x⁴ − 3x² + 1 solo hay potencias pares, así que cambiar x por −x no cambia nada. x³ + x es impar; x² + x y 2ˣ no son ni pares ni impares.",
  lambda f: all(abs(f(-x) - f(x)) < 1e-9 for x in (0.5, 1.3, 2.2, 3.7)))

P("funcs", 3, "Find the minimum value of f(x) = |x − 1| + |x + 3|.",
  [("4", 4), ("2", 2), ("0", 0), ("1", 1)],
  "|x − 1| + |x + 3| es la suma de las distancias de x a 1 y a −3.\nPara cualquier x entre −3 y 1 esa suma es justo la distancia entre los dos puntos: 1 − (−3) = 4. Fuera de ese tramo es mayor. Mínimo: 4.",
  lambda v: abs(-maximo(lambda x: -(abs(x - 1) + abs(x + 3)), -50, 50) - v) < 1e-6)

P("funcs", 1, "Find the slope of the line through the points (1, 2) and (4, 11).",
  [("3", 3), ("1/3", Fr(1, 3)), ("9", 9), ("−3", -3)],
  "Pendiente = (y₂ − y₁)/(x₂ − x₁) = (11 − 2)/(4 − 1) = 9/3 = 3.",
  lambda v: v == Fr(11 - 2, 4 - 1))

P("funcs", 2, "Which line passes through the point (4, 3) and is perpendicular to y = 2x + 1?",
  [("y = −0.5x + 5", (-0.5, 5)), ("y = 2x − 5", (2, -5)), ("y = 0.5x + 1", (0.5, 1)), ("y = −0.5x + 3", (-0.5, 3))],
  "Rectas perpendiculares: m₁·m₂ = −1, así que la pendiente es −1/2.\nPor (4, 3): 3 = −0.5·4 + c → c = 5. Recta: y = −0.5x + 5.\n(y = 2x − 5 y y = 0.5x + 1 pasan por el punto, pero no son perpendiculares.)",
  lambda mc: mc[0] * 2 == -1 and mc[0] * 4 + mc[1] == 3)

P("funcs", 3, "For which value of b is the line y = 4x + b tangent to the parabola y = x² + 1?",
  [("−3", -3), ("3", 3), ("−4", -4), ("1", 1)],
  "Tangente = un único punto común: x² + 1 = 4x + b → x² − 4x + (1 − b) = 0 con discriminante 0.\n16 − 4(1 − b) = 0 → 12 + 4b = 0 → b = −3. Punto de tangencia: x = 2, y = 5.",
  # tangente ⇔ la diferencia parábola − recta tiene mínimo exactamente 0
  lambda v: abs(maximo(lambda x: -((x * x + 1) - (4 * x + v)), -50, 50)) < 1e-6)

P("funcs", 2, "A function satisfies f(x + 2) = 3x + 5 for every x. Find f(7).",
  [("20", 20), ("26", 26), ("11", 11), ("17", 17)],
  "Busca el x que da x + 2 = 7, es decir x = 5: f(7) = 3·5 + 5 = 20.\nError típico: meter el 7 directamente (3·7 + 5 = 26).",
  lambda v: v == (lambda t: 3 * (t - 2) + 5)(7))

# =====================================================================
# EXPONENTES Y LOGARITMOS
# =====================================================================
lg = math.log
P("logs", 1, "Evaluate log₂ 32 + log₃ 9.",
  [("7", 7), ("10", 10), ("41", 41), ("5", 5)],
  "log₂ 32 = 5 porque 2⁵ = 32, y log₃ 9 = 2 porque 3² = 9. Suma: 7.",
  near(lg(32, 2) + lg(9, 3), 1e-9))

P("logs", 1, "Evaluate 8^(2/3) · 27^(−1/3).",
  [("4/3", 4 / 3), ("12", 12), ("3/4", 0.75), ("4/9", 4 / 9)],
  "8^(2/3) = (∛8)² = 2² = 4. 27^(−1/3) = 1/∛27 = 1/3.\nProducto: 4 · 1/3 = 4/3.",
  near(8 ** (2 / 3) * 27 ** (-1 / 3), 1e-9))

P("logs", 1, "Solve the equation 3^(x + 1) = 81.",
  [("x = 3", 3), ("x = 4", 4), ("x = 27", 27), ("x = 2", 2)],
  "81 = 3⁴, así que x + 1 = 4 → x = 3.",
  lambda v: 3 ** (v + 1) == 81)

P("logs", 2, "Find the sum of the roots of the equation 4ˣ − 6·2ˣ + 8 = 0.",
  [("3", 3), ("6", 6), ("2", 2), ("8", 8)],
  "4ˣ = (2ˣ)². Con t = 2ˣ > 0: t² − 6t + 8 = 0 → t = 2 o t = 4 → x = 1 o x = 2.\nSuma: 3. (6 es la suma de los valores de t, no de x.)",
  lambda v: abs(sum(raices(lambda x: 4 ** x - 6 * 2 ** x + 8, -20, 20)) - v) < 1e-6)

P("logs", 1, "Evaluate log₆ 4 + log₆ 9.",
  [("2", 2), ("log₆ 13", lg(13, 6)), ("36", 36), ("6", 6)],
  "Suma de logaritmos de la misma base = logaritmo del producto: log₆ (4·9) = log₆ 36 = 2.",
  near(lg(4, 6) + lg(9, 6), 1e-9))

P("logs", 2, "Solve the equation log₂(x − 1) + log₂(x + 1) = 3.",
  [("x = 3", (3,)), ("x = 3 or x = −3", (3, -3)), ("x = −3", (-3,)), ("x = 9", (9,))],
  "log₂((x − 1)(x + 1)) = 3 → x² − 1 = 8 → x = ±3.\nEl dominio exige x − 1 > 0 y x + 1 > 0, o sea x > 1: x = −3 no vale. Solución: x = 3.",
  lambda v: mismo_conjunto(v, raices(lambda x: lg(x - 1, 2) + lg(x + 1, 2) - 3, -50, 50)))

P("logs", 2, "If log₃ a = 4, find log₉ (a²).",
  [("4", 4), ("8", 8), ("2", 2), ("16", 16)],
  "a = 3⁴ = 81, así que a² = 3⁸ = 9⁴ y log₉(a²) = 4.\nCon fórmulas: log₉(a²) = 2·log₉ a = 2·(4/2) = 4.",
  near(lg((3 ** 4) ** 2, 9), 1e-9))

P("logs", 3, "Solve the equation logₓ 16 − logₓ 2 = 3/2.",
  [("x = 4", 4), ("x = 2", 2), ("x = 8", 8), ("x = 16", 16)],
  "logₓ 16 − logₓ 2 = logₓ 8 = 3/2 → x^(3/2) = 8 → x = 8^(2/3) = 4.\nLa base tiene que ser positiva y distinta de 1: 4 vale.",
  lambda v: v > 0 and v != 1 and abs(lg(16, v) - lg(2, v) - 1.5) < 1e-9)

P("logs", 1, "Simplify 2¹⁰ · 4⁻³ / 8.",
  [("2", 2), ("1/2", 0.5), ("4", 4), ("8", 8)],
  "Todo en base 2: 4⁻³ = 2⁻⁶ y 8 = 2³. Exponentes: 10 − 6 − 3 = 1 → 2¹ = 2.",
  near(2 ** 10 * 4 ** -3 / 8))

P("logs", 3, "Solve the inequality log₁/₂ (x − 2) > −3 (the base of the logarithm is 1/2).",
  [("2 < x < 10", lambda x: 2 < x < 10), ("x > 10", lambda x: x > 10), ("x < 10", lambda x: x < 10), ("2 < x < 8", lambda x: 2 < x < 8)],
  "−3 = log₁/₂ 8, porque (1/2)⁻³ = 8.\nCon base menor que 1 el logaritmo es decreciente y el signo se da la vuelta: x − 2 < 8 → x < 10.\nEl dominio pide x − 2 > 0. Solución: 2 < x < 10.",
  lambda p: misma_region(p, define(lambda x: lg(x - 2, 0.5) > -3), MUESTRA))

P("logs", 2, "Which of these numbers is the largest?",
  [("3²⁰", 3 ** 20), ("2³⁰", 2 ** 30), ("5¹²", 5 ** 12), ("10⁹", 10 ** 9)],
  "Ponlos con exponente 10: 2³⁰ = 8¹⁰ y 3²⁰ = 9¹⁰, así que 3²⁰ > 2³⁰.\nAdemás 10⁹ < 2³⁰ (2³⁰ = 1 073 741 824) y 5¹² = 25⁶ < 32⁶ = 2³⁰. El mayor: 3²⁰.",
  lambda v: v == max(3 ** 20, 2 ** 30, 5 ** 12, 10 ** 9))

P("logs", 2, "Find the sum of the roots of the equation 9ˣ − 4·3ˣ + 3 = 0.",
  [("1", 1), ("4", 4), ("3", 3), ("0", 0)],
  "Con t = 3ˣ > 0: t² − 4t + 3 = 0 → t = 1 o t = 3 → x = 0 o x = 1. Suma: 1.",
  lambda v: abs(sum(raices(lambda x: 9 ** x - 4 * 3 ** x + 3, -20, 20)) - v) < 1e-6)

P("logs", 3, "A town of 40,000 people grows by 5% every year. After how many full years will its population first exceed 50,000?",
  [("5", 5), ("4", 4), ("6", 6), ("7", 7)],
  "Hace falta 40 000·1,05ⁿ > 50 000 → 1,05ⁿ > 1,25 → n > log 1,25 / log 1,05 ≈ 4,57. El primer año entero es el 5.\nComprueba: 1,05⁴ ≈ 1,2155 (no llega) y 1,05⁵ ≈ 1,2763 (sí pasa).",
  lambda v: v == next(n for n in range(100) if 40000 * 1.05 ** n > 50000))

P("logs", 2, "Evaluate log₂ 3 · log₃ 8.",
  [("3", 3), ("8/3", 8 / 3), ("24", 24), ("1", 1)],
  "Cambio de base: log₂ 3 · log₃ 8 = (ln 3/ln 2)·(ln 8/ln 3) = ln 8/ln 2 = log₂ 8 = 3.",
  near(lg(3, 2) * lg(8, 3), 1e-9))

P("logs", 3, "Find the product of the roots of the equation (log₁₀ x)² − 3·log₁₀ x + 2 = 0.",
  [("1000", 1000), ("110", 110), ("3", 3), ("100", 100)],
  "Con t = log₁₀ x: t² − 3t + 2 = 0 → t = 1 o t = 2 → x = 10 o x = 100. Producto: 1000.\nAtajo: log₁₀(x₁x₂) = t₁ + t₂ = 3 → x₁x₂ = 10³.",
  lambda v: abs(math.prod(raices(lambda x: lg(x, 10) ** 2 - 3 * lg(x, 10) + 2, 0.5, 500)) - v) < 1e-4)

P("logs", 2, "If 2ᵃ = 3 and 3ᵇ = 4, find ab.",
  [("2", 2), ("12", 12), ("4/3", 4 / 3), ("7", 7)],
  "a = log₂ 3 y b = log₃ 4, así que ab = log₂ 3 · log₃ 4 = log₂ 4 = 2.\nOtra forma: 2^(ab) = (2ᵃ)ᵇ = 3ᵇ = 4 = 2² → ab = 2.",
  near(lg(3, 2) * lg(4, 3), 1e-9))

# =====================================================================
# SUCESIONES
# =====================================================================
P("seqs", 1, "In an arithmetic progression a₁ = 5 and the common difference is d = 3. Find a₂₀.",
  [("62", 62), ("65", 65), ("60", 60), ("57", 57)],
  "aₙ = a₁ + (n − 1)d = 5 + 19·3 = 62.\nError típico: multiplicar por 20 en vez de por 19 (sale 65).",
  lambda v: v == [5 + 3 * k for k in range(20)][-1])

P("seqs", 1, "Find the 8th term of the geometric progression 3, 6, 12, …",
  [("384", 384), ("768", 768), ("192", 192), ("48", 48)],
  "bₙ = b₁·qⁿ⁻¹ = 3·2⁷ = 3·128 = 384.",
  lambda v: v == [3 * 2 ** k for k in range(8)][-1])

P("seqs", 1, "Find the sum of the first 50 positive odd numbers.",
  [("2500", 2500), ("2550", 2550), ("1275", 1275), ("2450", 2450)],
  "1 + 3 + 5 + … + 99: los primeros n impares suman n². 50² = 2500.\n(También como progresión aritmética: (1 + 99)/2 · 50 = 2500.)",
  lambda v: v == sum(range(1, 100, 2)))

P("seqs", 2, "In an arithmetic progression a₃ = 11 and a₇ = 27. Find the sum of its first 10 terms.",
  [("210", 210), ("195", 195), ("230", 230), ("240", 240)],
  "De a₃ a a₇ hay 4 saltos: 4d = 27 − 11 = 16 → d = 4, y a₁ = 11 − 2·4 = 3.\na₁₀ = 3 + 9·4 = 39. S₁₀ = (3 + 39)/2 · 10 = 210.",
  lambda v: v == next(sum(a1 + d * k for k in range(10)) for a1 in range(-50, 51) for d in range(-20, 21)
                      if a1 + 2 * d == 11 and a1 + 6 * d == 27))

P("seqs", 1, "Find the sum of the infinite geometric series 12 + 6 + 3 + …",
  [("24", 24), ("21", 21), ("36", 36), ("18", 18)],
  "Razón q = 1/2 y |q| < 1, así que S = b₁/(1 − q) = 12/(1/2) = 24.",
  near(sum(12 * 0.5 ** k for k in range(200)), 1e-9))

P("seqs", 3, "In a geometric progression b₂ = 6 and b₅ = 162. Find the sum of its first five terms.",
  [("242", 242), ("243", 243), ("728", 728), ("240", 240)],
  "b₅/b₂ = q³ = 162/6 = 27 → q = 3 y b₁ = 6/3 = 2.\nTérminos: 2, 6, 18, 54, 162. Suma: 242.",
  lambda v: v == next(sum(b1 * q ** k for k in range(5)) for b1 in range(1, 50) for q in range(-10, 11)
                      if b1 * q == 6 and b1 * q ** 4 == 162))

P("seqs", 2, "How many terms of the arithmetic progression 7, 11, 15, … are less than 200?",
  [("49", 49), ("48", 48), ("50", 50), ("51", 51)],
  "aₙ = 7 + 4(n − 1) = 4n + 3 < 200 → n < 49,25. Valen n = 1, …, 49: son 49 términos (el último, 199).",
  lambda v: v == sum(1 for t in range(7, 1000, 4) if t < 200))

P("seqs", 2, "Find the sum of all two-digit numbers that are divisible by 7.",
  [("728", 728), ("735", 735), ("714", 714), ("637", 637)],
  "Son 14, 21, …, 98: progresión aritmética con d = 7 y (98 − 14)/7 + 1 = 13 términos.\nSuma: (14 + 98)/2 · 13 = 56 · 13 = 728.",
  lambda v: v == sum(n for n in range(10, 100) if n % 7 == 0))

P("seqs", 1, "A sequence is defined by a₁ = 2 and aₙ₊₁ = 3aₙ − 1. Find a₅.",
  [("122", 122), ("41", 41), ("365", 365), ("121", 121)],
  "Paso a paso: a₂ = 3·2 − 1 = 5, a₃ = 3·5 − 1 = 14, a₄ = 3·14 − 1 = 41, a₅ = 3·41 − 1 = 122.",
  lambda v: v == (lambda f: f(f(f(f(2)))))(lambda a: 3 * a - 1))

P("seqs", 3, "The numbers x − 1, x + 1 and 2x + 5 (in this order) form a geometric progression. Find the positive value of x.",
  [("2", 2), ("3", 3), ("6", 6), ("−3", -3)],
  "En una progresión geométrica el término central al cuadrado es el producto de los otros dos: (x + 1)² = (x − 1)(2x + 5).\nx² + 2x + 1 = 2x² + 3x − 5 → x² + x − 6 = 0 → x = 2 o x = −3. La positiva: x = 2 (la progresión es 1, 3, 9).",
  lambda v: v > 0 and (v - 1) != 0 and (v + 1) ** 2 == (v - 1) * (2 * v + 5))

P("seqs", 2, "Compute 1 − 2 + 3 − 4 + … + 99 − 100.",
  [("−50", -50), ("50", 50), ("−100", -100), ("0", 0)],
  "Agrupa de dos en dos: (1 − 2) + (3 − 4) + … + (99 − 100) son 50 parejas que valen −1. Total: −50.",
  lambda v: v == sum(k if k % 2 else -k for k in range(1, 101)))


def mayor_impar(n):
    while n % 2 == 0:
        n //= 2
    return n


P("seqs", 3, "Each of the numbers 1, 2, 3, …, 16 is replaced by its largest odd divisor (for example, 12 → 3 and 7 → 7). Find the sum of the 16 new numbers.",
  [("86", 86), ("64", 64), ("136", 136), ("85", 85)],
  "Llama S(n) a la suma para 1…n. Los impares no cambian y los pares 2k se convierten en el mayor divisor impar de k:\nS(16) = (1 + 3 + … + 15) + S(8) = 64 + S(8); S(8) = 16 + S(4); S(4) = 4 + S(2); S(2) = 1 + 1 = 2.\nTotal: 64 + 16 + 4 + 2 = 86. Es la versión pequeña del problema 10 de HSE 2024: de 1 a 2ⁿ la suma vale (4ⁿ + 2)/3.",
  lambda v: v == sum(mayor_impar(n) for n in range(1, 17)))

P("seqs", 1, "What is the next term of the sequence 2, 5, 10, 17, 26, …?",
  [("37", 37), ("35", 35), ("36", 36), ("39", 39)],
  "Las diferencias son 3, 5, 7, 9: la siguiente es 11 → 26 + 11 = 37. Es la fórmula n² + 1 (6² + 1 = 37).",
  lambda v: v == 6 ** 2 + 1 and all(k * k + 1 == t for k, t in zip(range(1, 6), (2, 5, 10, 17, 26))))

P("seqs", 1, "The sum of the first three terms of a geometric progression with ratio 2 is 21. Find the first term.",
  [("3", 3), ("7", 7), ("5.25", 5.25), ("1", 1)],
  "b₁ + 2b₁ + 4b₁ = 7b₁ = 21 → b₁ = 3 (la progresión es 3, 6, 12).",
  lambda v: v + 2 * v + 4 * v == 21)

# =====================================================================
# TRIGONOMETRÍA
# =====================================================================
rad = math.radians
P("trig", 1, "Evaluate sin 30° + cos 60°.",
  [("1", 1), ("√3", R3), ("1/2", 0.5), ("(1 + √3)/2", (1 + R3) / 2)],
  "sin 30° = 1/2 y cos 60° = 1/2. Suma: 1.",
  near(math.sin(rad(30)) + math.cos(rad(60)), 1e-9))

P("trig", 1, "Convert 135° to radians.",
  [("3π/4", 3 * PI / 4), ("2π/3", 2 * PI / 3), ("5π/6", 5 * PI / 6), ("3π/5", 3 * PI / 5)],
  "Multiplica por π/180: 135·π/180 = 3π/4.",
  near(rad(135), 1e-12))

P("trig", 2, "sin α = 3/5 and 90° < α < 180°. Find cos α.",
  [("−4/5", -0.8), ("4/5", 0.8), ("−3/4", -0.75), ("3/4", 0.75)],
  "cos²α = 1 − 9/25 = 16/25 → cos α = ±4/5.\nEn el segundo cuadrante el coseno es negativo: cos α = −4/5.",
  near(math.cos(PI - math.asin(0.6)), 1e-9))

P("trig", 2, "tan α = 2. Find (sin α + cos α)/(sin α − cos α).",
  [("3", 3), ("1/3", 1 / 3), ("−3", -3), ("2", 2)],
  "Divide arriba y abajo entre cos α: (tan α + 1)/(tan α − 1) = 3/1 = 3.",
  near((lambda a: (math.sin(a) + math.cos(a)) / (math.sin(a) - math.cos(a)))(math.atan(2)), 1e-9))

P("trig", 2, "Evaluate sin² 25° + sin² 65°.",
  [("1", 1), ("1/2", 0.5), ("2", 2), ("√3/2", R3 / 2)],
  "65° = 90° − 25°, así que sin 65° = cos 25°. Queda sin² 25° + cos² 25° = 1.",
  near(math.sin(rad(25)) ** 2 + math.sin(rad(65)) ** 2, 1e-9))

P("trig", 2, "Find the sum of all solutions of the equation 2 sin x = 1 on the interval [0, 2π).",
  [("π", PI), ("π/3", PI / 3), ("2π", 2 * PI), ("π/6", PI / 6)],
  "sin x = 1/2 → x = π/6 o x = π − π/6 = 5π/6.\nSuma: π/6 + 5π/6 = π.",
  lambda v: abs(sum(raices(lambda x: 2 * math.sin(x) - 1, 0, 2 * PI - 1e-9)) - v) < 1e-6)

P("trig", 3, "How many solutions does the equation sin 2x = cos x have on the interval [0, 2π)?",
  [("4", 4), ("2", 2), ("3", 3), ("6", 6)],
  "sin 2x = 2 sin x cos x, así que 2 sin x cos x − cos x = cos x·(2 sin x − 1) = 0.\ncos x = 0 → x = π/2, 3π/2; sin x = 1/2 → x = π/6, 5π/6. En total, 4 soluciones.\nError típico: dividir entre cos x y perder las dos primeras.",
  lambda v: v == len(raices(lambda x: math.sin(2 * x) - math.cos(x), 0, 2 * PI - 1e-9)))

P("trig", 2, "Find the maximum value of 3 sin x + 4 cos x.",
  [("5", 5), ("7", 7), ("4", 4), ("1", 1)],
  "a sin x + b cos x = √(a² + b²)·sin(x + φ), y el seno llega como mucho a 1. Máximo: √(9 + 16) = 5.\n(7 = 3 + 4 exigiría que seno y coseno valieran 1 a la vez, y eso no pasa.)",
  lambda v: abs(maximo(lambda x: 3 * math.sin(x) + 4 * math.cos(x), 0, 2 * PI) - v) < 1e-6)

P("trig", 1, "Evaluate cos 120°.",
  [("−1/2", -0.5), ("1/2", 0.5), ("−√3/2", -R3 / 2), ("√3/2", R3 / 2)],
  "120° = 180° − 60°. En el segundo cuadrante el coseno es negativo: cos 120° = −cos 60° = −1/2.",
  near(math.cos(rad(120)), 1e-9))


def periodo_minimo(f):
    xs = [i * 0.37 for i in range(40)]
    T = 0.05   # empezar lejos de 0: con T diminuto f(x + T) ≈ f(x) y engañaría
    while T < 20:
        if max(abs(f(x + T) - f(x)) for x in xs) < 2e-3:
            return T
        T += 1e-4
    return None


P("trig", 2, "Find the smallest positive period of the function y = 3 sin(2x + 1).",
  [("π", PI), ("2π", 2 * PI), ("π/2", PI / 2), ("4π", 4 * PI)],
  "El periodo de sin(kx + c) es 2π/|k|. Aquí k = 2: T = 2π/2 = π.\nEl 3 (amplitud) y el +1 (desplazamiento) no cambian el periodo. 2π y 4π también se repiten, pero no son los más pequeños.",
  lambda v: abs(v - periodo_minimo(lambda x: 3 * math.sin(2 * x + 1))) < 0.01)

P("trig", 2, "Two sides of a triangle are 5 and 8, and the angle between them is 60°. Find the third side.",
  [("7", 7), ("√89", math.sqrt(89)), ("√129", math.sqrt(129)), ("13", 13)],
  "Teorema del coseno: c² = 5² + 8² − 2·5·8·cos 60° = 25 + 64 − 40 = 49 → c = 7.\n(√129 sale si usas cos 120°, y √89 si te olvidas del último término.)",
  near(math.dist((5, 0), (8 * math.cos(rad(60)), 8 * math.sin(rad(60)))), 1e-9))

P("trig", 2, "Find the area of a triangle with two sides 6 and 10 and an included angle of 150°.",
  [("15", 15), ("30", 30), ("15√3", 15 * R3), ("7.5", 7.5)],
  "Área = ½·a·b·sin C = ½·6·10·sin 150° = 30 · 1/2 = 15. (sin 150° = sin 30° = 1/2.)",
  near(area((0, 0), (6, 0), (10 * math.cos(rad(150)), 10 * math.sin(rad(150)))), 1e-9))

P("trig", 3, "Evaluate sin 15° · cos 15°.",
  [("1/4", 0.25), ("1/2", 0.5), ("√3/4", R3 / 4), ("1/8", 0.125)],
  "sin x cos x = ½ sin 2x, así que sin 15° cos 15° = ½ sin 30° = ½ · ½ = 1/4.",
  near(math.sin(rad(15)) * math.cos(rad(15)), 1e-9))

P("trig", 3, "sin x + cos x = 7/5. Find sin x · cos x.",
  [("12/25", 12 / 25), ("24/25", 24 / 25), ("7/10", 0.7), ("6/25", 6 / 25)],
  "Eleva al cuadrado: sin²x + 2 sin x cos x + cos²x = 49/25 → 1 + 2 sin x cos x = 49/25.\nsin x cos x = (49/25 − 1)/2 = 24/50 = 12/25.",
  lambda v: (lambda rs: len(rs) > 0 and all(abs(math.sin(r) * math.cos(r) - v) < 1e-6 for r in rs))(
      raices(lambda x: math.sin(x) + math.cos(x) - 1.4, 0, 2 * PI)))

# =====================================================================
# GEOMETRÍA PLANA
# =====================================================================
P("geom", 1, "The legs of a right triangle are 9 and 12. Find the hypotenuse.",
  [("15", 15), ("13", 13), ("17", 17), ("21", 21)],
  "Pitágoras: √(81 + 144) = √225 = 15. (Es el triángulo 3-4-5 multiplicado por 3.)",
  near(math.hypot(9, 12)))

P("geom", 1, "Find each interior angle of a regular hexagon.",
  [("120°", 120), ("108°", 108), ("135°", 135), ("60°", 60)],
  "Suma de ángulos de un polígono de n lados: (n − 2)·180°. Para n = 6: 720°, y repartido entre 6 ángulos iguales: 120°.",
  lambda v: v == 180 - 360 / 6)


def cuerda_comun(c1, r1, c2, r2):
    d = math.dist(c1, c2)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    return 2 * math.sqrt(r1 * r1 - a * a)


P("geom", 2, "In a right triangle ABC the legs are AB = 8 and BC = 6. Circles are drawn with AB and BC as diameters. Find the length of the common chord of the two circles.",
  [("4.8", 4.8), ("5", 5), ("4", 4), ("2.4", 2.4)],
  "Los dos círculos pasan por B (el vértice del ángulo recto). Además, el pie H de la altura desde B está en los dos: ∠AHB = 90° y ∠BHC = 90°, y un ángulo recto siempre «ve» el diámetro.\nLa cuerda común es BH, la altura sobre la hipotenusa: BH = 8·6/10 = 4,8 (la hipotenusa mide 10).\nEs el problema 4 de la olimpiada HSE 2024.",
  near(cuerda_comun((0, 4), 4, (3, 0), 3), 1e-9))

P("geom", 1, "The circumference of a circle is 10π. Find its area.",
  [("25π", 25 * PI), ("100π", 100 * PI), ("10π", 10 * PI), ("5π", 5 * PI)],
  "C = 2πr = 10π → r = 5. Área = πr² = 25π.",
  near(PI * (10 * PI / (2 * PI)) ** 2, 1e-9))


def tercer_cuadrado(area1):
    s1 = math.sqrt(area1)
    s2 = s1 / math.sqrt(2)   # su diagonal es el diámetro del círculo inscrito (= s1)
    s3 = s2 / math.sqrt(2)
    return s3 * s3


P("geom", 2, "A circle is inscribed in a square of area 60 cm². A second square is inscribed in this circle, a second circle is inscribed in the second square, and a third square is inscribed in the second circle. Find the area of the third square.",
  [("15 cm²", 15), ("30 cm²", 30), ("7.5 cm²", 7.5), ("20 cm²", 20)],
  "Si un cuadrado está inscrito en el círculo inscrito en otro cuadrado, su diagonal mide lo que el lado del grande: su área es la mitad.\n60 → 30 → 15 cm².",
  near(tercer_cuadrado(60), 1e-9))

P("geom", 1, "Find the distance between the points (−1, 2) and (5, 10).",
  [("10", 10), ("14", 14), ("8", 8), ("12", 12)],
  "d = √((5 − (−1))² + (10 − 2)²) = √(36 + 64) = √100 = 10.",
  near(math.dist((-1, 2), (5, 10))))


def vertice_por_lados(b, c, a):
    """Triángulo con BC = a sobre el eje x: devuelve A con AB = c y AC = b."""
    x = (c * c - b * b + a * a) / (2 * a)
    return (x, math.sqrt(c * c - x * x))


P("geom", 3, "A triangle has sides 13, 14 and 15. Find the altitude drawn to the side of length 14.",
  [("12", 12), ("11.2", 11.2), ("6", 6), ("14", 14)],
  "Fórmula de Herón: p = (13 + 14 + 15)/2 = 21 y área = √(21·8·7·6) = √7056 = 84.\nAltura = 2·área/base = 168/14 = 12. (11,2 es la altura sobre el lado 15.)",
  near(vertice_por_lados(13, 15, 14)[1], 1e-9))

P("geom", 1, "An isosceles triangle has base 10 and equal sides 13. Find its area.",
  [("60", 60), ("65", 65), ("120", 120), ("30", 30)],
  "La altura cae en el punto medio de la base: √(13² − 5²) = √144 = 12. Área = ½·10·12 = 60.",
  near(area((0, 0), (10, 0), vertice_por_lados(13, 13, 10)), 1e-9))

P("geom", 2, "In triangle ABC, point D lies on AB and point E lies on AC so that DE ∥ BC. AD = 4, DB = 6 and BC = 15. Find DE.",
  [("6", 6), ("10", 10), ("9", 9), ("7.5", 7.5)],
  "Los triángulos ADE y ABC son semejantes con razón AD/AB = 4/10.\nDE = 15·4/10 = 6. (Ojo: la razón es con AB = 10, no con DB = 6.)",
  near((lambda B, C: math.dist((0.4 * B[0], 0.4 * B[1]), (0.4 * C[0], 0.4 * C[1])))((10, 0), (10 + 15 * math.cos(2), 15 * math.sin(2))), 1e-9))


def angulo_inscrito(central):
    """Ángulo en un punto del arco mayor que ve el arco de `central` grados."""
    A, B = (1, 0), (math.cos(rad(central)), math.sin(rad(central)))
    V = (math.cos(rad(central + (360 - central) / 2)), math.sin(rad(central + (360 - central) / 2)))
    u, w = (A[0] - V[0], A[1] - V[1]), (B[0] - V[0], B[1] - V[1])
    return math.degrees(math.acos((u[0] * w[0] + u[1] * w[1]) / (math.hypot(*u) * math.hypot(*w))))


P("geom", 1, "An inscribed angle and a central angle of a circle stand on the same arc. The central angle is 140°. Find the inscribed angle.",
  [("70°", 70), ("140°", 140), ("40°", 40), ("110°", 110)],
  "El ángulo inscrito mide la mitad del central que abarca el mismo arco: 140°/2 = 70°.",
  near(angulo_inscrito(140), 1e-9))

P("geom", 3, "An isosceles trapezoid has bases 6 and 14 and legs of length 5. Find its area.",
  [("30", 30), ("50", 50), ("60", 60), ("42", 42)],
  "Cada lado «sobra» (14 − 6)/2 = 4 por debajo. Altura: √(5² − 4²) = 3.\nÁrea = (6 + 14)/2 · 3 = 30. (50 sale si tomas el lado 5 como altura.)",
  near((lambda h: area((0, 0), (14, 0), (10, h), (4, h)))(math.sqrt(25 - 16)), 1e-9))


def kml():
    A, B, C = (0, 0), (8, 0), (0, 16)   # área 64
    mezcla = lambda P_, Q, t: (P_[0] + t * (Q[0] - P_[0]), P_[1] + t * (Q[1] - P_[1]))
    return area(mezcla(A, B, 1 / 8), mezcla(B, C, 1 / 8), mezcla(C, A, 1 / 8))


P("geom", 3, "Points K, L and M lie on the sides AB, BC and CA of triangle ABC so that AK : KB = BL : LC = CM : MA = 1 : 7. The area of triangle ABC is 64. Find the area of triangle KLM.",
  [("43", 43), ("49", 49), ("21", 21), ("36", 36)],
  "Quita las tres esquinas. En el triángulo AKM: AK = AB/8 y AM = 7·AC/8, así que su área es (1/8)·(7/8) = 7/64 del total, es decir 7.\nLas otras dos esquinas igual. KLM = 64 − 3·7 = 43.",
  near(kml(), 1e-9))

P("geom", 1, "A rectangle has perimeter 34 and one side of length 5. Find its diagonal.",
  [("13", 13), ("12", 12), ("17", 17), ("14", 14)],
  "La mitad del perímetro es 17, así que el otro lado mide 12. Diagonal: √(5² + 12²) = √169 = 13.",
  near(math.hypot(5, 34 / 2 - 5)))

P("geom", 2, "Find the area of a regular hexagon with side 4.",
  [("24√3", 24 * R3), ("16√3", 16 * R3), ("48√3", 48 * R3), ("12√3", 12 * R3)],
  "Un hexágono regular son 6 triángulos equiláteros de lado 4, cada uno de área (√3/4)·16 = 4√3. Total: 24√3.",
  near(area(*[(4 * math.cos(rad(60 * k)), 4 * math.sin(rad(60 * k))) for k in range(6)]), 1e-9))

P("geom", 2, "The distance from a point P to the centre of a circle of radius 5 is 13. Find the length of a tangent segment from P to the circle.",
  [("12", 12), ("8", 8), ("18", 18), ("13", 13)],
  "El radio es perpendicular a la tangente en el punto de contacto: triángulo rectángulo con hipotenusa 13 y cateto 5.\nTangente = √(169 − 25) = √144 = 12.",
  # punto de tangencia buscado numéricamente: el que hace OT ⟂ TP
  lambda v: abs(math.dist((13, 0), (lambda t: (5 * math.cos(t), 5 * math.sin(t)))(
      raices(lambda t: 5 * math.cos(t) * (5 * math.cos(t) - 13) + 25 * math.sin(t) ** 2, 0.01, PI - 0.01)[0])) - v) < 1e-6)

P("geom", 2, "Find the area of the triangle with vertices (1, 1), (7, 3) and (3, 9).",
  [("22", 22), ("44", 44), ("11", 11), ("26", 26)],
  "Fórmula con coordenadas: ½|x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)|\n= ½|1·(3 − 9) + 7·(9 − 1) + 3·(1 − 3)| = ½|−6 + 56 − 6| = 22.",
  near(area((1, 1), (7, 3), (3, 9))))

P("geom", 3, "Find the area of the figure formed by all points (x, y) of the plane with |x − 2| + |y − 3| ≤ 3.",
  [("18", 18), ("36", 36), ("9", 9), ("12", 12)],
  "Es un rombo (un cuadrado girado 45°) con centro (2, 3) y vértices a 3 unidades en horizontal y en vertical: (−1, 3), (5, 3), (2, 0), (2, 6).\nDiagonales 6 y 6 → área = d₁·d₂/2 = 36/2 = 18.",
  lambda v: abs(sum(1 for i in range(-200, 900) for j in range(-100, 1000)
                    if abs((i + .5) / 100 - 2) + abs((j + .5) / 100 - 3) <= 3) / 10000 - v) < 0.05)

# =====================================================================
# COMBINATORIA Y PROBABILIDAD
# =====================================================================
cajas = list(itertools.product(range(1, 7), repeat=2))
P("prob", 1, "Box A and box B each contain six cards numbered 1 to 6. One card is drawn at random from each box. What is the probability that the two numbers add up to 7?",
  [("1/6", Fr(1, 6)), ("7/36", Fr(7, 36)), ("1/12", Fr(1, 12)), ("5/36", Fr(5, 36))],
  "Hay 6·6 = 36 parejas igual de probables. Suman 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) → 6 casos.\nP = 6/36 = 1/6.",
  lambda v: v == Fr(sum(1 for a, b in cajas if a + b == 7), len(cajas)))

P("prob", 1, "In how many different ways can the letters of the word MATHS be arranged?",
  [("120", 120), ("25", 25), ("60", 60), ("24", 24)],
  "5 letras distintas: 5! = 5·4·3·2·1 = 120.",
  lambda v: v == len(set(itertools.permutations("MATHS"))))

P("prob", 1, "In how many ways can a team of 3 people be chosen from 8 people?",
  [("56", 56), ("336", 336), ("24", 24), ("28", 28)],
  "En un equipo el orden no importa: C(8, 3) = 8·7·6/(3·2·1) = 56. (336 sería si importara el orden.)",
  lambda v: v == len(list(itertools.combinations(range(8), 3))))

P("prob", 2, "How many different arrangements of the letters of the word LEVEL are there?",
  [("30", 30), ("120", 120), ("60", 60), ("20", 20)],
  "5 letras con la L repetida 2 veces y la E repetida 2 veces: 5!/(2!·2!) = 120/4 = 30.",
  lambda v: v == len(set(itertools.permutations("LEVEL"))))

bolas = "RRRRRBBB"
P("prob", 2, "A bag contains 5 red balls and 3 blue balls. Two balls are drawn at random without replacement. What is the probability that both are red?",
  [("5/14", Fr(5, 14)), ("25/64", Fr(25, 64)), ("3/14", Fr(3, 14)), ("1/2", Fr(1, 2))],
  "P = 5/8 · 4/7 = 20/56 = 5/14. (25/64 sería devolviendo la primera bola a la bolsa.)",
  lambda v: v == Fr(sum(1 for a, b in itertools.combinations(range(8), 2) if bolas[a] == bolas[b] == "R"),
                    len(list(itertools.combinations(range(8), 2)))))

P("prob", 2, "At a business forum there are 8 pairs of partners (16 people). Every person shakes hands once with every other person except their own partner. How many handshakes are there?",
  [("112", 112), ("120", 120), ("128", 128), ("104", 104)],
  "Si todos se saludaran: C(16, 2) = 16·15/2 = 120. Se quitan los 8 saludos entre socios: 120 − 8 = 112.",
  lambda v: v == sum(1 for a, b in itertools.combinations(range(16), 2) if a // 2 != b // 2))

P("prob", 3, "How many four-digit numbers have all their digits different?",
  [("4536", 4536), ("5040", 5040), ("3024", 3024), ("4320", 4320)],
  "Primera cifra: 9 opciones (no puede ser 0). Segunda: 9 (ya vale el 0, pero no la cifra usada). Tercera: 8. Cuarta: 7.\nTotal: 9·9·8·7 = 4536.",
  lambda v: v == sum(1 for n in range(1000, 10000) if len(set(str(n))) == 4))

monedas = list(itertools.product("HT", repeat=4))
P("prob", 2, "A fair coin is tossed 4 times. What is the probability of getting exactly 2 heads?",
  [("3/8", Fr(3, 8)), ("1/2", Fr(1, 2)), ("1/4", Fr(1, 4)), ("5/16", Fr(5, 16))],
  "Hay 2⁴ = 16 resultados igual de probables. Con exactamente 2 caras: C(4, 2) = 6.\nP = 6/16 = 3/8.",
  lambda v: v == Fr(sum(1 for m in monedas if m.count("H") == 2), len(monedas)))

P("prob", 3, "A three-digit number is chosen at random. What is the probability that it is divisible by 3 or by 5?",
  [("7/15", Fr(7, 15)), ("8/15", Fr(8, 15)), ("1/2", Fr(1, 2)), ("2/5", Fr(2, 5))],
  "De 100 a 999 hay 900 números. Divisibles por 3: 300; por 5: 180; por los dos (por 15): 60.\nInclusión-exclusión: 300 + 180 − 60 = 420. P = 420/900 = 7/15.",
  lambda v: v == Fr(sum(1 for n in range(100, 1000) if n % 3 == 0 or n % 5 == 0), 900))

P("prob", 2, "A country has 30 cities connected by roads. Each of 8 of the cities has exactly 2 roads leaving it, and each of the other 22 cities has exactly 7 roads leaving it. How many roads are there?",
  [("85", 85), ("170", 170), ("115", 115), ("60", 60)],
  "Cada carretera une dos ciudades, así que al sumar por ciudades se cuenta dos veces: 8·2 + 22·7 = 16 + 154 = 170.\n170/2 = 85 carreteras. Es uno de los problemas de práctica de la Financiera.",
  lambda v: (8 * 2 + 22 * 7) % 2 == 0 and v == (8 * 2 + 22 * 7) // 2)

P("prob", 1, "In how many ways can a captain and a vice-captain be chosen from 12 players?",
  [("132", 132), ("66", 66), ("144", 144), ("23", 23)],
  "Importa el orden (son cargos distintos): 12 opciones para capitán y 11 para vicecapitán: 12·11 = 132.",
  lambda v: v == len(list(itertools.permutations(range(12), 2))))


def caminos(m, n):
    t = [[1] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            t[i][j] = t[i - 1][j] + t[i][j - 1]
    return t[m][n]


P("prob", 3, "Moving only right or up along the grid lines, how many shortest paths lead from (0, 0) to (4, 3)?",
  [("35", 35), ("12", 12), ("70", 70), ("21", 21)],
  "Todo camino más corto tiene 7 pasos: 4 a la derecha y 3 hacia arriba. Basta elegir cuáles 3 de los 7 son «arriba»: C(7, 3) = 35.",
  lambda v: v == caminos(4, 3))

giros = list(itertools.product(range(1, 7), repeat=3))
P("prob", 3, "A fair spinner with six equal sectors numbered 1 to 6 is spun three times. What is the probability that it lands on 6 at least once?",
  [("91/216", Fr(91, 216)), ("1/2", Fr(1, 2)), ("125/216", Fr(125, 216)), ("25/72", Fr(25, 72))],
  "Lo contrario de «al menos un 6» es «ningún 6»: (5/6)³ = 125/216.\nP = 1 − 125/216 = 91/216. (25/72 es «exactamente un 6».)",
  lambda v: v == Fr(sum(1 for g in giros if 6 in g), len(giros)))

P("prob", 2, "How many pairs of non-negative integers (x, y) satisfy 2x + 3y ≤ 12?",
  [("19", 19), ("18", 18), ("21", 21), ("16", 16)],
  "Cuenta por valores de y: y = 0 → x de 0 a 6 (7); y = 1 → 2x ≤ 9, x de 0 a 4 (5); y = 2 → x de 0 a 3 (4); y = 3 → x = 0 o 1 (2); y = 4 → x = 0 (1).\nTotal: 7 + 5 + 4 + 2 + 1 = 19. Es la idea del problema 8 de HSE 2024, con números pequeños.",
  lambda v: v == sum(1 for x in range(50) for y in range(50) if 2 * x + 3 * y <= 12))

# =====================================================================
# PROBLEMAS DE TEXTO (porcentajes, movimiento, trabajo, mezclas, producción)
# =====================================================================
P("words", 1, "After a 20% discount a jacket costs 2,400 rubles. What was the original price?",
  [("3,000 rubles", 3000), ("2,880 rubles", 2880), ("2,900 rubles", 2900), ("2,000 rubles", 2000)],
  "Con el descuento pagas el 80 %: 0,8·p = 2400 → p = 2400/0,8 = 3000 rublos.\nError típico: sumar el 20 % a 2400 (sale 2880).",
  lambda v: abs(v * 0.8 - 2400) < 1e-9)

P("words", 2, "A price is increased by 25%, and then the new price is decreased by 20%. How has the price changed overall?",
  [("It has not changed", 0), ("It rose by 5%", 5), ("It fell by 5%", -5), ("It rose by 4%", 4)],
  "Multiplica los factores: 1,25 · 0,8 = 1. El precio vuelve a ser el mismo.\nLos porcentajes no se suman: el 20 % se calcula sobre un precio mayor.",
  near(100 * 1.25 * 0.8 - 100, 1e-9))

P("words", 1, "Two trains leave two stations 360 km apart at the same time and travel towards each other at 70 km/h and 50 km/h. After how many hours do they meet?",
  [("3", 3), ("2.5", 2.5), ("3.5", 3.5), ("4", 4)],
  "Se acercan a 70 + 50 = 120 km/h. Tiempo: 360/120 = 3 horas.",
  lambda v: abs(70 * v + 50 * v - 360) < 1e-9)

P("words", 1, "One worker can finish a job in 6 hours and another in 12 hours. How long will they take if they work together?",
  [("4 hours", 4), ("9 hours", 9), ("3 hours", 3), ("6 hours", 6)],
  "En una hora hacen 1/6 + 1/12 = 3/12 = 1/4 del trabajo, así que juntos tardan 4 horas.\n(9 horas, la media, es el error típico: juntos siempre se tarda MENOS que el más rápido.)",
  lambda v: v * (Fr(1, 6) + Fr(1, 12)) == 1)

P("words", 3, "A boat travels 36 km downstream and then 36 km back upstream in a total of 5 hours. The speed of the current is 3 km/h. Find the speed of the boat in still water.",
  [("15 km/h", 15), ("12 km/h", 12), ("18 km/h", 18), ("9 km/h", 9)],
  "36/(v + 3) + 36/(v − 3) = 5 → 36·2v = 5(v² − 9) → 5v² − 72v − 45 = 0 → v = (72 + 78)/10 = 15 (la otra raíz es negativa).\nComprueba: 36/18 + 36/12 = 2 + 3 = 5 h.",
  lambda v: v > 3 and Fr(36, v + 3) + Fr(36, v - 3) == 5)

P("words", 2, "300 g of a 10% salt solution is mixed with 200 g of a 25% salt solution. What is the salt concentration of the mixture?",
  [("16%", 16), ("17.5%", 17.5), ("15%", 15), ("35%", 35)],
  "Sal: 300·0,10 + 200·0,25 = 30 + 50 = 80 g en 500 g de mezcla. Concentración: 80/500 = 16 %.\n(17,5 % es la media sin tener en cuenta las cantidades.)",
  near(100 * (300 * 0.10 + 200 * 0.25) / 500, 1e-9))

P("words", 3, "A workshop makes tables and chairs. A table needs 2 hours of carpentry and 1 hour of painting; a chair needs 1 hour of carpentry and 1 hour of painting. Each week there are at most 100 hours of carpentry and 80 hours of painting. The profit is 70 per table and 50 per chair. What is the maximum weekly profit?",
  [("4400", 4400), ("4000", 4000), ("3500", 3500), ("5000", 5000)],
  "Restricciones: 2x + y ≤ 100 (carpintería) y x + y ≤ 80 (pintura). El máximo está en un vértice de la región:\n(0, 80) → 4000; (50, 0) → 3500; cruce de las dos rectas, x = 20 e y = 60 → 70·20 + 50·60 = 4400.\nMáximo: 4400. Es el tipo del problema 6 de HSE 2024 (programación lineal).",
  lambda v: v == max(70 * x + 50 * y for x in range(101) for y in range(101) if 2 * x + y <= 100 and x + y <= 80))

P("words", 1, "120 kg of rice is divided between two shops in the ratio 3 : 5. How much does the larger share weigh?",
  [("75 kg", 75), ("45 kg", 45), ("72 kg", 72), ("80 kg", 80)],
  "3 + 5 = 8 partes de 120/8 = 15 kg. La parte grande: 5·15 = 75 kg.",
  lambda v: v == max(a for a in range(121) if 5 * (120 - a) == 3 * a or 3 * (120 - a) == 5 * a))

P("words", 2, "A shop bought a batch of fresh figs worth 125,000 rubles. At the end of each of the four weeks they were stored, the same percentage x of the remaining fruit spoiled and was thrown away. After four weeks, fruit worth 51,200 rubles was left. Find x.",
  [("20%", 20), ("25%", 25), ("14.76%", 14.76), ("16%", 16)],
  "Cada semana queda (1 − x/100) de lo que había: 125 000·(1 − x/100)⁴ = 51 200 → (1 − x/100)⁴ = 0,4096 = 0,8⁴.\n1 − x/100 = 0,8 → x = 20. (14,76 % sale si repartes la pérdida a partes iguales, sin tener en cuenta que cada semana queda menos.)\nEs el problema 2 de la olimpiada HSE 2024.",
  lambda v: abs(125000 * (1 - v / 100) ** 4 - 51200) < 1e-6)

P("words", 2, "A company has two teams. The average age of all its employees is 30. Team A has 9 people with an average age of 26, and the average age in team B is 32. How many people are in team B?",
  [("18", 18), ("9", 9), ("12", 12), ("27", 27)],
  "Suma de edades: 26·9 + 32n = 30(9 + n) → 234 + 32n = 270 + 30n → 2n = 36 → n = 18.",
  lambda v: Fr(26 * 9 + 32 * v, 9 + v) == 30)

P("words", 3, "Two candles of the same length were lit at the same time. The first burns down completely in 3 hours and the second in 4 hours. At 4:00 one candle was exactly three times as long as the other. At what time were they lit?",
  [("1:20", 80), ("1:00", 60), ("1:40", 100), ("2:40", 160)],
  "Tras t horas quedan 1 − t/3 y 1 − t/4 de cada vela. La segunda (más lenta) es el triple: 1 − t/4 = 3(1 − t/3) → 1 − t/4 = 3 − t → 3t/4 = 2 → t = 8/3 h = 2 h 40 min.\n4:00 − 2:40 = 1:20. Es otro problema de práctica de la Financiera.",
  # v = minutos después de medianoche; t = tiempo encendidas hasta las 4:00
  lambda v: (lambda t: 0 < t < 180 and 1 - t / 240 == 3 * (1 - t / 180))(Fr(240 - v)))

P("words", 1, "The population of a city fell from 250,000 to 230,000. By what percentage did it decrease?",
  [("8%", 8), ("20%", 20), ("8.7%", 8.7), ("2%", 2)],
  "Bajó 20 000 sobre los 250 000 de partida: 20 000/250 000 = 0,08 = 8 %.\n(8,7 % sale si divides entre 230 000, que es el error típico.)",
  near(100 * (250000 - 230000) / 250000, 1e-9))

P("words", 3, "A factory planned to produce 600 parts in a certain number of days. By producing 10 more parts per day than planned, it finished the order 3 days early. How many parts per day did it plan to produce?",
  [("40", 40), ("50", 50), ("30", 30), ("60", 60)],
  "600/x − 600/(x + 10) = 3 → 6000 = 3x(x + 10) → x² + 10x − 2000 = 0 → x = 40 (la otra raíz, −50, no vale).\nComprueba: 600/40 = 15 días y 600/50 = 12 días: 3 días antes.",
  lambda v: Fr(600, v) - Fr(600, v + 10) == 3)

P("words", 2, "A car travels 120 km from A to B at 60 km/h and returns at 40 km/h. Find its average speed for the whole trip.",
  [("48 km/h", 48), ("50 km/h", 50), ("52 km/h", 52), ("45 km/h", 45)],
  "Velocidad media = distancia total / tiempo total = 240/(2 + 3) = 48 km/h.\nNo es la media de las dos velocidades (50): vas más tiempo a la velocidad lenta.",
  lambda v: Fr(240) / (Fr(120, 60) + Fr(120, 40)) == v)


# =====================================================================
def comprobar_y_escribir():
    errores, sets = [], []
    rnd = random.Random(2027)
    for i, p in enumerate(PROBS):
        ok = [bool(p["ok"](val)) for _, val in p["opts"]]
        textos = [t for t, _ in p["opts"]]
        if ok.count(True) != 1 or not ok[0]:
            errores.append(f"#{i} {p['q'][:60]} → correctas {ok}")
        if len(set(textos)) != 4:
            errores.append(f"#{i} opciones repetidas: {textos}")
        # La explicación debe nombrar la respuesta si es un número (evita que no cuadren)
        sol = textos[0]
        if re.fullmatch(r"[−\-]?[\d.,/]+", sol):
            variantes = {sol, sol.replace(".", ","), sol.replace("−", "-")}
            if not any(v in p["e"] for v in variantes):
                errores.append(f"#{i} la explicación no menciona la respuesta {sol}")
        # La correcta va en la posición i % 4 (reparto equilibrado); los distractores, barajados
        dist = textos[1:]
        rnd.shuffle(dist)
        pos = i % 4
        o = dist[:pos] + [sol] + dist[pos:]
        sets.append({"sec": p["sec"], "task": TASK[p["sec"]], "lvl": p["lvl"],
                     "qs": [{"t": "mcq", "q": p["q"], "o": o, "a": pos, "e": p["e"]}]})
    if errores:
        raise SystemExit("ERRORES en mat_gen:\n" + "\n".join(errores))
    with open(os.path.join(AQUI, "mat_a.json"), "w", encoding="utf-8") as f:
        json.dump(sets, f, ensure_ascii=False, indent=1)
    from collections import Counter
    print(f"mat: {len(sets)} preguntas comprobadas, todas con exactamente 1 opción correcta")
    print("  por sección:", dict(Counter(s["sec"] for s in sets)))
    print("  por nivel:  ", dict(sorted(Counter(s["lvl"] for s in sets).items())))
    print("  posición de la correcta:", dict(sorted(Counter(s["qs"][0]["a"] for s in sets).items())))


if __name__ == "__main__":
    comprobar_y_escribir()
