"""Genera www/kana.json: hiragana, katakana y los kanji del N5 con un truco
para memorizar cada uno. Escrito a mano (sin IA de pago); se valida aquí mismo.

Uso: python3 datos/kana_gen.py
"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (romaji, hiragana, truco hiragana, katakana, truco katakana)
BASICOS = [
    ("a", "あ", "Una «a» con una cruz delante: un altar con su vela.", "ア", "Un «a»rco de flecha visto de lado."),
    ("i", "い", "Dos palitos juntos, como las dos «i» de «iiih».", "イ", "Un hombre de pie inclinado: «i»nclinado."),
    ("u", "う", "Una oreja con un pelo encima: «¿uh?», ¿qué has dicho?", "ウ", "う con tejado: una «u» con techo."),
    ("e", "え", "Un pájaro exótico: «e»xótico.", "エ", "Una viga en forma de I tumbada: «e»levador."),
    ("o", "お", "Un golfista dando a la bola: «o», ¡qué golpe!", "オ", "Un hombre que tira algo: «o», ¡cuidado!"),
    ("ka", "か", "Alguien que corta con un «ka»tana: el corte y la gota.", "カ", "Como か sin la gota: una «ka»tana sola."),
    ("ki", "き", "Una «ki»ave (llave) con dos dientes.", "キ", "Una llave sencilla: la «ki» de key."),
    ("ku", "く", "El pico de un «cu»co abierto.", "ク", "Un «cu»chillo doblado que corta en ángulo."),
    ("ke", "け", "Un «ke»g (barril) con su grifo.", "ケ", "La letra K torcida: «ke»."),
    ("ko", "こ", "Dos gusanos «co»ntentos, uno encima del otro.", "コ", "Una esquina, como un «co»do."),
    ("sa", "さ", "Un «sa»murái con una espada cruzada.", "サ", "Una mesa con dos patas: «sa»lsa encima."),
    ("shi", "し", "Un anzuelo: «shi», hemos pescado.", "シ", "Una cara que sonríe mirando hacia arriba: «shi», gotas que suben."),
    ("su", "す", "Un columpio con un lazo: «su»be y baja.", "ス", "Un hombre que corre: «su»dando."),
    ("se", "せ", "Una boca que muestra un diente: «se» ve el diente.", "セ", "Como せ pero más simple: «se»ñal de stop."),
    ("so", "そ", "Un zigzag de «so»nido que viaja.", "ソ", "Dos rayas que caen hacia abajo: «so»l que baja (mira: de arriba abajo)."),
    ("ta", "た", "Una «ta»bla con las letras t y a.", "タ", "Como ク con una raya: una «ta»rta cortada."),
    ("chi", "ち", "Un número 5 dado la vuelta: «chi»ste raro.", "チ", "Una «chi»ca con los brazos abiertos."),
    ("tsu", "つ", "Una ola de «tsu»nami.", "ツ", "Tres gotas que caen de lado: «tsu»nami (las gotas van hacia abajo, no como シ)."),
    ("te", "て", "Una «te»la colgando de una cuerda.", "テ", "Un «te»léfono con su antena."),
    ("to", "と", "Un dedo del pie con una astilla: «to»ca.", "ト", "Un «tó»tem con una rama."),
    ("na", "な", "Una monja rezando: «na»da más.", "ナ", "Una cruz con el brazo caído: «na»da."),
    ("ni", "に", "Una rodilla con su línea: «ni» (knee).", "ニ", "Dos rayas: «ni» es el 2 en japonés."),
    ("nu", "ぬ", "Unos fideos con palillos: «nu»dles.", "ヌ", "Unos palillos cruzados: «nu»dles otra vez."),
    ("ne", "ね", "Un gato (neko) con la cola enroscada: «ne».", "ネ", "Una «ne»cesaria percha con gancho."),
    ("no", "の", "Una señal de prohibido: «no».", "ノ", "Una sola raya diagonal: «no» hay más."),
    ("ha", "は", "Una «ha»macha entre dos palos: «ja ja».", "ハ", "Dos palos que se abren al reír: «ha»."),
    ("hi", "ひ", "Una boca que sonríe: «hi», hola.", "ヒ", "Una persona sentada que dice «hi»."),
    ("fu", "ふ", "El monte «Fu»ji con nubes alrededor.", "フ", "Un gancho como el «fu»ego que sube."),
    ("he", "へ", "Una montaña pequeña: «he», ya llegué arriba.", "ヘ", "Igual que la hiragana: la misma montaña."),
    ("ho", "ほ", "Un «ho»mbre con un palo al lado de は.", "ホ", "Una cruz con dos patas: un «ho»rmiguero."),
    ("ma", "ま", "Una «ma»má con dos brazos cruzados.", "マ", "Una «ma»ma con la cabeza inclinada."),
    ("mi", "み", "El número 21 escrito deprisa: «mi»l.", "ミ", "Tres rayas: «mi» de «mitsu» (3)."),
    ("mu", "む", "Una vaca diciendo «mu».", "ム", "La nariz de una vaca: «mu»."),
    ("me", "め", "Un ojo (me) con una pestaña cruzada.", "メ", "Una cruz en el ojo: «me»."),
    ("mo", "も", "Un anzuelo con dos líneas: pescar «mo»re (más).", "モ", "Igual que も con una línea recta: más «mo»derna."),
    ("ya", "や", "Un «ya»k con cuernos.", "ヤ", "Un «ya»k más sencillo, de lado."),
    ("yu", "ゆ", "Un pez con aleta: «yu» (unicornio de mar).", "ユ", "Una «U» cuadrada tumbada: «yu»."),
    ("yo", "よ", "Un «yo»-yo colgando de la mano.", "ヨ", "Una E al revés: «yo» al revés."),
    ("ra", "ら", "Un «ra»pero con la gorra puesta.", "ラ", "Un 7 con sombrero: «ra»yo."),
    ("ri", "り", "Dos «ri»os que corren juntos.", "リ", "Como り pero más recto: los «ri»os en línea."),
    ("ru", "る", "Una «ru»ta con un lazo al final.", "ル", "Dos piernas que corren: «ru»n."),
    ("re", "れ", "Un hombre que se arrodilla: «re»zar.", "レ", "Una L inclinada: «re»."),
    ("ro", "ろ", "Como る sin el lazo: un «ro»llo cortado.", "ロ", "Una caja: «ro»bot cuadrado."),
    ("wa", "わ", "Un «wa»sh: alguien lavando con la mano.", "ワ", "Una taza vista de lado: «wa», qué rica el agua."),
    ("wo", "を", "Un hombre que se tira de cabeza: «wo»ah. Suena como «o».", "ヲ", "Como フ con una raya: «wo»."),
    ("n", "ん", "Una «n» escrita a mano.", "ン", "Una gota y una raya que sube: «n» (la raya sube, no como ソ)."),
]

# Con ゛ (dakuten) y ゜ (handakuten): mismas formas que las básicas
DAKUTEN = [
    ("ga", "が", "ガ"), ("gi", "ぎ", "ギ"), ("gu", "ぐ", "グ"), ("ge", "げ", "ゲ"), ("go", "ご", "ゴ"),
    ("za", "ざ", "ザ"), ("ji", "じ", "ジ"), ("zu", "ず", "ズ"), ("ze", "ぜ", "ゼ"), ("zo", "ぞ", "ゾ"),
    ("da", "だ", "ダ"), ("ji (di)", "ぢ", "ヂ"), ("zu (du)", "づ", "ヅ"), ("de", "で", "デ"), ("do", "ど", "ド"),
    ("ba", "ば", "バ"), ("bi", "び", "ビ"), ("bu", "ぶ", "ブ"), ("be", "べ", "ベ"), ("bo", "ぼ", "ボ"),
    ("pa", "ぱ", "パ"), ("pi", "ぴ", "ピ"), ("pu", "ぷ", "プ"), ("pe", "ぺ", "ペ"), ("po", "ぽ", "ポ"),
]

# Combinaciones (yōon): consonante + ゃゅょ pequeña
COMBOS = []
for base_r, hi, ka in [("k", "き", "キ"), ("sh", "し", "シ"), ("ch", "ち", "チ"), ("n", "に", "ニ"),
                       ("h", "ひ", "ヒ"), ("m", "み", "ミ"), ("r", "り", "リ"), ("g", "ぎ", "ギ"),
                       ("j", "じ", "ジ"), ("b", "び", "ビ"), ("p", "ぴ", "ピ")]:
    for v, sh, sk in [("a", "ゃ", "ャ"), ("u", "ゅ", "ュ"), ("o", "ょ", "ョ")]:
        r = base_r + ("y" if base_r not in ("sh", "ch", "j") else "") + v
        COMBOS.append((r, hi + sh, ka + sk))

# (kanji, significado, on'yomi, kun'yomi, palabra de ejemplo, lectura, significado, truco)
KANJI = [
    ("一", "uno", "イチ", "ひと(つ)", "一つ", "ひとつ", "uno (cosa)", "Una raya = uno."),
    ("二", "dos", "ニ", "ふた(つ)", "二人", "ふたり", "dos personas", "Dos rayas = dos."),
    ("三", "tres", "サン", "みっ(つ)", "三月", "さんがつ", "marzo", "Tres rayas = tres."),
    ("四", "cuatro", "シ", "よん・よ(つ)", "四時", "よじ", "las cuatro", "Una ventana con cuatro lados y cortinas."),
    ("五", "cinco", "ゴ", "いつ(つ)", "五日", "いつか", "día 5", "Un 5 con tejado y suelo."),
    ("六", "seis", "ロク", "むっ(つ)", "六百", "ろっぴゃく", "seiscientos", "Una persona con sombrero y piernas abiertas."),
    ("七", "siete", "シチ", "なな(つ)", "七時", "しちじ", "las siete", "Un 7 al revés cruzado."),
    ("八", "ocho", "ハチ", "やっ(つ)", "八百", "はっぴゃく", "ochocientos", "Dos rayas que se abren, como el 8 cortado por la mitad."),
    ("九", "nueve", "キュウ・ク", "ここの(つ)", "九時", "くじ", "las nueve", "Un hombre que da una patada: ¡nueve goles!"),
    ("十", "diez", "ジュウ", "とお", "十日", "とおか", "día 10", "Una cruz: el 10 romano es X."),
    ("百", "cien", "ヒャク", "—", "三百", "さんびゃく", "trescientos", "Un uno encima de 白 (blanco): cien canas blancas."),
    ("千", "mil", "セン", "ち", "千円", "せんえん", "mil yenes", "Diez (十) con un pelo encima."),
    ("万", "diez mil", "マン", "—", "一万円", "いちまんえん", "diez mil yenes", "Un billete que se dobla: diez mil."),
    ("円", "yen, círculo", "エン", "まる(い)", "百円", "ひゃくえん", "cien yenes", "Una cartera abierta con el dinero dentro."),
    ("日", "día, sol", "ニチ・ジツ", "ひ・か", "日曜日", "にちようび", "domingo", "Un sol cuadrado con una raya en medio."),
    ("月", "luna, mes", "ゲツ・ガツ", "つき", "月曜日", "げつようび", "lunes", "Una luna creciente con dos nubes."),
    ("火", "fuego", "カ", "ひ", "火曜日", "かようび", "martes", "Una hoguera con chispas a los lados."),
    ("水", "agua", "スイ", "みず", "水曜日", "すいようび", "miércoles", "Un río que salpica a los lados."),
    ("木", "árbol", "モク・ボク", "き", "木曜日", "もくようび", "jueves", "Un árbol con sus raíces."),
    ("金", "oro, dinero", "キン", "かね", "金曜日", "きんようび", "viernes", "Un tejado que guarda pepitas de oro."),
    ("土", "tierra", "ド・ト", "つち", "土曜日", "どようび", "sábado", "Una planta que sale de la tierra."),
    ("曜", "día de la semana", "ヨウ", "—", "何曜日", "なんようび", "¿qué día?", "Sol (日) + pájaros: el día en que vuelan."),
    ("年", "año", "ネン", "とし", "去年", "きょねん", "el año pasado", "Una persona con un saco de arroz: la cosecha de cada año."),
    ("時", "hora", "ジ", "とき", "時間", "じかん", "tiempo", "Sol (日) + templo (寺): la campana que da la hora."),
    ("分", "minuto, entender", "フン・ブン", "わ(かる)", "五分", "ごふん", "cinco minutos", "Un cuchillo (刀) que parte en dos (八)."),
    ("半", "mitad", "ハン", "なか(ば)", "三時半", "さんじはん", "las tres y media", "Una vaca cortada por la mitad."),
    ("今", "ahora", "コン", "いま", "今日", "きょう", "hoy", "Un tejado y alguien que llega ahora."),
    ("午", "mediodía", "ゴ", "—", "午後", "ごご", "por la tarde", "Como 牛 (vaca) pero sin cuerno: al mediodía se le cae."),
    ("前", "antes, delante", "ゼン", "まえ", "名前", "なまえ", "nombre", "Cuernos + luna + cuchillo: lo que va delante."),
    ("後", "después, detrás", "ゴ", "あと・うし(ろ)", "後で", "あとで", "después", "Alguien que se queda atrás con hilo en los pies."),
    ("週", "semana", "シュウ", "—", "来週", "らいしゅう", "la semana que viene", "Un camino (辶) que da la vuelta: la semana."),
    ("毎", "cada", "マイ", "—", "毎日", "まいにち", "cada día", "Una madre (母) con sombrero: cada día igual."),
    ("何", "qué", "カ", "なに・なん", "何時", "なんじ", "¿qué hora?", "Una persona (亻) con una pregunta (可)."),
    ("人", "persona", "ジン・ニン", "ひと", "日本人", "にほんじん", "japonés (persona)", "Dos piernas que caminan."),
    ("男", "hombre", "ダン", "おとこ", "男の子", "おとこのこ", "chico", "Campo (田) + fuerza (力): quien trabaja el campo."),
    ("女", "mujer", "ジョ", "おんな", "女の人", "おんなのひと", "mujer", "Una persona sentada con las piernas cruzadas."),
    ("子", "niño", "シ", "こ", "子ども", "こども", "niño", "Un bebé con los brazos abiertos."),
    ("父", "padre", "フ", "ちち", "お父さん", "おとうさん", "padre", "Un padre que cruza los brazos."),
    ("母", "madre", "ボ", "はは", "お母さん", "おかあさん", "madre", "Una madre con dos puntos: el pecho."),
    ("友", "amigo", "ユウ", "とも", "友だち", "ともだち", "amigo", "Dos manos que se dan la mano."),
    ("名", "nombre", "メイ", "な", "名前", "なまえ", "nombre", "Noche (夕) + boca (口): de noche dices tu nombre."),
    ("口", "boca", "コウ", "くち", "入口", "いりぐち", "entrada", "Una boca abierta y cuadrada."),
    ("目", "ojo", "モク", "め", "一つ目", "ひとつめ", "el primero", "Un ojo vertical con dos rayas."),
    ("耳", "oreja", "ジ", "みみ", "耳", "みみ", "oreja", "Una oreja con sus pliegues."),
    ("手", "mano", "シュ", "て", "上手", "じょうず", "hábil", "Una mano con los dedos abiertos."),
    ("足", "pie, pierna", "ソク", "あし", "足", "あし", "pie", "Una rodilla (口) encima de un pie."),
    ("上", "arriba", "ジョウ", "うえ・あ(がる)", "上手", "じょうず", "hábil", "Una flecha que apunta arriba."),
    ("下", "abajo", "カ・ゲ", "した・さ(がる)", "地下鉄", "ちかてつ", "metro", "Una flecha que apunta abajo."),
    ("中", "dentro, medio", "チュウ", "なか", "中国", "ちゅうごく", "China", "Una flecha que atraviesa el centro de la caja."),
    ("外", "fuera", "ガイ", "そと", "外国", "がいこく", "extranjero", "Noche (夕) + adivino (卜): fuera, de noche."),
    ("右", "derecha", "ウ", "みぎ", "右", "みぎ", "derecha", "Mano + boca: con la derecha se come."),
    ("左", "izquierda", "サ", "ひだり", "左", "ひだり", "izquierda", "Mano + herramienta (工): la otra mano."),
    ("東", "este", "トウ", "ひがし", "東京", "とうきょう", "Tokio", "El sol (日) sale tras el árbol (木): el este."),
    ("西", "oeste", "セイ・サイ", "にし", "関西", "かんさい", "Kansai", "Un pájaro que vuelve al nido al atardecer: el oeste."),
    ("南", "sur", "ナン", "みなみ", "南口", "みなみぐち", "salida sur", "Una tienda bajo el sol del sur."),
    ("北", "norte", "ホク", "きた", "北海道", "ほっかいどう", "Hokkaidō", "Dos personas de espaldas por el frío del norte."),
    ("大", "grande", "ダイ・タイ", "おお(きい)", "大学", "だいがく", "universidad", "Una persona con los brazos bien abiertos: ¡así de grande!"),
    ("小", "pequeño", "ショウ", "ちい(さい)・こ", "小学校", "しょうがっこう", "escuela primaria", "Un palito con dos gotas: pequeño."),
    ("高", "alto, caro", "コウ", "たか(い)", "高校", "こうこう", "instituto", "Un edificio alto con tejado."),
    ("安", "barato, tranquilo", "アン", "やす(い)", "安い", "やすい", "barato", "Una mujer (女) bajo un techo: tranquila."),
    ("新", "nuevo", "シン", "あたら(しい)", "新聞", "しんぶん", "periódico", "Árbol + hacha: madera recién cortada."),
    ("古", "viejo", "コ", "ふる(い)", "古い", "ふるい", "viejo", "Diez (十) bocas (口): lo que han contado diez generaciones."),
    ("長", "largo, jefe", "チョウ", "なが(い)", "社長", "しゃちょう", "presidente", "Un anciano con el pelo largo."),
    ("白", "blanco", "ハク", "しろ(い)", "白い", "しろい", "blanco", "Un rayo de luz sobre el sol (日): blanco."),
    ("多", "mucho", "タ", "おお(い)", "多い", "おおい", "mucho", "Dos noches (夕) una encima de otra: muchas noches."),
    ("少", "poco", "ショウ", "すく(ない)・すこ(し)", "少し", "すこし", "un poco", "Pequeño (小) con un trozo que se cae."),
    ("山", "montaña", "サン", "やま", "富士山", "ふじさん", "monte Fuji", "Tres picos de montaña."),
    ("川", "río", "セン", "かわ", "川", "かわ", "río", "Tres líneas de agua que corren."),
    ("田", "arrozal", "デン", "た", "田中さん", "たなかさん", "Sr. Tanaka", "Un campo de arroz dividido en cuatro."),
    ("天", "cielo", "テン", "あめ", "天気", "てんき", "el tiempo", "Una persona grande (大) bajo el cielo (一)."),
    ("気", "espíritu, aire", "キ", "—", "元気", "げんき", "con energía", "Vapor que sube del arroz."),
    ("雨", "lluvia", "ウ", "あめ", "雨", "あめ", "lluvia", "Gotas que caen bajo una nube."),
    ("花", "flor", "カ", "はな", "花火", "はなび", "fuegos artificiales", "Hierba (艹) que cambia (化): una flor."),
    ("電", "electricidad", "デン", "—", "電車", "でんしゃ", "tren", "Lluvia (雨) + un rayo que cae."),
    ("車", "coche", "シャ", "くるま", "電車", "でんしゃ", "tren", "Un carro visto desde arriba con sus ruedas."),
    ("駅", "estación", "エキ", "—", "駅", "えき", "estación", "Un caballo (馬): antes la estación era de caballos."),
    ("道", "camino", "ドウ", "みち", "道", "みち", "calle", "Una cabeza (首) que avanza por el camino (辶)."),
    ("国", "país", "コク", "くに", "外国", "がいこく", "extranjero", "Un rey con su joya (玉) dentro de una frontera."),
    ("学", "estudiar", "ガク", "まな(ぶ)", "学生", "がくせい", "estudiante", "Un niño (子) bajo un tejado lleno de libros."),
    ("校", "escuela", "コウ", "—", "学校", "がっこう", "escuela", "Árbol (木) + intercambio (交): la escuela de madera."),
    ("生", "vida, nacer", "セイ", "い(きる)・う(まれる)", "先生", "せんせい", "profesor", "Una planta que nace de la tierra."),
    ("先", "antes, adelante", "セン", "さき", "先週", "せんしゅう", "la semana pasada", "Una persona que va un paso por delante."),
    ("本", "libro, origen", "ホン", "もと", "日本", "にほん", "Japón", "Un árbol (木) con una marca en la raíz: el origen."),
    ("語", "idioma", "ゴ", "かた(る)", "日本語", "にほんご", "japonés", "Palabras (言) de cinco (五) bocas (口)."),
    ("話", "hablar", "ワ", "はな(す)", "電話", "でんわ", "teléfono", "Palabras (言) + lengua (舌)."),
    ("言", "decir", "ゲン", "い(う)", "言う", "いう", "decir", "Una boca (口) con las ondas de lo que dice."),
    ("読", "leer", "ドク", "よ(む)", "読む", "よむ", "leer", "Palabras (言) que se venden (売): leer."),
    ("書", "escribir", "ショ", "か(く)", "図書館", "としょかん", "biblioteca", "Una mano con pincel sobre el papel."),
    ("聞", "oír, preguntar", "ブン", "き(く)", "新聞", "しんぶん", "periódico", "Una oreja (耳) en la puerta (門)."),
    ("見", "ver", "ケン", "み(る)", "見る", "みる", "ver", "Un ojo (目) con piernas: va a ver."),
    ("食", "comer", "ショク", "た(べる)", "食べ物", "たべもの", "comida", "Un tejado sobre un cuenco de arroz."),
    ("飲", "beber", "イン", "の(む)", "飲み物", "のみもの", "bebida", "Comer (食) + boca abierta (欠): beber."),
    ("行", "ir", "コウ", "い(く)", "銀行", "ぎんこう", "banco", "Un cruce de caminos."),
    ("来", "venir", "ライ", "く(る)", "来年", "らいねん", "el año que viene", "Un árbol con frutos: viene la cosecha."),
    ("出", "salir", "シュツ", "で(る)・だ(す)", "出口", "でぐち", "salida", "Dos montañas, una sobre otra: salir del valle."),
    ("入", "entrar", "ニュウ", "はい(る)・い(れる)", "入口", "いりぐち", "entrada", "Una persona (人) que se agacha para entrar."),
    ("休", "descansar", "キュウ", "やす(む)", "休み", "やすみ", "vacaciones", "Una persona (亻) apoyada en un árbol (木)."),
    ("買", "comprar", "バイ", "か(う)", "買い物", "かいもの", "compras", "Una red sobre una concha (貝): las conchas eran dinero."),
    ("立", "ponerse de pie", "リツ", "た(つ)", "立つ", "たつ", "levantarse", "Una persona de pie sobre el suelo."),
    ("会", "reunirse", "カイ", "あ(う)", "会社", "かいしゃ", "empresa", "Gente bajo un mismo tejado."),
    ("社", "empresa, santuario", "シャ", "—", "会社", "かいしゃ", "empresa", "Un altar (ネ) sobre la tierra (土)."),
    ("店", "tienda", "テン", "みせ", "店", "みせ", "tienda", "Un tejado con un puesto de adivino (占) debajo."),
    ("間", "intervalo", "カン", "あいだ", "時間", "じかん", "tiempo", "El sol (日) que entra entre las puertas (門)."),
    ("空", "cielo, vacío", "クウ", "そら", "空港", "くうこう", "aeropuerto", "Un agujero con trabajo (工): el cielo vacío."),
]


def validar():
    roma = [b[0] for b in BASICOS]
    assert len(BASICOS) == 46, len(BASICOS)
    assert len(set(roma)) == 46, "romaji repetido"
    assert len(DAKUTEN) == 25 and len(COMBOS) == 33
    for b in BASICOS:
        assert len(b[1]) == 1 and len(b[3]) == 1, b
    ks = [k[0] for k in KANJI]
    assert len(ks) == len(set(ks)), [k for k in ks if ks.count(k) > 1]
    for k in KANJI:
        assert len(k) == 8 and all(k), k
        assert k[0] in k[4] or k[4] == k[0], f"{k[0]} no sale en su ejemplo {k[4]}"


def main():
    validar()
    datos = {
        "hira": [{"r": b[0], "c": b[1], "t": b[2]} for b in BASICOS]
        + [{"r": d[0], "c": d[1], "g": "dakuten"} for d in DAKUTEN]
        + [{"r": c[0], "c": c[1], "g": "combo"} for c in COMBOS],
        "kata": [{"r": b[0], "c": b[3], "t": b[4]} for b in BASICOS]
        + [{"r": d[0], "c": d[2], "g": "dakuten"} for d in DAKUTEN]
        + [{"r": c[0], "c": c[2], "g": "combo"} for c in COMBOS],
        "kanji": [{"c": k[0], "m": k[1], "on": k[2], "kun": k[3], "w": k[4], "wr": k[5], "wm": k[6], "t": k[7]}
                  for k in KANJI],
    }
    ruta = os.path.join(RAIZ, "www", "kana.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    print(f"kana.json: {len(datos['hira'])} hiragana, {len(datos['kata'])} katakana, {len(KANJI)} kanji")


if __name__ == "__main__":
    main()
