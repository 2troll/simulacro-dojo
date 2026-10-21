"""Ruso desde cero para hispanohablantes: el alfabeto cirílico, vocabulario con frases y lo que
hace falta para estudiar en una universidad rusa (vía cuota estatal: año preparatorio y ТРКИ).
Se añade a www/kana.json.

La pronunciación (campo r) marca la sílaba tónica en MAYÚSCULAS: en ruso el acento no se escribe
y cambia el sonido de la «o» átona, que suena «a» (молоко = malakÓ).

Uso: python3 datos/ru_gen.py   (después de kana_gen, vocab_gen y pt_gen)
"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (letra, sonido, qué suena, palabra de ejemplo, significado, truco, lo que dice la voz)
CIRILICO = {
    "Como en español": [
        ("А а", "a", "a, como en «casa»", "мама", "mamá", "Igual que la nuestra.", "а, мама"),
        ("К к", "k", "k, como en «casa»", "кот", "gato", "Igual que la nuestra.", "ка, кот"),
        ("М м", "m", "m, como en «mano»", "метро", "metro", "Igual, pero la minúscula es una M pequeña, no «m» redonda.", "эм, метро"),
        ("О о", "o", "o (si es tónica); si no, suena «a»", "молоко", "leche", "malakÓ: solo la O con acento suena O.", "о, молоко"),
        ("Т т", "t", "t, como en «té»", "такси", "taxi", "En cursiva se escribe como una «m»: no te asustes.", "тэ, такси"),
    ],
    "Engañosas: parecen latinas": [
        ("В в", "v", "v, como la «v» inglesa (labio y dientes)", "вода", "agua", "Parece una B, pero es V. «Водка» no; «вода» sí: agua.", "вэ, вода"),
        ("Е е", "ye", "ye, como en «yema»", "есть", "comer / hay", "Parece E, pero suena «ye».", "е, есть"),
        ("Н н", "n", "n, como en «no»", "нет", "no", "Parece H, pero es N. НЕТ = «nyet», no.", "эн, нет"),
        ("Р р", "r", "r, como en «pero» (o «perro» si quieres)", "рыба", "pescado", "Parece P, pero es R. Los españoles la pronunciamos perfecta.", "эр, рыба"),
        ("С с", "s", "s, como en «sol»", "сок", "zumo", "Parece C, pero siempre es S.", "эс, сок"),
        ("У у", "u", "u, como en «uva»", "утро", "mañana (por la mañana)", "Parece Y, pero suena U.", "у, утро"),
        ("Х х", "j", "j suave, como en «jamón» dicho con calma", "хлеб", "pan", "Parece X, pero suena J.", "ха, хлеб"),
    ],
    "Nuevas": [
        ("Б б", "b", "b, como en «boca»", "банан", "plátano", "La B de verdad lleva un «sombrero».", "бэ, банан"),
        ("Г г", "g", "g siempre dura, como en «gato»", "город", "ciudad", "Una L al revés. Nunca suena como nuestra «ge».", "гэ, город"),
        ("Д д", "d", "d, como en «dedo»", "дом", "casa", "Una casita con patas: «дом», casa.", "дэ, дом"),
        ("Ё ё", "yo", "yo, como en «yogur»; siempre tónica", "ёлка", "abeto", "Muchas veces se escribe sin puntos (Е): la pronunciación hay que saberla.", "ё, ёлка"),
        ("Ж ж", "zh", "como la «j» francesa (sonido de abeja)", "журнал", "revista", "Parece un insecto, y suena a zumbido: «zhhh».", "жэ, журнал"),
        ("З з", "z", "z zumbada, como la «s» de «mismo»", "зима", "invierno", "Parece un 3. Suena a mosquito: «zzz».", "зэ, зима"),
        ("И и", "i", "i, como en «isla»", "игра", "juego (de mesa, deporte)", "Una N al revés: suena I.", "и, игра"),
        ("Й й", "y", "y breve, como en «hoy»", "чай", "té", "Una И con un sombrerito: «i corta».", "и краткое, чай"),
        ("Л л", "l", "l, más oscura que la nuestra", "лук", "cebolla", "Parece la letra griega lambda.", "эль, лук"),
        ("П п", "p", "p, como en «pan»", "парк", "parque", "La π de las matemáticas.", "пэ, парк"),
        ("Ф ф", "f", "f, como en «foto»", "фото", "foto", "Un círculo atravesado por una raya.", "эф, фото"),
        ("Ц ц", "ts", "ts, como en «pizza»", "центр", "centro", "Una U cuadrada con una colita.", "цэ, центр"),
        ("Ч ч", "ch", "ch, como en «chico»", "часы", "reloj", "Parece un 4: imagina a un «chico» con un 4 en la camiseta.", "чэ, часы"),
        ("Ш ш", "sh", "sh, como «¡shhh!» (silencio)", "школа", "escuela", "Tres dientes: el sonido que haces con los dientes para pedir silencio.", "ша, школа"),
        ("Щ щ", "shch", "sh más suave y larga", "щи", "sopa de col", "Una Ш con colita: más larga y suave.", "ща, щи"),
        ("Ъ ъ", "—", "no suena: separa (signo duro)", "объём", "volumen", "Casi no aparece. Hace una pequeña pausa: ob-yom.", "твёрдый знак, объём"),
        ("Ы ы", "y", "una «i» dicha con la lengua hacia atrás", "мы", "nosotros", "El sonido de cuando te dan un golpe en la barriga: «ы».", "ы, мы"),
        ("Ь ь", "ʼ", "no suena: ablanda la consonante de antes (signo blando)", "мать", "madre", "Pon la lengua como para decir «i» al terminar la consonante.", "мягкий знак, мать"),
        ("Э э", "e", "e, como en «eso»", "это", "esto", "La E «de verdad», vuelta hacia la izquierda.", "э, это"),
        ("Ю ю", "yu", "yu, como en «yuca»", "юг", "sur", "Un IO pegado: suena YU.", "ю, юг"),
        ("Я я", "ya", "ya, como en «yate»", "я", "yo", "Una R al revés. Y sola es «я»: yo.", "я, я"),
    ],
}

# Tema → [(ruso, pronunciación, español, frase, traducción, pista)]
VOCAB = {
    "Lo básico": [
        ("Здравствуйте", "ZDRASTvuitie", "hola (formal)", "Здравствуйте! Меня зовут Тони.", "¡Hola! Me llamo Tony.", "La primera «в» no se pronuncia. Si te lías, di «Привет» con amigos."),
        ("Привет", "priVIET", "hola (con amigos)", "Привет! Как дела?", "¡Hola! ¿Qué tal?", ""),
        ("Спасибо", "spaSIba", "gracias", "Спасибо большое!", "¡Muchas gracias!", ""),
        ("Пожалуйста", "paZHAlsta", "por favor / de nada", "Чай, пожалуйста.", "Un té, por favor.", "Sirve para «por favor» y para «de nada»."),
        ("Да / Нет", "da / niet", "sí / no", "Да, да… то есть нет.", "Sí, sí… o sea, no.", ""),
        ("Извините", "izviNIte", "perdone", "Извините, я не понимаю.", "Perdone, no entiendo.", ""),
        ("Я не понимаю", "ya nie panimAyu", "no entiendo", "Я не понимаю, говорите медленнее.", "No entiendo, hable más despacio.", ""),
        ("Вы говорите по-испански?", "vy gavaRIte pa-isPANski", "¿habla español?", "Вы говорите по-испански? Нет? Хорошо, по-английски.", "¿Habla español? ¿No? Vale, en inglés.", ""),
        ("Хорошо", "haraSHO", "bien / vale", "Всё хорошо!", "¡Todo bien!", "Dos «o» átonas que suenan «a»: haraSHÓ."),
        ("До свидания / Пока", "da sviDAnia / paKA", "adiós / chao", "Пока, до завтра!", "¡Chao, hasta mañana!", ""),
        ("Меня зовут…", "miNIA zaVUT", "me llamo…", "Меня зовут Тони, я из Испании.", "Me llamo Tony, soy de España.", "Literalmente: «a mí me llaman…»."),
        ("Как дела?", "kak diLA", "¿qué tal?", "Как дела? — Нормально.", "¿Qué tal? — Normal.", "«Нормально» es la respuesta rusa estándar: ni bien ni mal."),
    ],
    "Números": [
        ("Один, два, три", "aDIN, dva, tri", "uno, dos, tres", "Один, два, три — поехали!", "¡Uno, dos, tres… vamos!", ""),
        ("Четыре, пять", "chiTYrie, piat", "cuatro, cinco", "Пять минут, пожалуйста.", "Cinco minutos, por favor.", ""),
        ("Шесть, семь, восемь", "shest, siem, VOsiem", "seis, siete, ocho", "Урок в восемь утра.", "La clase es a las ocho de la mañana.", ""),
        ("Девять, десять", "DIEviat, DIEsiat", "nueve, diez", "Десять рублей? Дорого!", "¿Diez rublos? ¡Caro!", "Es broma: con diez rublos no compras casi nada."),
        ("Сто / Тысяча", "sto / TYsiacha", "cien / mil", "Тысяча рублей.", "Mil rublos.", ""),
        ("Сколько стоит?", "SKOLka STOit", "¿cuánto cuesta?", "Сколько стоит билет?", "¿Cuánto cuesta el billete?", ""),
    ],
    "Comer (halal)": [
        ("Вода", "vaDA", "agua", "Можно воды?", "¿Me da agua?", ""),
        ("Чай / Кофе", "chai / KOfie", "té / café", "Чай с лимоном, пожалуйста.", "Té con limón, por favor.", "En Rusia se bebe té a todas horas."),
        ("Хлеб", "hliep", "pan", "Хлеб — всему голова.", "El pan es lo primero (refrán).", ""),
        ("Курица / Говядина", "KUritsa / gaVIAdina", "pollo / ternera", "Курица или говядина?", "¿Pollo o ternera?", ""),
        ("Без свинины", "biez sviNIny", "sin cerdo", "Это без свинины?", "¿Esto es sin cerdo?", "Útil siempre. Pregunta también por «сало» (tocino)."),
        ("Халяль", "haLIAL", "halal", "Где здесь халяльное кафе?", "¿Dónde hay un café halal por aquí?", "En Moscú, Kazán y el Cáucaso hay mucha comida halal."),
        ("Рис / Суп", "ris / sup", "arroz / sopa", "Суп дня, пожалуйста.", "La sopa del día, por favor.", ""),
        ("Счёт", "shchiot", "la cuenta", "Счёт, пожалуйста.", "La cuenta, por favor.", ""),
        ("Вкусно!", "VKUSna", "¡qué rico!", "Очень вкусно, спасибо!", "¡Muy rico, gracias!", ""),
    ],
    "Ciudad y transporte": [
        ("Метро", "miTRO", "metro", "Где метро?", "¿Dónde está el metro?", "El metro de Moscú es un museo: mira los techos."),
        ("Вокзал", "vagZAL", "estación de tren", "Как доехать до вокзала?", "¿Cómo llego a la estación?", ""),
        ("Билет", "biLIET", "billete", "Один билет до Казани.", "Un billete a Kazán.", ""),
        ("Направо / Налево / Прямо", "naPRAva / naLIEva / PRIAma", "a la derecha / izquierda / recto", "Идите прямо, потом налево.", "Siga recto y luego a la izquierda.", ""),
        ("Где…?", "gdie", "¿dónde…?", "Где туалет?", "¿Dónde está el baño?", ""),
        ("Улица", "Ulitsa", "calle", "Я живу на этой улице.", "Vivo en esta calle.", ""),
        ("Аптека / Больница", "apTIEka / balNItsa", "farmacia / hospital", "Где ближайшая аптека?", "¿Dónde está la farmacia más cercana?", ""),
        ("Мечеть", "miCHET", "mezquita", "Пятничная молитва в мечети в час.", "La oración del viernes en la mezquita es a la una.", ""),
    ],
    "Personas y verbos": [
        ("Я / Ты / Вы", "ya / ty / vy", "yo / tú / usted (y vosotros)", "Вы студент?", "¿Usted es estudiante?", "Con profesores y desconocidos, siempre «Вы»."),
        ("Друг / Подруга", "druk / paDRUga", "amigo / amiga", "Это мой друг из Японии.", "Este es mi amigo de Japón.", ""),
        ("Семья", "siMIA", "familia", "У меня большая семья.", "Tengo una familia grande.", ""),
        ("Хотеть", "haTIET", "querer", "Я хочу учиться в России.", "Quiero estudiar en Rusia.", ""),
        ("Мочь / Можно?", "moch / MOZHna", "poder / ¿se puede?", "Можно войти?", "¿Se puede pasar?", "«Можно?» abre casi todas las puertas."),
        ("Говорить", "gavaRIT", "hablar", "Я говорю по-испански и по-арабски.", "Hablo español y árabe.", ""),
        ("Учиться", "uCHItsa", "estudiar (en un centro)", "Я учусь на подготовительном факультете.", "Estudio en el curso preparatorio.", ""),
        ("Работать", "raBOtat", "trabajar", "Я работаю гидом.", "Trabajo de guía.", ""),
        ("Понимать", "paniMAT", "entender", "Теперь я понимаю!", "¡Ahora lo entiendo!", ""),
        ("Знать", "znat", "saber / conocer", "Я не знаю.", "No lo sé.", ""),
    ],
}

# Estudiar en Rusia: (término, qué es, consejo)
UNI = [
    ("Подготовительный факультет (подфак)", "año preparatorio de ruso", "Los estudiantes de la cuota que no saben ruso hacen primero este curso: ruso intensivo y asignaturas básicas de la carrera."),
    ("Квота / Россотрудничество", "beca de cuota estatal / la agencia que la gestiona", "La solicitud va por la plataforma education-in-russia.com y la Casa Rusa del país. Cubre la matrícula, no siempre el alojamiento."),
    ("ТРКИ / TORFL", "examen oficial de ruso para extranjeros", "Niveles: ТЭУ (A1), ТБУ (A2), ТРКИ-1 (B1)… Para entrar a la carrera en ruso suelen pedir el ТРКИ-1."),
    ("Общежитие", "residencia de estudiantes", "La más barata. Lleva el pasaporte y las fotos: piden registro para darte la llave."),
    ("Стипендия", "beca (paga mensual)", "Los de cuota suelen cobrar una pequeña paga mensual. No cuentes con ella para vivir."),
    ("Деканат", "secretaría de la facultad", "Ahí se arregla casi todo: certificados, horarios y problemas con asignaturas."),
    ("Расписание", "horario", "Suele estar en un tablón o en la web de la universidad, y cambia por semanas pares e impares."),
    ("Пара", "clase de 90 minutos", "Una «пара» son dos horas académicas seguidas."),
    ("Зачёт / Экзамен", "aprobado-suspenso / examen con nota", "Primero tienes que pasar los «зачёты» para que te dejen presentarte a los exámenes."),
    ("Сессия", "época de exámenes", "En enero y en junio. Si suspendes hay «пересдача» (recuperación)."),
    ("Студенческий билет", "carné de estudiante", "Descuentos en transporte y museos."),
    ("Зачётная книжка", "libreta de notas", "Cada profesor firma ahí tus aprobados. Que no se te pierda."),
    ("Миграционный учёт / регистрация", "registro de extranjero en tu dirección", "Obligatorio en pocos días tras llegar. Normalmente lo hace la universidad: pregunta el primer día."),
    ("Учебная виза", "visado de estudiante", "La universidad manda la invitación oficial («приглашение») y con ella pides el visado en el consulado."),
    ("Медосмотр / Медицинская страховка", "reconocimiento médico / seguro médico", "Lo piden al llegar para la residencia y el registro. Lleva tu historial de vacunas."),
    ("Куратор", "tutor de grupo", "Ayuda a los extranjeros con papeles y dudas: apúntate su teléfono."),
    ("Справка", "certificado", "Para todo te piden una «справка». Se pide en el деканат."),
]


def validar():
    letras = [l for g in CIRILICO.values() for l in g]
    assert len(letras) == 33, len(letras)
    for l in letras:
        assert len(l) == 7 and all(l[:4]) and l[6], l
    vistos = set()
    for tema, lista in VOCAB.items():
        for e in lista:
            assert len(e) == 6 and all(e[:5]), (tema, e)
            assert e[0] not in vistos, e[0]
            vistos.add(e[0])
    for t in UNI:
        assert len(t) == 3 and all(t), t


def main():
    validar()
    ruta = os.path.join(RAIZ, "www", "kana.json")
    datos = json.load(open(ruta, encoding="utf-8"))
    datos["cirilico"] = [{"c": c, "r": r, "m": m, "f": f, "fe": fe, "t": t, "v": v, "g": g}
                         for g, lista in CIRILICO.items() for (c, r, m, f, fe, t, v) in lista]
    datos["ruvocab"] = [{"c": c, "r": r, "m": m, "f": f, "fe": fe, "t": t, "g": g}
                        for g, lista in VOCAB.items() for (c, r, m, f, fe, t) in lista]
    datos["ruuni"] = [{"c": c, "m": m, "t": t, "g": "Estudiar en Rusia"} for (c, m, t) in UNI]
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    print(f"ru: {len(datos['cirilico'])} letras · {len(datos['ruvocab'])} palabras · {len(datos['ruuni'])} de universidad")


if __name__ == "__main__":
    main()
