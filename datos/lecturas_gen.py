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
        ("pt-mercado", "No mercado", "A1", [
            ("Ao sábado de manhã, o Tony vai ao mercado.", "El sábado por la mañana, Tony va al mercado."),
            ("Há fruta, legumes, peixe e pão fresco.", "Hay fruta, verdura, pescado y pan recién hecho."),
            ("— Bom dia! Quanto custam as laranjas?", "—¡Buenos días! ¿Cuánto cuestan las naranjas?"),
            ("— Dois euros o quilo. São do Algarve.", "—Dos euros el kilo. Son del Algarve."),
            ("— Então quero dois quilos, por favor.", "—Entonces quiero dos kilos, por favor."),
            ("A senhora põe as laranjas num saco e dá-lhe uma maçã de presente.", "La señora pone las naranjas en una bolsa y le regala una manzana."),
            ("O Tony diz: — Muito obrigado! Até para a semana!", "Tony dice: —¡Muchas gracias! ¡Hasta la semana que viene!"),
        ], [
            ("¿Cuándo va Tony al mercado?", ["El sábado por la mañana", "El lunes por la tarde", "Cada noche"], 0),
            ("¿Cuánto paga por las naranjas?", ["Dos euros", "Cuatro euros", "Seis euros"], 1),
            ("¿Qué le regala la señora?", ["Pan", "Una manzana", "Una bolsa"], 1),
        ]),
        ("pt-comboio", "De comboio para o Porto", "A2", [
            ("O Tony quer conhecer o Porto e compra um bilhete de comboio.", "Tony quiere conocer Oporto y compra un billete de tren."),
            ("O comboio sai da estação de Santa Apolónia às oito e meia.", "El tren sale de la estación de Santa Apolónia a las ocho y media."),
            ("A viagem demora quase três horas.", "El viaje dura casi tres horas."),
            ("Pela janela, vê campos verdes, vinhas e pequenas aldeias.", "Por la ventana ve campos verdes, viñedos y pueblos pequeños."),
            ("Ao lado dele está uma estudante de Coimbra que fala espanhol.", "A su lado va una estudiante de Coímbra que habla español."),
            ("Ela recomenda-lhe ver a Ribeira e atravessar a ponte a pé.", "Ella le recomienda ver la Ribeira y cruzar el puente a pie."),
            ("No Porto está frio, mas o Tony acha a cidade linda.", "En Oporto hace frío, pero a Tony la ciudad le parece preciosa."),
        ], [
            ("¿A qué hora sale el tren?", ["A las 8:30", "A las 9:00", "A las 10:30"], 0),
            ("¿Cuánto dura el viaje?", ["Una hora", "Casi tres horas", "Cinco horas"], 1),
            ("¿Qué le recomienda la estudiante?", ["Ir en taxi", "Cruzar el puente a pie", "Volver a Lisboa"], 1),
        ]),
        ("pt-entrevista", "Uma entrevista de trabalho", "A2", [
            ("O Tony tem uma entrevista numa agência de viagens.", "Tony tiene una entrevista en una agencia de viajes."),
            ("A diretora pergunta: — Que línguas fala?", "La directora pregunta: —¿Qué idiomas habla?"),
            ("— Falo espanhol, árabe e inglês, e estou a aprender português.", "—Hablo español, árabe e inglés, y estoy aprendiendo portugués."),
            ("— Tem experiência como guia?", "—¿Tiene experiencia como guía?"),
            ("— Sim, trabalhei como guia no Japão, com grupos de até catorze pessoas.", "—Sí, trabajé como guía en Japón, con grupos de hasta catorce personas."),
            ("A diretora fica interessada, porque muitos clientes vêm do Golfo.", "La directora se interesa, porque muchos clientes vienen del Golfo."),
            ("No fim, diz: — Ligamos-lhe na próxima semana.", "Al final dice: —Le llamamos la semana que viene."),
        ], [
            ("¿Dónde es la entrevista?", ["En un hotel", "En una agencia de viajes", "En un museo"], 1),
            ("¿Dónde trabajó Tony como guía?", ["En Japón", "En Brasil", "En Rusia"], 0),
            ("¿Por qué se interesa la directora?", ["Porque Tony vive cerca", "Porque muchos clientes vienen del Golfo", "Porque Tony es barato"], 1),
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
        ("ru-metro", "В метро", "A1", [
            ("Тони стоит у входа в метро.", "Tony está en la entrada del metro."),
            ("— Извините, как доехать до центра?", "—Perdone, ¿cómo llego al centro?"),
            ("— Садитесь на красную линию. Это три станции.", "—Coja la línea roja. Son tres estaciones."),
            ("— Спасибо! А сколько стоит билет?", "—¡Gracias! ¿Y cuánto cuesta el billete?"),
            ("— Шестьдесят рублей. Можно платить картой.", "—Sesenta rublos. Se puede pagar con tarjeta."),
            ("В метро очень красиво: на станции картины и большие лампы.", "El metro es muy bonito: en la estación hay cuadros y lámparas grandes."),
            ("Через десять минут Тони уже в центре.", "Diez minutos después, Tony ya está en el centro."),
        ], [
            ("¿Qué línea debe coger Tony?", ["La azul", "La roja", "La verde"], 1),
            ("¿Cuántas estaciones son?", ["Tres", "Cinco", "Diez"], 0),
            ("¿Cuánto cuesta el billete?", ["Seis rublos", "Sesenta rublos", "Seiscientos rublos"], 1),
        ]),
        ("ru-magazin", "В магазине", "A1", [
            ("Вечером Тони идёт в магазин рядом с общежитием.", "Por la tarde, Tony va a la tienda cerca de la residencia."),
            ("Ему нужны хлеб, молоко, яйца и яблоки.", "Necesita pan, leche, huevos y manzanas."),
            ("Он не знает, где молоко, и спрашивает продавца.", "No sabe dónde está la leche y le pregunta a la dependienta."),
            ("— Молоко там, слева, рядом с сыром.", "—La leche está allí, a la izquierda, junto al queso."),
            ("На кассе Тони говорит: — Пакет, пожалуйста.", "En la caja, Tony dice: —Una bolsa, por favor."),
            ("Всё стоит четыреста двадцать рублей.", "Todo cuesta cuatrocientos veinte rublos."),
            ("Дома он делает омлет и звонит другу.", "En casa hace una tortilla y llama a un amigo."),
        ], [
            ("¿Dónde está la leche?", ["A la derecha", "A la izquierda, junto al queso", "En la caja"], 1),
            ("¿Qué pide Tony en la caja?", ["Una bolsa", "Agua", "El ticket"], 0),
            ("¿Cuánto cuesta todo?", ["240 rublos", "420 rublos", "4.200 rublos"], 1),
        ]),
        ("ru-kazan", "Зима в Казани", "A2", [
            ("В Казани зима длинная и холодная.", "En Kazán el invierno es largo y frío."),
            ("В январе бывает минус двадцать градусов.", "En enero puede hacer veinte grados bajo cero."),
            ("Тони покупает тёплую куртку, шапку и перчатки.", "Tony se compra una chaqueta de abrigo, un gorro y guantes."),
            ("В субботу он гуляет по Кремлю с друзьями из группы.", "El sábado pasea por el Kremlin con amigos del grupo."),
            ("Они заходят в мечеть Кул-Шариф и долго смотрят на город.", "Entran en la mezquita Kul Sharif y miran la ciudad largo rato."),
            ("Потом пьют горячий чай с чак-чаком — это татарская сладость.", "Después toman té caliente con chak-chak, un dulce tártaro."),
            ("Тони думает: «Холодно, но мне здесь очень нравится».", "Tony piensa: «Hace frío, pero aquí me gusta mucho»."),
        ], [
            ("¿Qué temperatura puede hacer en enero?", ["Cero grados", "Veinte bajo cero", "Diez grados"], 1),
            ("¿Qué se compra Tony?", ["Una bicicleta", "Ropa de abrigo", "Un billete de tren"], 1),
            ("¿Qué es el chak-chak?", ["Una bebida", "Un dulce tártaro", "Una mezquita"], 1),
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
