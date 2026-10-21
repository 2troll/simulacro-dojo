"""Lecturas cortas (A1-A2) en portugués de Portugal y en ruso, frase a frase con su traducción y
preguntas de comprensión. Cada frase tiene audio (grabar_voces.py edge). Se añade a www/kana.json
como «lecturas».

Uso: python3 datos/lecturas_gen.py
"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# idioma → [(id, título, nivel, [(frase, traducción)], [(pregunta, [opciones], índice correcto)])]
LECTURAS = {
    "pt": [
        ("pt-cafe", "Um café em Lisboa", "A1", [
            ("O Tony chega a Lisboa numa segunda-feira.", "Tony llega a Lisboa un lunes."),
            ("Está cansado, mas está muito contente.", "Está cansado, pero muy contento."),
            ("Entra num café pequeno perto do rio.", "Entra en un café pequeño cerca del río."),
            ("— Bom dia! Uma bica e um pastel de nata, por favor.", "—¡Buenos días! Un café solo y un pastel de nata, por favor."),
            ("O empregado sorri e responde: — É para já!", "El camarero sonríe y responde: —¡Ahora mismo!"),
            ("O café custa um euro e o pastel custa um euro e meio.", "El café cuesta un euro y el pastel, un euro y medio."),
            ("O Tony paga, agradece e olha para o rio.", "Tony paga, da las gracias y mira el río."),
            ("Pensa: «Acho que vou gostar muito desta cidade.»", "Piensa: «Creo que me va a gustar mucho esta ciudad»."),
        ], [
            ("¿Qué día llega Tony?", ["El lunes", "El viernes", "El domingo"], 0),
            ("¿Qué pide?", ["Té y tostadas", "Un café solo y un pastel de nata", "Agua con gas"], 1),
            ("¿Cuánto paga en total?", ["Un euro", "Dos euros y medio", "Cinco euros"], 1),
        ]),
        ("pt-casa", "À procura de casa", "A2", [
            ("A Sara procura um quarto para alugar em Lisboa.", "Sara busca una habitación para alquilar en Lisboa."),
            ("Vê um anúncio: quarto com janela, perto do metro, 450 euros.", "Ve un anuncio: habitación con ventana, cerca del metro, 450 euros."),
            ("Liga para o senhorio e marca uma visita para amanhã.", "Llama al casero y queda para una visita mañana."),
            ("O quarto é pequeno, mas tem muita luz.", "La habitación es pequeña, pero tiene mucha luz."),
            ("O senhorio pede o NIF e dois meses de caução.", "El casero pide el NIF y dos meses de fianza."),
            ("A Sara ainda não tem NIF, por isso vai primeiro às Finanças.", "Sara todavía no tiene NIF, así que primero va a Hacienda."),
            ("Uma semana depois, assina o contrato e recebe as chaves.", "Una semana después, firma el contrato y recibe las llaves."),
        ], [
            ("¿Cuánto cuesta la habitación?", ["350 €", "450 €", "650 €"], 1),
            ("¿Qué le pide el casero?", ["El pasaporte y una foto", "El NIF y dos meses de fianza", "Un año por adelantado"], 1),
            ("¿Adónde va Sara primero?", ["A Hacienda (Finanças)", "Al banco", "Al metro"], 0),
        ]),
        ("pt-guia", "O primeiro tour", "A2", [
            ("Hoje é o primeiro tour do Tony em Lisboa.", "Hoy es el primer tour de Tony en Lisboa."),
            ("O ponto de encontro é na Praça do Comércio, às dez.", "El punto de encuentro es en la Plaza del Comercio, a las diez."),
            ("Chegam seis turistas: dois de Madrid e quatro do Dubai.", "Llegan seis turistas: dos de Madrid y cuatro de Dubái."),
            ("O Tony explica a história da cidade em espanhol e em árabe.", "Tony explica la historia de la ciudad en español y en árabe."),
            ("Sobem até um miradouro e veem o rio Tejo inteiro.", "Suben hasta un mirador y ven todo el río Tajo."),
            ("Começa a chover e a calçada fica escorregadia.", "Empieza a llover y el empedrado se pone resbaladizo."),
            ("Ninguém cai, e no fim todos querem tirar uma fotografia com o guia.", "Nadie se cae y, al final, todos quieren hacerse una foto con el guía."),
        ], [
            ("¿Dónde es el punto de encuentro?", ["En el mirador", "En la Plaza del Comercio", "En la estación"], 1),
            ("¿En qué idiomas explica Tony?", ["Portugués e inglés", "Español y árabe", "Solo en inglés"], 1),
            ("¿Qué pasa cuando llueve?", ["El tour se cancela", "El empedrado resbala", "Toman un taxi"], 1),
        ]),
    ],
    "ru": [
        ("ru-znak", "Знакомство", "A1", [
            ("Привет! Меня зовут Тони.", "¡Hola! Me llamo Tony."),
            ("Я из Испании, но сейчас живу в Японии.", "Soy de España, pero ahora vivo en Japón."),
            ("Я говорю по-испански, по-арабски и по-английски.", "Hablo español, árabe e inglés."),
            ("Сейчас я учу русский язык.", "Ahora estoy aprendiendo ruso."),
            ("Это трудно, но очень интересно.", "Es difícil, pero muy interesante."),
            ("Я хочу учиться в России.", "Quiero estudiar en Rusia."),
            ("А вы? Как вас зовут?", "¿Y usted? ¿Cómo se llama?"),
        ], [
            ("¿De dónde es Tony?", ["De Rusia", "De España", "De Japón"], 1),
            ("¿Qué está aprendiendo ahora?", ["Ruso", "Japonés", "Portugués"], 0),
            ("¿Cómo le parece el ruso?", ["Fácil y aburrido", "Difícil pero interesante", "Imposible"], 1),
        ]),
        ("ru-kafe", "В кафе", "A1", [
            ("Тони и его друг Ахмед идут в кафе.", "Tony y su amigo Ahmed van a un café."),
            ("— Здравствуйте! У вас есть меню?", "—¡Buenas! ¿Tienen carta?"),
            ("— Конечно. Вот меню.", "—Claro. Aquí tiene la carta."),
            ("— Это без свинины?", "—¿Esto es sin cerdo?"),
            ("— Да, это курица с рисом. Всё халяль.", "—Sí, es pollo con arroz. Todo es halal."),
            ("— Отлично! Две курицы и два чая, пожалуйста.", "—¡Perfecto! Dos de pollo y dos tés, por favor."),
            ("Всё очень вкусно. Счёт — восемьсот рублей.", "Todo está muy rico. La cuenta: ochocientos rublos."),
        ], [
            ("¿Con quién va Tony?", ["Con su amigo Ahmed", "Con su profesor", "Solo"], 0),
            ("¿Qué comen?", ["Pescado", "Pollo con arroz", "Sopa de col"], 1),
            ("¿Cuánto cuesta la cuenta?", ["80 rublos", "800 rublos", "8.000 rublos"], 1),
        ]),
        ("ru-uni", "Первый день в университете", "A2", [
            ("Сегодня понедельник, первый день учёбы.", "Hoy es lunes, el primer día de clase."),
            ("Тони живёт в общежитии рядом с университетом.", "Tony vive en la residencia, cerca de la universidad."),
            ("Утром он идёт в деканат и получает студенческий билет.", "Por la mañana va a la secretaría y recibe el carné de estudiante."),
            ("Первая пара начинается в девять часов.", "La primera clase empieza a las nueve."),
            ("Преподаватель говорит медленно, и Тони почти всё понимает.", "La profesora habla despacio y Tony lo entiende casi todo."),
            ("В группе студенты из Египта, Бразилии и Китая.", "En el grupo hay estudiantes de Egipto, Brasil y China."),
            ("Вечером Тони звонит маме: «Всё хорошо, мне здесь нравится!»", "Por la noche, Tony llama a su madre: «¡Todo bien, aquí me gusta!»."),
        ], [
            ("¿Dónde vive Tony?", ["En un hotel", "En la residencia", "En casa de un amigo"], 1),
            ("¿Qué recibe en la secretaría?", ["El carné de estudiante", "El visado", "Las llaves"], 0),
            ("¿A qué hora empieza la primera clase?", ["A las ocho", "A las nueve", "A las diez"], 1),
        ]),
    ],
}


def validar():
    for lang, L in LECTURAS.items():
        ids = set()
        for (i, tit, niv, frases, preg) in L:
            assert i not in ids and i.startswith(lang), i
            ids.add(i)
            assert frases and all(len(f) == 2 and all(f) for f in frases), i
            for (q, ops, ok) in preg:
                assert 0 <= ok < len(ops), (i, q)


def main():
    validar()
    ruta = os.path.join(RAIZ, "www", "kana.json")
    datos = json.load(open(ruta, encoding="utf-8"))
    datos["lecturas"] = {lang: [{"id": i, "t": tit, "n": niv, "f": [{"o": o, "e": e} for o, e in frases],
                                 "q": [{"p": p, "o": ops, "ok": ok} for p, ops, ok in preg]}
                                for (i, tit, niv, frases, preg) in L] for lang, L in LECTURAS.items()}
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    print("lecturas:", {k: len(v) for k, v in LECTURAS.items()})


if __name__ == "__main__":
    main()
