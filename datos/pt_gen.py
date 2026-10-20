"""Portugués de Portugal para hispanohablantes: supervivencia, trámites para vivir allí
y falsos amigos. Portugués EUROPEO (no de Brasil). Se añade a www/kana.json.

Uso: python3 datos/kana_gen.py && python3 datos/vocab_gen.py && python3 datos/pt_gen.py
"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Tema → [(portugués, español, frase, traducción, pista de pronunciación o "")]
PT = {
    "Lo básico": [
        ("Olá", "hola", "Olá! Tudo bem?", "¡Hola! ¿Todo bien?", "La h no suena: «oLÁ»."),
        ("Bom dia / Boa tarde / Boa noite", "buenos días / tardes / noches", "Bom dia! Um café, por favor.", "¡Buenos días! Un café, por favor.", "«bom» casi «bõ», nasal."),
        ("Obrigado / Obrigada", "gracias (lo dice un hombre / una mujer)", "Obrigado! — De nada.", "¡Gracias! — De nada.", "Concuerda con quien HABLA, no con quien escucha."),
        ("Por favor", "por favor", "Fala mais devagar, por favor.", "Habla más despacio, por favor.", ""),
        ("Desculpe", "perdone", "Desculpe, não percebi.", "Perdone, no he entendido.", ""),
        ("Com licença", "con permiso", "Com licença, posso passar?", "Con permiso, ¿puedo pasar?", ""),
        ("Sim / Não", "sí / no", "Não, não, não. Obrigado.", "No, no, no. Gracias.", "«não» suena «nãu», nasal."),
        ("Não percebo", "no entiendo", "Não percebo nada, mas sorrio.", "No entiendo nada, pero sonrío.", "En Portugal «perceber» = entender (en Brasil, «entender»)."),
        ("Fala espanhol?", "¿habla español?", "Fala espanhol? Não? Então em português!", "¿Habla español? ¿No? ¡Pues en portugués!", ""),
        ("Até logo / Até amanhã", "hasta luego / hasta mañana", "Até amanhã, se o comboio deixar.", "Hasta mañana, si el tren me deja.", ""),
        ("Está bem", "vale / de acuerdo", "Está bem, está bem… amanhã faço.", "Vale, vale… mañana lo hago.", ""),
        ("Fixe", "guay (coloquial)", "A tua casa é muito fixe!", "¡Tu casa mola mucho!", "Palabra muy portuguesa; en Brasil dicen «legal»."),
    ],
    "Comer y comprar": [
        ("Pequeno-almoço", "desayuno", "O pequeno-almoço é um café e um pastel de nata.", "El desayuno es un café y un pastel de nata.", ""),
        ("Almoço / Jantar", "comida / cena", "O jantar é às oito. Ou às nove. Ou às dez.", "La cena es a las ocho. O a las nueve. O a las diez.", ""),
        ("Uma bica", "un café solo (Lisboa)", "Uma bica e a conta, por favor.", "Un café solo y la cuenta, por favor.", "En Oporto se dice «um cimbalino»."),
        ("A conta", "la cuenta", "A conta? Já? Ainda não comi a sobremesa!", "¿La cuenta? ¿Ya? ¡Aún no he tomado el postre!", ""),
        ("Sem carne de porco", "sin cerdo", "Tem alguma coisa sem carne de porco?", "¿Tiene algo sin cerdo?", "Útil para comer halal: pregunta también por «banha» (manteca)."),
        ("Peixe / Frango", "pescado / pollo", "Peixe grelhado, outra vez. Estamos em Portugal.", "Pescado a la parrilla, otra vez. Estamos en Portugal.", ""),
        ("Água com gás / sem gás", "agua con / sin gas", "Água sem gás, natural, por favor.", "Agua sin gas, del tiempo, por favor.", "«natural» = a temperatura ambiente; «fresca» = fría."),
        ("Quanto custa?", "¿cuánto cuesta?", "Quanto custa? … Ah, afinal não quero.", "¿Cuánto cuesta? … Ah, pues no lo quiero.", ""),
        ("Supermercado / Mercearia", "supermercado / tienda de barrio", "A mercearia da esquina sabe a minha vida toda.", "La tienda de la esquina sabe toda mi vida.", ""),
        ("Talho", "carnicería", "Há um talho halal perto da mesquita.", "Hay una carnicería halal cerca de la mezquita.", ""),
        ("Saco", "bolsa", "Quer saco? São dez cêntimos.", "¿Quiere bolsa? Son diez céntimos.", ""),
        ("Talão", "ticket de compra", "Guarde o talão, por favor.", "Guarde el ticket, por favor.", "Al pagar te preguntan «Contribuinte?»: es tu NIF para la factura."),
    ],
    "Moverse": [
        ("Comboio", "tren", "O comboio para Coimbra está atrasado. Que surpresa.", "El tren a Coimbra va con retraso. Qué sorpresa.", "En Brasil es «trem»; en Portugal SIEMPRE «comboio»."),
        ("Autocarro", "autobús", "O autocarro passou e não parou.", "El autobús pasó y no paró.", "Brasil: «ônibus». Portugal: «autocarro»."),
        ("Elétrico", "tranvía", "O elétrico 28 está cheio de turistas. Como sempre.", "El tranvía 28 está lleno de turistas. Como siempre.", ""),
        ("Metro", "metro", "Onde é a estação de metro mais perto?", "¿Dónde está la estación de metro más cercana?", ""),
        ("Bilhete / Passe", "billete / abono mensual", "Com o passe navegante viajo por toda a Lisboa.", "Con el abono Navegante viajo por toda Lisboa.", ""),
        ("Paragem", "parada (de bus)", "A paragem é ali, depois da subida. Tudo é subida.", "La parada está ahí, después de la cuesta. Todo es cuesta.", ""),
        ("À direita / À esquerda / Em frente", "a la derecha / izquierda / recto", "Sempre em frente e depois… pergunte outra vez.", "Todo recto y luego… vuelva a preguntar.", ""),
        ("Perto / Longe", "cerca / lejos", "É perto, cinco minutos. (São vinte.)", "Está cerca, cinco minutos. (Son veinte.)", ""),
        ("Onde fica…?", "¿dónde queda…?", "Onde fica a mesquita central?", "¿Dónde queda la mezquita central?", ""),
        ("Carro / Boleia", "coche / llevar a alguien en coche", "Dás-me boleia até à faculdade?", "¿Me llevas en coche a la facultad?", "«boleia» = aventón, autostop."),
    ],
    "Casa y estudio": [
        ("Quarto", "habitación", "Procuro um quarto perto da faculdade.", "Busco una habitación cerca de la facultad.", ""),
        ("Renda", "alquiler (mensualidad)", "A renda é 335 euros, com despesas incluídas?", "El alquiler son 335 euros, ¿con gastos incluidos?", "En Portugal «renda» = alquiler, no ingresos."),
        ("Senhorio", "casero", "O senhorio só responde à noite.", "El casero solo contesta por la noche.", ""),
        ("Caução", "fianza", "A caução é de dois meses?", "¿La fianza es de dos meses?", "«ção» suena «sãu»."),
        ("Despesas", "gastos (luz, agua, internet)", "As despesas estão incluídas na renda?", "¿Los gastos están incluidos en el alquiler?", ""),
        ("Casa de banho", "baño", "Onde é a casa de banho?", "¿Dónde está el baño?", "Brasil: «banheiro»."),
        ("Frigorífico", "nevera", "O frigorífico é partilhado. A comida desaparece.", "La nevera es compartida. La comida desaparece.", ""),
        ("Faculdade / Aula", "facultad / clase", "A aula começa às nove em ponto. Em teoria.", "La clase empieza a las nueve en punto. En teoría.", ""),
        ("Matrícula / Inscrição", "matrícula / inscripción", "A inscrição no curso de férias já está aberta.", "La inscripción en el curso de verano ya está abierta.", ""),
        ("Propina", "tasa de matrícula (lo que se paga)", "A propina paga-se em duas prestações.", "La matrícula se paga en dos plazos.", "Falso amigo: «propina» NO es la propina; la propina es «gorjeta»."),
        ("Trabalho de casa", "deberes", "Fiz o trabalho de casa… quase todo.", "Hice los deberes… casi todos.", ""),
    ],
    "Salud y emergencias": [
        ("Centro de saúde", "centro de salud", "Tenho de marcar consulta no centro de saúde.", "Tengo que pedir cita en el centro de salud.", ""),
        ("Marcar consulta", "pedir cita", "Queria marcar uma consulta, por favor.", "Quería pedir una cita, por favor.", "«Queria» (condicional educado) es lo normal para pedir."),
        ("Farmácia", "farmacia", "A farmácia de serviço está aberta toda a noite.", "La farmacia de guardia abre toda la noche.", ""),
        ("Dói-me aqui", "me duele aquí", "Dói-me aqui… e ali… e a carteira.", "Me duele aquí… y ahí… y la cartera.", ""),
        ("Constipado", "resfriado", "Estou constipado, não venho à aula.", "Estoy resfriado, no voy a clase.", "Falso amigo: «constipado» = resfriado (¡no estreñido!)."),
        ("Ajuda!", "¡socorro!", "Ajuda! Liguem para o 112!", "¡Socorro! ¡Llamad al 112!", "112: emergencias en toda la UE."),
        ("Seguro de saúde", "seguro médico", "O meu seguro de saúde cobre isto?", "¿Mi seguro médico cubre esto?", ""),
    ],
    "Hablar como allí": [
        ("Pá", "tío / hombre (muletilla)", "Pá, não sei, pá.", "Tío, no sé, tío.", "La muletilla más portuguesa que existe."),
        ("Bué", "mucho (jerga de Lisboa)", "Isto é bué de caro!", "¡Esto es carísimo!", ""),
        ("Giro / Gira", "bonito / mono", "Que cão tão giro!", "¡Qué perro tan mono!", ""),
        ("Chato", "pesado / aburrido", "Que chato, está a chover outra vez.", "Qué rollo, está lloviendo otra vez.", ""),
        ("Estou a + verbo", "estoy …-ando (Portugal)", "Estou a estudar. Juro.", "Estoy estudiando. Lo juro.", "Portugal: «estou a estudar». Brasil: «estou estudando»."),
        ("Se calhar", "a lo mejor", "Se calhar amanhã chove. Se calhar não.", "A lo mejor mañana llueve. A lo mejor no.", ""),
        ("Já está!", "¡listo! / ¡ya está!", "Já está! Inscrição feita.", "¡Listo! Inscripción hecha.", ""),
        ("Pois", "pues sí / claro", "— Está calor. — Pois.", "— Hace calor. — Pues sí.", "Respuesta comodín: «pois, pois»."),
        ("Saudade", "nostalgia, echar de menos", "Tenho saudades de Osaka e do takoyaki.", "Echo de menos Osaka y el takoyaki.", "La palabra más famosa del portugués."),
    ],
}

# Falsos amigos: (portugués, lo que significa, la trampa en español)
FALSOS = [
    ("Esquisito", "raro", "No es «exquisito». Si la comida está rica, di «delicioso»."),
    ("Polvo", "pulpo", "No es polvo de suciedad: el polvo es «pó»."),
    ("Rato", "ratón", "No es «un rato»: un rato es «um bocado»."),
    ("Exquisito", "—", "Ojo al revés: «esquisito» = raro. Para rico, «delicioso»."),
    ("Embaraçada", "avergonzada", "No es embarazada: embarazada es «grávida»."),
    ("Constipado", "resfriado", "No es estreñido: estreñido es «com prisão de ventre»."),
    ("Propina", "tasa de matrícula", "La propina del camarero es «gorjeta»."),
    ("Apelido", "apellido", "No es apodo: el apodo es «alcunha»."),
    ("Escritório", "oficina", "No es escritorio (mueble): el mueble es «secretária»."),
    ("Secretária", "escritorio (mueble) o secretaria", "«Está na secretária» puede ser «está en la mesa»."),
    ("Borracha", "goma de borrar", "No es una persona ebria."),
    ("Ninho", "nido", "No es «niño»: niño es «criança» o «miúdo»."),
    ("Taça", "copa (de fútbol, de helado)", "Una taza de café es «chávena»."),
    ("Copo", "vaso (para beber)", "No es copo de nieve: el copo es «floco»."),
    ("Vaso", "maceta / jarrón", "El vaso para beber es «copo»."),
    ("Largo", "ancho / plaza", "Largo (de longitud) se dice «comprido»."),
    ("Ligar", "llamar por teléfono", "«Liga-me amanhã» = llámame mañana. No es ligar con alguien."),
    ("Acordar", "despertar", "«Acordo às sete» = me despierto a las siete."),
    ("Prender", "detener, arrestar / sujetar", "Encender la luz es «acender»."),
    ("Pegar", "coger, agarrar", "Pegar a alguien es «bater»."),
    ("Ofício", "carta oficial / oficio", "Un oficio en la Administración es un documento."),
    ("Cena", "escena", "La cena es «jantar»."),
    ("Salada", "ensalada", "Salada = ensalada; salado es «salgado»."),
    ("Presunto", "jamón", "No es presunto culpable."),
    ("Rua", "calle", "No es «ruta»: la ruta es «percurso» o «rota»."),
]

# Trámites para vivir en Portugal como ciudadano de la UE
TRAMITES = [
    ("NIF", "número fiscal: lo piden para alquilar, abrir cuenta, el móvil y hasta en el súper", "Se pide en Finanças (o por un representante). Es lo primero."),
    ("Finanças", "Hacienda portuguesa", "Ahí se saca el NIF y se declaran ingresos."),
    ("Certificado de Registo de Cidadão da UE", "registro de residente UE", "Obligatorio si te quedas más de 3 meses. Se pide en la Câmara Municipal (unos 15 €)."),
    ("Câmara Municipal", "ayuntamiento", "Ahí va el Certificado de Registo."),
    ("Junta de Freguesia", "junta de barrio (distrito)", "Da el «atestado de residência» que piden en muchos trámites."),
    ("Atestado de residência", "certificado de empadronamiento", "Lo da la Junta de Freguesia; suelen pedir dos testigos o el contrato."),
    ("Segurança Social / NISS", "Seguridad Social / su número", "Necesario para trabajar o darte de alta como autónomo."),
    ("Recibos verdes", "facturas de autónomo", "Sistema para trabajar por tu cuenta (guía, web…). Se emiten en el Portal das Finanças."),
    ("SNS / Número de utente", "sistema de salud / número de paciente", "Con la residencia te inscribes en el centro de salud y te dan el número de utente."),
    ("Cartão Europeu de Seguro de Doença", "Tarjeta Sanitaria Europea", "Cubre lo urgente mientras sigues asegurado en España."),
    ("IBAN / Conta bancária", "cuenta bancaria", "Para abrirla: pasaporte o DNI, NIF y comprobante de domicilio."),
    ("Contrato de arrendamento", "contrato de alquiler", "Pide que esté registrado en Finanças: te sirve como comprobante de domicilio."),
    ("Comprovativo de morada", "comprobante de domicilio", "Contrato, factura de luz o atestado de la Junta."),
    ("Marcação", "cita previa", "Casi todo va con «marcação». Pide cita pronto: hay lista de espera."),
    ("Senha", "número de turno (y también contraseña)", "«Tire uma senha» = coja número y espere."),
    ("Balcão", "ventanilla / mostrador", "«Dirija-se ao balcão 3» = vaya a la ventanilla 3."),
    ("Cartão de Cidadão", "DNI portugués", "Solo para portugueses; a ti te piden pasaporte o DNI español."),
    ("CIPLE / CAPLE", "exámenes oficiales de portugués (A2 y otros niveles)", "El CIPLE (A2) es el que se pide para la nacionalidad. Lo organiza la Universidad de Lisboa."),
]


def validar():
    vistos = set()
    for tema, lista in PT.items():
        for e in lista:
            assert len(e) == 5 and all(e[:4]), (tema, e)
            assert e[0] not in vistos, e[0]
            vistos.add(e[0])
    assert len({f[0] for f in FALSOS}) == len(FALSOS)
    for t in TRAMITES:
        assert len(t) == 3 and all(t), t


def main():
    validar()
    ruta = os.path.join(RAIZ, "www", "kana.json")
    datos = json.load(open(ruta, encoding="utf-8"))
    datos["pt"] = [{"c": c, "m": m, "f": f, "fe": fe, "t": t, "g": tema} for tema, lista in PT.items() for (c, m, f, fe, t) in lista]
    datos["falsos"] = [{"c": c, "m": m, "t": t, "g": "Falsos amigos"} for (c, m, t) in FALSOS if m != "—"]
    datos["tramites"] = [{"c": c, "m": m, "t": t, "g": "Trámites"} for (c, m, t) in TRAMITES]
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    print(f"pt: {len(datos['pt'])} · falsos amigos: {len(datos['falsos'])} · trámites: {len(datos['tramites'])}")


if __name__ == "__main__":
    main()
