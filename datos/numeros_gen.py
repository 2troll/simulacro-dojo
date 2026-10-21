"""Números escritos con letra (0-100, centenas y mil) en portugués de Portugal, ruso y japonés,
para el juego «Números al oído» de la mecanografía: suena el número y se escribe en cifras.
Se añade a www/kana.json como «numeros» (un dict por idioma, no una lista de fichas).

Uso: python3 datos/numeros_gen.py
"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENTENAS = [200, 300, 400, 500, 600, 700, 800, 900, 1000]

PT_U = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze",
        "treze", "catorze", "quinze", "dezasseis", "dezassete", "dezoito", "dezanove"]
PT_D = {20: "vinte", 30: "trinta", 40: "quarenta", 50: "cinquenta", 60: "sessenta", 70: "setenta", 80: "oitenta", 90: "noventa"}
PT_C = {100: "cem", 200: "duzentos", 300: "trezentos", 400: "quatrocentos", 500: "quinhentos", 600: "seiscentos",
        700: "setecentos", 800: "oitocentos", 900: "novecentos", 1000: "mil"}

RU_U = ["ноль", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять", "одиннадцать",
        "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
RU_D = {20: "двадцать", 30: "тридцать", 40: "сорок", 50: "пятьдесят", 60: "шестьдесят", 70: "семьдесят", 80: "восемьдесят", 90: "девяносто"}
RU_C = {100: "сто", 200: "двести", 300: "триста", 400: "четыреста", 500: "пятьсот", 600: "шестьсот",
        700: "семьсот", 800: "восемьсот", 900: "девятьсот", 1000: "тысяча"}

JA_U = ["ゼロ", "いち", "に", "さん", "よん", "ご", "ろく", "なな", "はち", "きゅう"]
JA_C = {100: "ひゃく", 200: "にひゃく", 300: "さんびゃく", 400: "よんひゃく", 500: "ごひゃく", 600: "ろっぴゃく",
        700: "ななひゃく", 800: "はっぴゃく", 900: "きゅうひゃく", 1000: "せん"}


def pt(n):
    if n < 20:
        return PT_U[n]
    if n in PT_C:
        return PT_C[n]
    d, u = n // 10 * 10, n % 10
    return PT_D[d] + (" e " + PT_U[u] if u else "")


def ru(n):
    if n < 20:
        return RU_U[n]
    if n in RU_C:
        return RU_C[n]
    d, u = n // 10 * 10, n % 10
    return RU_D[d] + (" " + RU_U[u] if u else "")


def ja(n):
    if n in JA_C:
        return JA_C[n]
    if n < 10:
        return JA_U[n]
    d, u = n // 10, n % 10
    return ("" if d == 1 else JA_U[d]) + "じゅう" + (JA_U[u] if u else "")


def main():
    nums = list(range(0, 101)) + CENTENAS
    assert pt(21) == "vinte e um" and pt(100) == "cem" and pt(16) == "dezasseis"
    assert ru(42) == "сорок два" and ru(100) == "сто"
    assert ja(10) == "じゅう" and ja(34) == "さんじゅうよん" and ja(600) == "ろっぴゃく"
    ruta = os.path.join(RAIZ, "www", "kana.json")
    datos = json.load(open(ruta, encoding="utf-8"))
    datos["numeros"] = {k: [{"n": n, "t": f(n)} for n in nums] for k, f in (("pt", pt), ("ru", ru), ("ja", ja))}
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, separators=(",", ":"))
    print("numeros:", {k: len(v) for k, v in datos["numeros"].items()})


if __name__ == "__main__":
    main()
