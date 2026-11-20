"""Inglés B2 para la olimpiada de la Universidad Financiera (Economics) y el inglés B1 de SPbU.

Genera datos/ingb2_a.json. Formato del test real (recomendaciones oficiales de la
Financiera): Listening 10, Reading 10, Vocabulary 15 (phrasal verbs, preposiciones,
idioms) y Grammar 15; 90 minutos, 100 puntos, cada fallo resta 2.

En cada pregunta la opción correcta se escribe PRIMERO; el script la coloca en
una posición equilibrada y baraja los distractores.

Uso: python3 datos/ingb2_gen.py
"""
import json
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))
SETS = []
T_GRAM = "Grammar"
T_PHR = "Phrasal verbs and prepositions"
T_IDI = "Idioms and collocations"
T_WF = "Word formation"
T_READ = "Reading comprehension"
T_LIS = "Listening: true or false"


def mcq(task, sec, lvl, q, opts, e):
    SETS.append({"sec": sec, "task": task, "lvl": lvl, "qs": [{"t": "mcq", "q": q, "o": opts, "e": e}]})


def G(lvl, q, opts, e):
    mcq(T_GRAM, "grammar", lvl, q, opts, e)


def V(task, lvl, q, opts, e):
    mcq(task, "vocab", lvl, q, opts, e)


# ---------------- GRAMMAR (artículos, pronombres, tiempos, formas no personales, modales, condicionales) ----------------
G(2, "Many people wonder whether the company ___ its prices next year.",
  ["will raise", "raises", "has raised", "raised"],
  "Tras «whether» en una pregunta indirecta sobre el futuro va futuro normal: will raise. La regla de «no will tras if/when» es para condiciones, no para preguntas indirectas.")
G(1, "Could you give me ___ about choosing a university?",
  ["some advice", "an advice", "some advices", "a advice"],
  "«Advice» es incontable: nunca lleva «an» ni plural. Se dice «some advice» o «a piece of advice».")
G(2, "It's no use ___ about the delay — the flight has already been cancelled.",
  ["complaining", "to complain", "complain", "complained"],
  "«It's no use» va siempre con -ing: it's no use complaining (no sirve de nada quejarse).")
G(2, "You hardly ever check your email, ___?",
  ["do you", "don't you", "have you", "aren't you"],
  "«Hardly ever» ya es negativo, así que la coletilla va en afirmativo: do you?")
G(2, "I wish I ___ work tomorrow, but unfortunately I do.",
  ["didn't have to", "don't have to", "won't have to", "hadn't to"],
  "Wish + pasado para desear que el presente o el futuro fueran distintos: I wish I didn't have to.")
G(1, "I ___ come to the meeting yesterday because my train was cancelled.",
  ["couldn't", "mustn't", "shouldn't", "needn't"],
  "Imposibilidad en el pasado: couldn't. Mustn't es prohibición y shouldn't es consejo.")
G(1, "I've known Sara ___ we were at school together.",
  ["since", "for", "from", "during"],
  "Since + momento de inicio (since we were at school); for + duración (for ten years).")
G(3, "If the data had been collected properly, the company ___ in a much better position now.",
  ["would be", "would have been", "was", "will be"],
  "Condicional mixto: condición en el pasado (had been collected) y resultado en el presente (now) → would be.")
G(2, "'I'm meeting the director next week.' — 'That ___ be right. She's on a business trip in Brazil until June.'",
  ["can't", "mustn't", "needn't", "shouldn't"],
  "Deducción negativa segura: can't (no puede ser). Mustn't expresa prohibición, no deducción.")
G(2, "The new software ___ next week, so the system will be offline for a day.",
  ["is being installed", "will install", "is been installed", "has installed"],
  "Plan futuro en pasiva: present continuous pasivo, is being installed. El programa no se instala solo (will install es activa) y «is been» no existe.")
G(2, "By the time we arrived at the station, the train ___.",
  ["had already left", "already left", "has already left", "was already leaving"],
  "Acción anterior a otra del pasado (arrived) → past perfect: had already left.")
G(2, "This is the first time I ___ a presentation in English.",
  ["have given", "give", "am giving", "gave"],
  "«This is the first time» exige present perfect: have given.")
G(3, "Not only ___ the project on time, but she also reduced its cost.",
  ["did she finish", "she finished", "she did finish", "finished she"],
  "«Not only» al principio provoca inversión, como en una pregunta: Not only did she finish…")
G(2, "The manager made us ___ the report again.",
  ["rewrite", "to rewrite", "rewriting", "rewritten"],
  "Make + persona + infinitivo SIN to: made us rewrite. (En pasiva sí lleva to: we were made to rewrite.)")
G(2, "She suggested ___ the train instead of flying.",
  ["taking", "to take", "that we taking", "take"],
  "Suggest + -ing (o «suggest that we take»). Nunca «suggest to take».")
G(1, "___ Amazon is the longest river in South America.",
  ["The", "A", "An", "— (no article)"],
  "Ríos, mares y océanos llevan «the»: the Amazon, the Nile, the Pacific.")
G(1, "It took us ___ hour to get to the airport.",
  ["an", "a", "the", "— (no article)"],
  "La h de «hour» no suena, así que la palabra empieza por sonido vocal: an hour (igual que an honest man).")
G(2, "The children had a great time: they really enjoyed ___ at the science museum.",
  ["themselves", "them", "theirselves", "their"],
  "Enjoy necesita objeto: enjoy yourself / enjoy themselves (reflexivo). «Theirselves» no existe.")
G(1, "The engineer ___ designed this bridge has won an international award.",
  ["who", "which", "whom", "whose"],
  "Para personas como sujeto: who (o that). Which es para cosas, whom es objeto y whose es posesivo.")
G(1, "If I ___ you, I would accept the job offer.",
  ["were", "am", "would be", "will be"],
  "Segundo condicional: If + pasado + would. En estilo cuidado se usa «were» con todas las personas: If I were you.")
G(2, "She told me that she ___ the report the day before.",
  ["had finished", "has finished", "finishes", "will finish"],
  "Estilo indirecto: el pasado retrocede a past perfect, y «yesterday» pasa a «the day before».")
G(2, "You ___ bring your passport; an ID card is enough for this trip.",
  ["don't have to", "mustn't", "can't", "shouldn't to"],
  "No es necesario = don't have to. Mustn't significaría «está prohibido».")
G(2, "I'm used to ___ up early for work.",
  ["getting", "get", "got", "have got"],
  "Be used to + -ing = estar acostumbrado a. (Used to + infinitivo es otra cosa: un hábito del pasado.)")
G(3, "Hardly ___ the office when it started to rain.",
  ["had I left", "I had left", "did I leave", "I left"],
  "Hardly … when va con inversión y past perfect: Hardly had I left the office when…")
G(2, "The report, ___ was published last week, has caused a lot of discussion.",
  ["which", "that", "what", "who"],
  "Oración explicativa entre comas: which. «That» no se usa después de una coma.")
G(3, "By 2030, the city ___ a new metro line.",
  ["will have built", "has built", "builds", "is building"],
  "«By + fecha futura» = acción terminada antes de ese momento: future perfect, will have built.")
G(3, "I'd rather you ___ the meeting until Monday.",
  ["postponed", "postpone", "will postpone", "to postpone"],
  "I'd rather + otra persona + pasado: I'd rather you postponed. (Si es la misma persona: I'd rather postpone.)")
G(2, "He apologised ___ late for the interview.",
  ["for being", "to be", "for be", "being"],
  "Apologise for + -ing: he apologised for being late.")

# ---------------- PHRASAL VERBS Y PREPOSICIONES ----------------
V(T_PHR, 1, "The meeting has been ___ until next Friday because the director is ill.",
  ["put off", "put out", "put up", "put on"],
  "Put off = aplazar. Put out = apagar (un fuego), put up = alojar o montar, put on = ponerse (ropa).")
V(T_PHR, 1, "The committee decided to ___ the offer because the price was too high.",
  ["turn down", "turn up", "turn over", "turn into"],
  "Turn down = rechazar (una oferta). Turn up = aparecer o subir el volumen.")
V(T_PHR, 2, "Engineers are ___ tests to make sure the bridge is safe.",
  ["carrying out", "carrying on", "carrying off", "carrying away"],
  "Carry out = llevar a cabo (tests, research, a survey). Carry on = continuar.")
V(T_PHR, 1, "We have ___ paper, so I can't print the tickets.",
  ["run out of", "run into", "run over", "run up"],
  "Run out of = quedarse sin. Run into = encontrarse con alguien por casualidad.")
V(T_PHR, 2, "After years of working for a large firm, she decided to ___ her own business.",
  ["set up", "set off", "set back", "set out"],
  "Set up = montar, fundar (a business, a company). Set off = salir de viaje; set back = retrasar.")
V(T_PHR, 2, "The authorities are ___ the cause of the fire.",
  ["looking into", "looking after", "looking up to", "looking forward to"],
  "Look into = investigar. Look after = cuidar, look up to = admirar, look forward to = esperar con ganas.")
V(T_PHR, 2, "It took him two weeks to ___ the flu.",
  ["get over", "get by", "get through to", "get across"],
  "Get over = recuperarse de, superar (una enfermedad o un mal momento).")
V(T_PHR, 1, "The match was ___ because of the heavy snow.",
  ["called off", "called for", "called on", "called up"],
  "Call off = suspender, cancelar. Call for = exigir; call on = visitar o pedir a alguien que intervenga.")
V(T_PHR, 2, "Can you help me ___ how this new app works?",
  ["figure out", "figure in", "give out", "make up"],
  "Figure out = averiguar, entender cómo funciona algo. Make up = inventar; give out = repartir.")
V(T_PHR, 1, "The car ___ on the motorway and we had to call for help.",
  ["broke down", "broke up", "broke out", "broke in"],
  "Break down = averiarse. Break up = romper o disolverse; break out = estallar (un incendio); break in = entrar a robar.")
V(T_PHR, 2, "She ___ a brilliant idea for reducing waste in the factory.",
  ["came up with", "came across", "came down with", "came round to"],
  "Come up with = idear, proponer. Come across = encontrarse por casualidad; come down with = caer enfermo de.")
V(T_PHR, 2, "Our flight leaves at 6 a.m., so we need to ___ very early.",
  ["set off", "put off", "see off", "show off"],
  "Set off = salir (de viaje). See off = despedir a alguien (necesita objeto); show off = presumir.")
V(T_PHR, 1, "The museum is closed ___ Mondays.",
  ["on", "in", "at", "by"],
  "Días de la semana y fechas: on (on Mondays, on 1 January). In para meses y años; at para horas.")
V(T_PHR, 1, "She is very good ___ solving problems under pressure.",
  ["at", "in", "on", "with"],
  "Good at + -ing o sustantivo: good at solving, good at maths.")
V(T_PHR, 1, "The price of the tickets depends ___ the time of year.",
  ["on", "of", "from", "in"],
  "Depend on (nunca «depend of»).")
V(T_PHR, 2, "He was accused ___ copying his classmate's work.",
  ["of", "for", "with", "about"],
  "Accuse someone OF something. (Ojo: blame someone FOR something.)")
V(T_PHR, 2, "Our department is ___ charge of organising the conference.",
  ["in", "on", "at", "under"],
  "Be in charge of = estar a cargo de.")
V(T_PHR, 2, "I'm not familiar ___ this software yet.",
  ["with", "to", "of", "about"],
  "Familiar WITH = conocer bien algo. (Algo es familiar TO alguien: this face is familiar to me.)")

# ---------------- IDIOMS Y COLLOCATIONS ----------------
V(T_IDI, 1, "Don't worry about the test — it'll be a piece of ___.",
  ["cake", "bread", "pie", "sugar"],
  "A piece of cake = pan comido, muy fácil.")
V(T_IDI, 1, "We only see our cousins once in a blue ___ because they live abroad.",
  ["moon", "sky", "sun", "star"],
  "Once in a blue moon = muy de vez en cuando.")
V(T_IDI, 1, "At the start of the workshop, the trainer told a funny story to break the ___.",
  ["ice", "snow", "rock", "door"],
  "Break the ice = romper el hielo, hacer que la gente se relaje al principio.")
V(T_IDI, 2, "You've hit the nail on the ___ — that's exactly the problem.",
  ["head", "top", "point", "end"],
  "Hit the nail on the head = dar en el clavo.")
V(T_IDI, 2, "I'm feeling a bit under the ___ today, so I'll work from home.",
  ["weather", "rain", "cloud", "sky"],
  "Under the weather = algo pachucho, un poco enfermo.")
V(T_IDI, 1, "A new laptop like that must cost an arm and a ___.",
  ["leg", "hand", "foot", "finger"],
  "Cost an arm and a leg = costar un ojo de la cara.")
V(T_IDI, 1, "Before the trip, we need to ___ a reservation at the hotel.",
  ["make", "do", "take", "give"],
  "Make a reservation / a decision / a mistake / progress. «Do» va con tareas: do homework, do research.")
V(T_IDI, 1, "Scientists ___ a lot of research before the new vaccine was approved.",
  ["did", "made", "took", "gave"],
  "Do research (nunca «make research»).")
V(T_IDI, 2, "The government plans to ___ measures to reduce air pollution.",
  ["take", "make", "do", "put"],
  "Take measures / take steps / take action = tomar medidas.")
V(T_IDI, 2, "As soon as the doctor examined her, he was able to ___ the cause of her headaches.",
  ["diagnose", "define", "decide", "describe"],
  "Diagnose = diagnosticar (la causa de un problema de salud). Define = definir, describe = describir.")
V(T_IDI, 2, "There is a ___ chance of rain this afternoon, so take an umbrella.",
  ["strong", "heavy", "tall", "wide"],
  "Chance se combina con strong, good o high. Heavy va con rain o traffic, no con chance.")
V(T_IDI, 1, "The traffic was so ___ that we missed the beginning of the conference.",
  ["heavy", "strong", "big", "crowded"],
  "Heavy traffic = tráfico denso. Crowded va con lugares: a crowded train, a crowded street.")
V(T_IDI, 1, "Please ___ attention to the safety instructions.",
  ["pay", "make", "do", "take"],
  "Pay attention to = prestar atención a.")
V(T_IDI, 3, "Learning a language takes time, so don't ___ heart if you make mistakes.",
  ["lose", "break", "miss", "drop"],
  "Lose heart = desanimarse.")
V(T_IDI, 2, "The two companies decided to join ___ to develop the new product.",
  ["forces", "arms", "strengths", "powers"],
  "Join forces = unir fuerzas, colaborar.")
V(T_IDI, 3, "I can't make ___ or tail of these instructions.",
  ["head", "top", "face", "front"],
  "Can't make head or tail of something = no entender nada de algo.")

# ---------------- WORD FORMATION ----------------
V(T_WF, 1, "The ___ to close the factory surprised everyone. (DECIDE)",
  ["decision", "decisive", "deciding", "decidedly"],
  "Tras «The» y delante de «to» hace falta un sustantivo: decide → decision.")
V(T_WF, 1, "Thanks to the new system, the team has become much more ___. (EFFECT)",
  ["effective", "effectively", "effectiveness", "effected"],
  "Tras «become much more» hace falta un adjetivo: effective.")
V(T_WF, 1, "The museum is ___ closed on Mondays. (USUAL)",
  ["usually", "usual", "unusual", "usualness"],
  "Modifica al verbo (is closed): hace falta un adverbio, usually.")
V(T_WF, 2, "Her ___ to work long hours impressed the manager. (WILLING)",
  ["willingness", "willing", "willingly", "unwilling"],
  "Es el sujeto de la frase y va tras el posesivo «Her»: sustantivo, willingness.")
V(T_WF, 1, "It is ___ to drive without a licence. (LEGAL)",
  ["illegal", "unlegal", "inlegal", "dislegal"],
  "El contrario de legal es illegal: delante de l se usa il- (illegal, illogical).")
V(T_WF, 1, "The ___ of the new bridge took three years. (CONSTRUCT)",
  ["construction", "constructor", "constructive", "constructively"],
  "El proceso de construir = construction. Constructor es una persona o empresa; constructive es un adjetivo.")
V(T_WF, 2, "The instructions were so ___ that nobody understood what to do. (CLEAR)",
  ["unclear", "clearly", "clarity", "uncleared"],
  "Si nadie entendió, hace falta el adjetivo negativo: unclear.")
V(T_WF, 2, "We need to find a ___ solution to this problem. (PRACTICE)",
  ["practical", "practise", "practically", "practitioner"],
  "Delante del sustantivo «solution» va un adjetivo: practical.")
V(T_WF, 2, "There has been a ___ increase in online sales this year. (SIGNIFY)",
  ["significant", "significance", "signify", "significantly"],
  "Adjetivo delante de «increase»: significant. (Significantly va con un verbo: sales increased significantly.)")
V(T_WF, 3, "The company is looking for ___ staff who can speak three languages. (EXPERIENCE)",
  ["experienced", "experiencing", "inexperience", "experiential"],
  "Personal con experiencia = experienced staff (adjetivo en -ed).")
V(T_WF, 2, "Online shopping offers great ___ for busy people. (CONVENIENT)",
  ["convenience", "conveniently", "inconvenient", "convenient"],
  "Tras «great» y como objeto de «offers» hace falta un sustantivo: convenience.")
V(T_WF, 2, "The new manager is popular because she treats everyone ___. (EQUAL)",
  ["equally", "equal", "equality", "unequal"],
  "Modifica al verbo «treats»: adverbio, equally.")

# ---------------- READING ----------------
def lectura(lvl, passage, qs):
    SETS.append({"sec": "reading", "task": T_READ, "lvl": lvl, "passage": passage,
                 "qs": [{"t": "mcq", "q": q, "o": o, "e": e} for q, o, e in qs]})


lectura(1, """Farming on the rooftops

In many large cities, empty rooftops are being turned into small farms. Supporters say that growing vegetables close to the people who eat them reduces the cost of transport and cuts pollution, because the food does not have to travel hundreds of kilometres by lorry. Rooftop gardens also help to keep buildings cooler in summer, which lowers the amount of energy spent on air conditioning.

However, urban farming is not without problems. Rooftops can only carry a limited weight, so soil must often be replaced with lighter materials, and water has to be pumped up from the ground. As a result, setting up a rooftop farm can be expensive. Critics also point out that these farms produce only a tiny share of the food a city needs.

Even so, many city councils now offer grants to people who want to start one. They argue that the main value of urban farms is not the amount of food they produce but the way they teach city residents, especially children, where their food comes from.""", [
    ("According to the text, rooftop farms reduce pollution because…",
     ["the food travels shorter distances", "they replace lorries with trains", "they use no water at all", "they are cheaper to build than normal farms"],
     "«the food does not have to travel hundreds of kilometres by lorry»: menos transporte, menos contaminación."),
    ("Why can setting up a rooftop farm be expensive?",
     ["Light materials and water pumps are needed", "City councils charge high taxes", "The seeds have to be imported", "Farmers in cities earn higher salaries"],
     "El tejado aguanta poco peso (hay que usar materiales ligeros) y hay que bombear el agua: «As a result, setting up a rooftop farm can be expensive»."),
    ("What do critics say about urban farms?",
     ["They produce very little of a city's food", "They make buildings too hot", "They are dangerous for children", "They use too much energy"],
     "«these farms produce only a tiny share of the food a city needs»."),
    ("According to city councils, the main value of urban farms is…",
     ["educational", "the amount of food they produce", "the money they earn", "the jobs they create"],
     "«not the amount of food… but the way they teach city residents… where their food comes from»: el valor principal es educativo."),
])

lectura(2, """The Trans-Siberian Railway

The Trans-Siberian Railway, which links Moscow with Vladivostok on the Pacific coast, is the longest railway line in the world. It is about 9,300 kilometres long and passes through eight time zones. A non-stop journey takes almost a week.

Construction began in 1891, and the final section was completed in 1916. The work was extremely difficult: builders had to cross wide rivers, lay tracks over frozen ground and cut through mountains near Lake Baikal. Thousands of workers took part, many of them using only simple hand tools.

The railway transformed Siberia. Before it existed, travelling from Moscow to the Pacific could take months by road and river. Once the line opened, new towns grew up along the route, and Siberian timber, grain and coal could be sent to distant markets. Today the railway still carries a large share of Russia's freight, and it is also popular with tourists who want to see the country slowly, from the window of a train.""", [
    ("How long does a non-stop journey along the whole line take?",
     ["Almost a week", "Eight days", "Several months", "About nine hours"],
     "«A non-stop journey takes almost a week». Los «meses» eran lo que se tardaba ANTES del tren."),
    ("Which difficulty of the construction is NOT mentioned in the text?",
     ["A shortage of money", "Wide rivers", "Frozen ground", "Mountains near Lake Baikal"],
     "El texto nombra ríos anchos, suelo helado y montañas junto al Baikal. Del dinero no dice nada."),
    ("What was one effect of the railway on Siberia?",
     ["New towns appeared along the route", "Fewer goods were sent to other regions", "People stopped using rivers completely", "The time zones were changed"],
     "«new towns grew up along the route», y además la madera, el grano y el carbón llegaban a mercados lejanos."),
    ("The word 'freight' in the last paragraph is closest in meaning to…",
     ["goods that are transported", "passengers", "fuel", "tickets"],
     "Freight = mercancías transportadas (carga). Se contrapone a los turistas de la misma frase."),
])

lectura(2, """Working from home

Since 2020, millions of office workers around the world have started working from home for at least part of the week. For many of them, the biggest benefit is time: instead of spending an hour or more travelling to and from the office, they can start work as soon as they have had breakfast. Some companies have also found that employees who work from home take fewer days off.

Yet remote work also has disadvantages. Some people find it hard to separate their job from their private life, and they end up checking emails late in the evening. Others miss the informal conversations with colleagues that often lead to new ideas. Young employees, in particular, say that it is harder to learn from experienced staff when they cannot simply walk over to their desks and ask a question.

For these reasons, many firms have chosen a hybrid model, in which staff spend two or three days in the office and the rest at home. Whether this compromise will last is still unclear, but few experts expect a complete return to the old five-day office week.""", [
    ("According to the text, the biggest benefit of working from home for many people is…",
     ["saving travel time", "earning a higher salary", "receiving fewer emails", "working fewer hours"],
     "«the biggest benefit is time: instead of spending an hour or more travelling…»."),
    ("Why do young employees find remote work difficult?",
     ["It is harder to learn from experienced colleagues", "They cannot afford good computers", "They are not allowed to work from home", "They have to travel more"],
     "«it is harder to learn from experienced staff when they cannot simply walk over to their desks»."),
    ("What is a 'hybrid model', as described in the text?",
     ["Spending part of the week in the office and part at home", "Working only from home", "Working for two different companies", "Changing offices every week"],
     "«staff spend two or three days in the office and the rest at home»."),
    ("What do most experts expect, according to the last paragraph?",
     ["The five-day office week will not fully return", "Everyone will soon work from home full-time", "The hybrid model will end next year", "Companies will close all their offices"],
     "«few experts expect a complete return to the old five-day office week»: no creen que vuelva del todo."),
])

# ---------------- LISTENING (verdadero / falso) ----------------
def escucha(lvl, audio, qs):
    SETS.append({"sec": "listening", "task": T_LIS, "lvl": lvl, "audio": audio,
                 "qs": [{"t": "mcq", "q": q, "o": ["True", "False"], "a": 0 if v else 1, "e": e} for q, v, e in qs]})


escucha(1, """M: Today I'm talking to Anna, who moved from the city to a small village two years ago. Anna, did your friends think you would regret it?
W: Oh yes. Most of them were sure I would miss my job in the city. In fact, I still do the same job; I just work online now.
M: And do you see your friends less?
W: Actually, I see them more than before. When I lived in the city we were all too busy, but now they come and stay with me for whole weekends.
M: How do you get on with the people in the village?
W: Very well. My neighbours helped me to repair the roof when I arrived, and now I teach their children English twice a week.
M: Is there anything you don't like?
W: The transport. There's only one bus a day to the nearest town, so I really need my car.""", [
    ("Anna's friends thought she would miss her job.", True,
     "«Most of them were sure I would miss my job in the city»: verdadero."),
    ("Anna changed her profession when she moved.", False,
     "«I still do the same job; I just work online now»: sigue con el mismo trabajo. Falso."),
    ("She sees her friends less often than before.", False,
     "«I see them more than before»: los ve más. Falso."),
    ("Her neighbours helped her when she arrived.", True,
     "«My neighbours helped me to repair the roof when I arrived»: verdadero."),
    ("There is a good bus service to the nearest town.", False,
     "«There's only one bus a day»: el autobús es malo, por eso necesita el coche. Falso."),
])

escucha(2, """W: Hello, and welcome to the travel advice line. My name is Lucy, and this week we are answering questions about travelling by train in Europe.
M: Hi Lucy. I'm going from Madrid to Paris next month. Is it cheaper to book early?
W: Usually, yes. Tickets often go on sale three months before the journey, and the cheapest seats disappear first. If you wait until the last week, you can pay twice as much.
M: Do I need to print my ticket?
W: Not any more on most routes. A ticket on your phone is enough, but make sure the battery is charged, and keep a screenshot of the ticket just in case.
M: And what about luggage? Is there a limit?
W: On most high-speed trains you can take two large suitcases and one small bag. Just remember that you will have to lift them onto the rack yourself.""", [
    ("Lucy says that booking early is usually cheaper.", True,
     "«Is it cheaper to book early? — Usually, yes»: verdadero."),
    ("Tickets usually go on sale one month before the journey.", False,
     "Dice «three months before the journey», no uno. Falso: fíjate siempre en los números."),
    ("Tickets bought in the last week can cost twice as much.", True,
     "«If you wait until the last week, you can pay twice as much»: verdadero."),
    ("Passengers must always print their tickets.", False,
     "«Not any more on most routes. A ticket on your phone is enough»: falso."),
    ("On most high-speed trains, staff lift your suitcases for you.", False,
     "«you will have to lift them onto the rack yourself»: lo haces tú. Falso."),
])


def escribir():
    rnd = random.Random(2027)
    errores, k = [], 0
    for s in SETS:
        for q in s["qs"]:
            if not q.get("e"):
                errores.append(f"sin explicación: {q['q'][:50]}")
            if "a" in q:          # verdadero/falso: ya viene con su índice
                continue
            o = q["o"]
            if len(o) != 4 or len(set(o)) != 4:
                errores.append(f"opciones: {q['q'][:50]} → {o}")
                continue
            buena, dist = o[0], o[1:]
            rnd.shuffle(dist)
            pos = k % 4
            k += 1
            q["o"], q["a"] = dist[:pos] + [buena] + dist[pos:], pos
            if "___" not in q["q"] and s["sec"] in ("grammar", "vocab"):
                errores.append(f"falta el hueco ___: {q['q'][:50]}")
    if errores:
        raise SystemExit("ERRORES en ingb2_gen:\n" + "\n".join(errores))
    with open(os.path.join(AQUI, "ingb2_a.json"), "w", encoding="utf-8") as f:
        json.dump(SETS, f, ensure_ascii=False, indent=1)
    from collections import Counter
    nq = sum(len(s["qs"]) for s in SETS)
    print(f"ingb2: {len(SETS)} sets, {nq} preguntas")
    print("  por tarea:", dict(Counter(s["task"] for s in SETS for _ in s["qs"])))


if __name__ == "__main__":
    escribir()
