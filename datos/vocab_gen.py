"""Vocabulario esencial del N5 con frases para reír (y no olvidar), más un bloque de
Kansai-ben y frases de «matón de película». Escrito a mano; se añade a www/kana.json.

Uso: python3 datos/kana_gen.py && python3 datos/vocab_gen.py
"""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Tema → [(palabra, lectura, significado, frase, traducción, versión de Kansai o "")]
VOCAB = {
    "Lo básico": [
        ("はい", "はい", "sí", "はい、わかりました。…わかってないけど。", "Sí, entendido. …No he entendido nada.", "せや"),
        ("いいえ", "いいえ", "no", "いいえ、ねていません。めを とじて いるだけです。", "No, no duermo. Solo tengo los ojos cerrados.", "ちゃう"),
        ("すみません", "すみません", "perdón / disculpe", "すみません、もう いちど。…もう いちど。", "Perdone, otra vez. …Otra vez.", "すんまへん"),
        ("ありがとう", "ありがとう", "gracias", "ありがとう。でも いりません。", "Gracias. Pero no lo quiero.", "おおきに"),
        ("おはよう", "おはよう", "buenos días", "おはよう。もう ひるだけど。", "Buenos días. Aunque ya es mediodía.", ""),
        ("こんにちは", "こんにちは", "hola / buenas tardes", "こんにちは。かねを かえして ください。", "Hola. Devuélveme el dinero, por favor.", "まいど"),
        ("こんばんは", "こんばんは", "buenas noches (saludo)", "こんばんは。また きみか。", "Buenas noches. Otra vez tú.", ""),
        ("さようなら", "さようなら", "adiós", "さようなら。にどと こないで。", "Adiós. No vuelvas nunca.", "ほな"),
        ("おやすみなさい", "おやすみなさい", "buenas noches (al dormir)", "おやすみなさい。あしたも はやいですよ。", "Buenas noches. Mañana también madrugas.", ""),
        ("いただきます", "いただきます", "que aproveche (antes de comer)", "いただきます。あ、それ わたしの です。", "Que aproveche. Ah, eso es mío.", ""),
        ("ごちそうさま", "ごちそうさま", "gracias por la comida", "ごちそうさま。おかねは かれが はらいます。", "Gracias por la comida. Paga él.", ""),
        ("だいじょうぶ", "だいじょうぶ", "estoy bien / no pasa nada", "だいじょうぶ、だいじょうぶ。たぶん。", "Tranquilo, tranquilo. Creo.", ""),
        ("だめ", "だめ", "no vale / prohibido", "だめです。ぜったいに だめ。…まあ、いいか。", "No. De ninguna manera. …Bueno, vale.", "あかん"),
        ("ほんとう", "ほんとう", "verdad / de verdad", "ほんとうですか。うそでしょう。", "¿De verdad? Mentira, ¿no?", "ほんま"),
        ("ちがいます", "ちがいます", "no es así / se equivoca", "ちがいます。わたしは にんじゃでは ありません。", "No. No soy un ninja.", "ちゃいます"),
    ],
    "Personas": [
        ("わたし", "わたし", "yo", "わたしは てんさいです。じぶんで いいます。", "Soy un genio. Lo digo yo.", "うち"),
        ("あなた", "あなた", "tú / usted", "あなたは だれですか。なぜ わたしの いえに いますか。", "¿Quién eres? ¿Por qué estás en mi casa?", "じぶん"),
        ("ひと", "人", "persona", "あの ひとは いつも いそがしい ふりを します。", "Esa persona siempre finge estar ocupada.", ""),
        ("ともだち", "友だち", "amigo", "ともだちは ひとり います。ねこです。", "Tengo un amigo. Es un gato.", "つれ"),
        ("せんせい", "先生", "profesor / doctor", "せんせい、しゅくだいは いぬが たべました。", "Profe, el perro se comió los deberes.", ""),
        ("がくせい", "学生", "estudiante", "がくせいです。べんきょうは あしたから。", "Soy estudiante. Estudio a partir de mañana.", ""),
        ("かぞく", "家族", "familia", "かぞくは みんな うるさいです。わたしも。", "En mi familia todos son ruidosos. Yo también.", ""),
        ("ちち / おとうさん", "父 / お父さん", "padre (mío / de otro)", "おとうさんの じょうだんは さむいです。", "Los chistes de papá dan frío.", "おとん"),
        ("はは / おかあさん", "母 / お母さん", "madre (mía / de otro)", "おかあさんは なんでも しっています。こわい。", "Mamá lo sabe todo. Da miedo.", "おかん"),
        ("あに / おにいさん", "兄 / お兄さん", "hermano mayor", "あには わたしの プリンを たべました。", "Mi hermano mayor se comió mi flan.", ""),
        ("あね / おねえさん", "姉 / お姉さん", "hermana mayor", "あねは いつも ただしいです。と いいます。", "Mi hermana siempre tiene razón. Eso dice.", ""),
        ("おとうと", "弟", "hermano menor", "おとうとは ゲームが じょうずです。べんきょうは へたです。", "Mi hermano pequeño es bueno en juegos. En estudiar, malo.", ""),
        ("いもうと", "妹", "hermana menor", "いもうとの へやは ジャングルです。", "La habitación de mi hermana pequeña es una jungla.", ""),
        ("こども", "子ども", "niño", "こどもは げんきです。おとなは つかれて います。", "Los niños tienen energía. Los adultos, cansancio.", ""),
        ("おとこ / おんな", "男 / 女", "hombre / mujer", "おとこの ひとが ないています。たまねぎです。", "Un hombre está llorando. Es la cebolla.", ""),
        ("いしゃ", "医者", "médico", "いしゃは「やすんで ください」と いいました。むりです。", "El médico dijo «descanse». Imposible.", ""),
        ("けいさつ", "警察", "policía", "けいさつです。とまって ください。…はしらないで！", "¡Policía! Pare, por favor. …¡No corra!", ""),
    ],
    "Tiempo": [
        ("いま", "今", "ahora", "いま、いきます。（まだ いえ）", "Ya voy. (Sigue en casa.)", ""),
        ("きょう", "今日", "hoy", "きょうは なにも しません。あしたも。", "Hoy no hago nada. Mañana tampoco.", ""),
        ("あした", "明日", "mañana", "あしたから がんばります。まいにち そう いいます。", "Desde mañana me esfuerzo. Lo digo cada día.", ""),
        ("きのう", "昨日", "ayer", "きのうの ことは おぼえて いません。べんりです。", "Lo de ayer no lo recuerdo. Qué práctico.", ""),
        ("あさ", "朝", "mañana (parte del día)", "あさは きらいです。あさも わたしが きらいです。", "Odio la mañana. Y la mañana me odia a mí.", ""),
        ("ひる", "昼", "mediodía", "ひるごはんの あとで ねむく なります。", "Después de comer me entra sueño.", ""),
        ("よる", "夜", "noche", "よる に なると、れいぞうこが よびます。", "Por la noche, la nevera me llama.", ""),
        ("まいにち", "毎日", "cada día", "まいにち ラーメンです。けんこうは あしたから。", "Ramen cada día. La salud, a partir de mañana.", ""),
        ("いつも", "いつも", "siempre", "かれは いつも おくれます。けっこんしきにも。", "Siempre llega tarde. Hasta a su boda.", ""),
        ("ときどき", "時々", "a veces", "ときどき べんきょうします。ときどき。", "A veces estudio. A veces.", ""),
        ("あとで", "後で", "luego / después", "あとで やります。（やりません）", "Luego lo hago. (No lo hará.)", ""),
        ("はやく", "早く", "pronto / rápido", "はやく！でんしゃが いきますよ！", "¡Rápido! ¡Que se va el tren!", "はよ"),
        ("〜じ / 〜ふん", "〜時 / 〜分", "… en punto / … minutos", "しちじ ごふんです。でんしゃは もう いません。", "Son las 7:05. El tren ya no está.", ""),
        ("しゅうまつ", "週末", "fin de semana", "しゅうまつは ずっと ねます。けいかくです。", "El finde duermo sin parar. Es un plan.", ""),
        ("やすみ", "休み", "descanso / vacaciones", "やすみの ひも しごとの メールが きます。", "En el día libre también llegan correos del trabajo.", ""),
    ],
    "Comida": [
        ("ごはん", "ご飯", "arroz / comida", "ごはん まだ？ もう にじかん まって います。", "¿Aún no está la comida? Llevo dos horas esperando.", "めし"),
        ("たべもの", "食べ物", "comida", "たべものの しゃしんを とって、たべるのを わすれました。", "Hice fotos a la comida y olvidé comérmela.", ""),
        ("のみもの", "飲み物", "bebida", "のみものは みずで いいです。ただですから。", "De beber, agua. Porque es gratis.", ""),
        ("みず", "水", "agua", "みずを ください。なまぬるくても いいです。", "Agua, por favor. Aunque esté tibia.", ""),
        ("おちゃ", "お茶", "té", "おちゃが こい。にがい。でも のみます。", "El té está fuerte. Amargo. Pero me lo bebo.", ""),
        ("コーヒー", "コーヒー", "café", "コーヒーを さんばい のみました。いま、とべます。", "Me tomé tres cafés. Ahora puedo volar.", ""),
        ("ぎゅうにゅう", "牛乳", "leche", "ぎゅうにゅうの きげんは きのうでした。", "La leche caducó ayer.", ""),
        ("パン", "パン", "pan", "パンを かいに いって、ケーキを かいました。", "Fui a por pan y compré pastel.", ""),
        ("たまご", "卵", "huevo", "たまごが われました。わたしの こころも。", "Se rompió el huevo. Y mi corazón.", ""),
        ("にく", "肉", "carne", "にくは ハラールですか。きいて みます。", "¿La carne es halal? Voy a preguntar.", ""),
        ("さかな", "魚", "pescado", "さかなは すきです。ほねは きらいです。", "Me gusta el pescado. Las espinas, no.", ""),
        ("やさい", "野菜", "verdura", "やさいも たべて ください。ケチャップは やさいでは ありません。", "Come verdura también. El kétchup no es verdura.", ""),
        ("くだもの", "果物", "fruta", "にほんの くだものは たかい。メロンは ほうせきです。", "La fruta en Japón es cara. El melón es una joya.", ""),
        ("おいしい", "おいしい", "rico", "おいしい！…ねだんを みるまでは。", "¡Qué rico! …Hasta ver el precio.", "うまい"),
        ("あまい", "甘い", "dulce", "この ケーキは あまい。きみの かんがえも あまい。", "Este pastel es dulce. Y tu plan, ingenuo.", ""),
        ("からい", "辛い", "picante", "からくない と いいましたよね？", "Dijiste que no picaba, ¿verdad?", ""),
        ("おなか", "お腹", "barriga", "おなかが すきました。さっき たべましたけど。", "Tengo hambre. Aunque acabo de comer.", ""),
        ("たべる", "食べる", "comer", "よる じゅうにじに たべるのは ひみつです。", "Comer a las 12 de la noche es un secreto.", "くう"),
        ("のむ", "飲む", "beber", "くすりを のんで ください。ジュースじゃ ありません。", "Tómate la medicina. No es zumo.", ""),
    ],
    "Lugares": [
        ("いえ / うち", "家", "casa", "うちが いちばん。そとは さむい。", "Como en casa, nada. Fuera hace frío.", ""),
        ("へや", "部屋", "habitación", "へやが せまい。でも やちんは ひろい。", "La habitación es pequeña. Pero el alquiler, enorme.", ""),
        ("がっこう", "学校", "escuela", "がっこうは たのしい。やすみの ひは。", "La escuela es divertida. En vacaciones.", ""),
        ("かいしゃ", "会社", "empresa / oficina", "かいしゃに いきたくない。でも いきます。", "No quiero ir a la oficina. Pero voy.", ""),
        ("えき", "駅", "estación", "えきで まいごに なりました。さんかい めです。", "Me perdí en la estación. Es la tercera vez.", ""),
        ("みせ", "店", "tienda", "この みせは たかい。かんばんも たかい。", "Esta tienda es cara. Hasta el cartel es alto.", ""),
        ("コンビニ", "コンビニ", "tienda 24 h", "コンビニは わたしの れいぞうこです。", "El konbini es mi nevera.", ""),
        ("びょういん", "病院", "hospital", "びょういん と びよういん は ちがいます！", "¡Hospital (byōin) y peluquería (biyōin) no son lo mismo!", ""),
        ("ぎんこう", "銀行", "banco", "ぎんこうは さんじに しまります。いつも わすれます。", "El banco cierra a las tres. Siempre se me olvida.", ""),
        ("トイレ", "トイレ", "baño", "トイレは どこですか。いそいで います！", "¿Dónde está el baño? ¡Tengo prisa!", ""),
        ("みち", "道", "camino / calle", "この みちで いいですか。グーグルは「はい」と いいます。", "¿Es por esta calle? Google dice que sí.", ""),
        ("こうえん", "公園", "parque", "こうえんで はとに ごはんを とられました。", "En el parque una paloma me quitó la comida.", ""),
        ("やま / うみ", "山 / 海", "montaña / mar", "やまに いきましょう。…やっぱり うみ。", "Vamos a la montaña. …Mejor al mar.", ""),
        ("ここ / そこ / あそこ", "ここ / そこ / あそこ", "aquí / ahí / allí", "かぎは どこ？ ここ？ そこ？ …ポケットだ。", "¿Las llaves? ¿Aquí? ¿Ahí? …En el bolsillo.", ""),
        ("どこ", "どこ", "dónde", "ここは どこ？ わたしは だれ？", "¿Dónde estoy? ¿Quién soy?", ""),
        ("みぎ / ひだり", "右 / 左", "derecha / izquierda", "みぎ…いや、ひだり…いや、まっすぐ。", "Derecha… no, izquierda… no, recto.", ""),
        ("まえ / うしろ", "前 / 後ろ", "delante / detrás", "うしろに だれか いますよ。…じょうだんです。", "Hay alguien detrás de ti. …Es broma.", ""),
        ("うえ / した", "上 / 下", "arriba / abajo", "ねこは いつも いちばん うえに います。", "El gato siempre está en lo más alto.", ""),
        ("なか / そと", "中 / 外", "dentro / fuera", "そとは あめ。なかは ふとん。けってい。", "Fuera llueve. Dentro, futón. Decidido.", ""),
    ],
    "Moverse": [
        ("でんしゃ", "電車", "tren", "でんしゃで ねて、しゅうてんまで いきました。", "Me dormí en el tren y llegué al final de la línea.", ""),
        ("ちかてつ", "地下鉄", "metro", "ちかてつの ちずは スパゲッティです。", "El mapa del metro es un plato de espaguetis.", ""),
        ("バス", "バス", "autobús", "バスが きません。わたしの きもちも。", "El autobús no viene. Mis ganas tampoco.", ""),
        ("くるま", "車", "coche", "くるまは ありません。じてんしゃが あります。いきが あります。", "No tengo coche. Tengo bici. Y pulmones.", ""),
        ("じてんしゃ", "自転車", "bicicleta", "おおさかの じてんしゃは しんごうを みません。", "Las bicis de Osaka no miran los semáforos.", "チャリ"),
        ("ひこうき", "飛行機", "avión", "ひこうきの ごはんは すきです。へんですか。", "Me gusta la comida del avión. ¿Soy raro?", ""),
        ("きっぷ", "切符", "billete", "きっぷを なくしました。ポケットの なかでした。", "Perdí el billete. Estaba en el bolsillo.", ""),
        ("いく", "行く", "ir", "どこに いきますか。かえりたいです。", "¿Adónde vamos? Yo quiero volver.", ""),
        ("くる", "来る", "venir", "かれは きません。いつも そうです。", "Él no viene. Siempre igual.", ""),
        ("かえる", "帰る", "volver (a casa)", "もう かえります。まだ ごじですけど。", "Ya me voy a casa. Aunque son las cinco.", ""),
        ("あるく", "歩く", "andar", "えきまで あるいて ごふん。と ふどうさんやは いいました。", "Cinco minutos andando a la estación. Eso dijo la inmobiliaria.", ""),
        ("はしる", "走る", "correr", "でんしゃの ために はしりました。ドアが しまりました。", "Corrí por el tren. Se cerró la puerta.", ""),
        ("のる / おりる", "乗る / 降りる", "subir / bajar (de vehículo)", "まちがえた でんしゃに のりました。つぎで おります。", "Me subí al tren equivocado. Me bajo en la próxima.", ""),
        ("とおい / ちかい", "遠い / 近い", "lejos / cerca", "「ちかいですよ」と いって、さんじゅっぷん あるきました。", "«Está cerca», dijo, y anduvimos treinta minutos.", ""),
    ],
    "Cosas": [
        ("ほん", "本", "libro", "ほんを かいました。よんで いません。", "Compré un libro. No lo he leído.", ""),
        ("かばん", "かばん", "bolso / mochila", "かばんの なかに なんでも あります。かぎ いがい。", "En mi bolso hay de todo. Menos las llaves.", ""),
        ("かぎ", "鍵", "llave", "かぎを いえの なかに わすれました。", "Me dejé las llaves dentro de casa.", ""),
        ("でんわ", "電話", "teléfono", "でんわに でません。メールも みません。わたしです。", "No contesto al teléfono ni miro el correo. Así soy yo.", ""),
        ("おかね", "お金", "dinero", "おかねが ありません。でも げんきです。", "No tengo dinero. Pero tengo salud.", "ゼニ"),
        ("かさ", "傘", "paraguas", "かさを もって いない ひだけ、あめが ふります。", "Solo llueve los días que no llevo paraguas.", ""),
        ("とけい", "時計", "reloj", "とけいは ありますが、じかんは ありません。", "Tengo reloj, pero no tengo tiempo.", ""),
        ("つくえ / いす", "机 / 椅子", "mesa / silla", "いすに すわって、つくえで ねます。", "Me siento en la silla y duermo en la mesa.", ""),
        ("ふく", "服", "ropa", "ふくが たくさん あります。きる ふくは ありません。", "Tengo mucha ropa. Y nada que ponerme.", ""),
        ("くつ", "靴", "zapatos", "にほんでは いえで くつを ぬいで ください！", "¡En Japón, quítate los zapatos en casa!", ""),
        ("しゃしん", "写真", "foto", "しゃしんでは わかく みえます。じつぶつは…", "En la foto parezco joven. En persona…", ""),
        ("テレビ", "テレビ", "tele", "テレビを みながら ねました。テレビは おきて います。", "Me dormí viendo la tele. La tele sigue despierta.", ""),
        ("パソコン", "パソコン", "ordenador", "パソコンが おそい。わたしも おそい。", "El ordenador va lento. Yo también.", ""),
        ("てがみ", "手紙", "carta", "てがみを かきました。メールで おくりました。", "Escribí una carta. La mandé por correo electrónico.", ""),
        ("なまえ", "名前", "nombre", "おなまえは？ …ちょっと わすれました。", "¿Su nombre? …Se me ha olvidado un momento.", ""),
    ],
    "Verbos del día": [
        ("みる", "見る", "ver / mirar", "なにを みて いますか。…なにも。", "¿Qué estás mirando? …Nada.", ""),
        ("きく", "聞く", "oír / preguntar", "きいて いますか？ …はい（きいて いない）", "¿Me escuchas? …Sí. (No escucha.)", ""),
        ("はなす", "話す", "hablar", "にほんごを はなします。すこし。とても すこし。", "Hablo japonés. Un poco. Muy poco.", ""),
        ("いう", "言う", "decir", "「かんたん」と いう ひとは ぜんぶ うそつきです。", "Todos los que dicen «es fácil» mienten.", "ゆう"),
        ("よむ", "読む", "leer", "メニューを よみました。しゃしんで えらびます。", "He leído la carta. Elijo por las fotos.", ""),
        ("かく", "書く", "escribir", "かんじを かきました。だれも よめません。わたしも。", "Escribí un kanji. Nadie lo entiende. Ni yo.", ""),
        ("かう", "買う", "comprar", "やすかったので みっつ かいました。いりません。", "Como era barato compré tres. No los necesito.", ""),
        ("まつ", "待つ", "esperar", "まって！ …まってって いったのに。", "¡Espera! …Te dije que esperaras.", ""),
        ("ねる", "寝る", "dormir / acostarse", "はやく ねます。と いって、にじまで スマホ。", "«Me acuesto pronto», y con el móvil hasta las dos.", ""),
        ("おきる", "起きる", "levantarse", "ろくじに おきました。ろくじ ごふんに また ねました。", "Me levanté a las seis. A las seis y cinco, otra vez a dormir.", ""),
        ("する", "する", "hacer", "なにも しない のも しごとです。", "No hacer nada también es un trabajo.", ""),
        ("べんきょうする", "勉強する", "estudiar", "べんきょうして います。（ユーチューブ）", "Estoy estudiando. (YouTube.)", ""),
        ("はたらく", "働く", "trabajar", "はたらきたくない。でも たべたい。", "No quiero trabajar. Pero quiero comer.", ""),
        ("わかる", "分かる", "entender", "わかりましたか？ …はい（ぜんぜん）", "¿Lo has entendido? …Sí. (Nada.)", ""),
        ("しる", "知る", "saber / conocer", "しりません。しりたくも ありません。", "No lo sé. Ni quiero saberlo.", ""),
        ("ある / いる", "ある / いる", "haber (cosas / seres vivos)", "おかねは ありません。ねこは います。", "Dinero no hay. Gato, sí.", "おる"),
        ("あう", "会う", "quedar / ver a alguien", "あいたかった！ …だれでしたっけ？", "¡Qué ganas de verte! …¿Quién eras?", ""),
        ("あそぶ", "遊ぶ", "jugar / divertirse", "おとなも あそびたいです。", "Los adultos también quieren jugar.", ""),
        ("つかれる", "疲れる", "cansarse", "なにも して いないのに つかれました。", "Estoy cansado sin haber hecho nada.", "しんどい"),
        ("わすれる", "忘れる", "olvidar", "なにを わすれたか わすれました。", "He olvidado qué he olvidado.", ""),
    ],
    "Cómo es (adjetivos)": [
        ("おおきい / ちいさい", "大きい / 小さい", "grande / pequeño", "ちいさい いぬが いちばん うるさい。", "El perro pequeño es el que más ladra.", ""),
        ("たかい / やすい", "高い / 安い", "caro / barato", "やすい！ …あ、ゼロを みまちがえた。", "¡Qué barato! …Ah, he contado mal los ceros.", ""),
        ("あたらしい / ふるい", "新しい / 古い", "nuevo / viejo", "あたらしい スマホ。ふるい わたし。", "Móvil nuevo. Yo, viejo.", ""),
        ("いい / わるい", "いい / 悪い", "bueno / malo", "いい しらせと わるい しらせ。どっち から？", "Una buena noticia y una mala. ¿Cuál primero?", "ええ"),
        ("あつい / さむい", "暑い / 寒い", "calor / frío (tiempo)", "なつは あつい。ふゆは さむい。もんくは まいにち。", "En verano calor, en invierno frío. Las quejas, a diario.", ""),
        ("たのしい", "楽しい", "divertido", "テストは たのしい ですね！ …だれも わらいません。", "¡Los exámenes son divertidos! …Nadie se ríe.", ""),
        ("むずかしい / やさしい", "難しい / 易しい", "difícil / fácil", "かんじは やさしい。と かんじは いいます。", "Los kanji son fáciles. Eso dicen los kanji.", ""),
        ("いそがしい", "忙しい", "ocupado", "いそがしい？ ゲームで？", "¿Ocupado? ¿Con el videojuego?", ""),
        ("おもしろい", "面白い", "interesante / gracioso", "おもしろい じょうだんですね。（わらって いない）", "Qué chiste tan gracioso. (No se ríe.)", "おもろい"),
        ("つまらない", "つまらない", "aburrido", "この えいがは つまらない。でも さいごまで みます。", "Esta peli es aburrida. Pero la veo hasta el final.", "しょうもない"),
        ("ながい / みじかい", "長い / 短い", "largo / corto", "こうちょうの はなしは ながい。", "El discurso del director es largo.", ""),
        ("はやい / おそい", "速い / 遅い", "rápido / lento (tarde)", "インターネットが おそい。わたしの へんじも。", "Internet va lento. Mis respuestas también.", ""),
        ("すき / きらい", "好き / 嫌い", "gustar / odiar", "げつようびが きらいです。げつようびも わたしが きらい。", "Odio los lunes. Y los lunes me odian.", ""),
        ("じょうず / へた", "上手 / 下手", "hábil / torpe", "にほんご、じょうずですね！（はい、と しか いってない）", "¡Qué bien hablas japonés! (Solo ha dicho «hai».)", ""),
        ("げんき", "元気", "con energía / sano", "げんきです！ コーヒーの おかげで。", "¡Estoy bien! Gracias al café.", ""),
        ("しずか / にぎやか", "静か / 賑やか", "tranquilo / animado", "おおさかに しずかな ばしょは ありません。", "En Osaka no hay sitios tranquilos.", ""),
        ("きれい", "きれい", "bonito / limpio", "へやが きれい！ …ぜんぶ クローゼットの なかです。", "¡Qué habitación tan limpia! …Todo está en el armario.", ""),
        ("ゆうめい", "有名", "famoso", "わたしは ゆうめいです。うちの ねこに。", "Soy famoso. Para mi gato.", ""),
    ],
    "Preguntas y palabras clave": [
        ("なに / なん", "何", "qué", "なに これ？ たべもの？ かざり？", "¿Qué es esto? ¿Comida? ¿Decoración?", "なんや"),
        ("だれ", "誰", "quién", "だれが れいぞうこの プリンを たべましたか。", "¿Quién se comió el flan de la nevera?", ""),
        ("いつ", "いつ", "cuándo", "いつ やりますか。…いつか。", "¿Cuándo lo haces? …Algún día.", ""),
        ("いくら", "いくら", "cuánto (precio)", "いくらですか。…やっぱり いいです。", "¿Cuánto cuesta? …Mejor no.", "なんぼ"),
        ("どうして", "どうして", "por qué", "どうして？ どうして げつようびは くるの？", "¿Por qué? ¿Por qué existen los lunes?", "なんで"),
        ("どう", "どう", "cómo / qué tal", "わたしの かみ、どう？ …しょうじきに いわないで。", "¿Qué tal mi pelo? …No seas sincero.", ""),
        ("これ / それ / あれ", "これ / それ / あれ", "esto / eso / aquello", "これ ください。それじゃ なくて、これ！", "Esto, por favor. ¡Eso no, esto!", ""),
        ("とても", "とても", "muy", "とても かんたんです。（さんじかん かかった）", "Es muy fácil. (Le llevó tres horas.)", "めっちゃ"),
        ("すこし / ちょっと", "少し / ちょっと", "un poco", "ちょっと…（＝ぜったい いや）", "Es que… un poco… (= ni de broma)", ""),
        ("たくさん", "たくさん", "mucho", "しゅくだいが たくさん。やるきは ゼロ。", "Muchos deberes. Ganas, cero.", "ぎょうさん"),
        ("ぜんぜん", "全然", "nada (con negación)", "ぜんぜん だいじょうぶ じゃ ありません。", "No estoy nada bien.", ""),
        ("まだ / もう", "まだ / もう", "todavía / ya", "まだ？ …もう いい。", "¿Todavía no? …Ya da igual.", ""),
        ("でも", "でも", "pero", "ダイエット ちゅうです。でも ケーキは べつ。", "Estoy a dieta. Pero el pastel es otra cosa.", ""),
        ("だから", "だから", "por eso", "だから いったでしょう！", "¡Por eso te lo dije!", "せやから"),
        ("いっしょに", "一緒に", "juntos", "いっしょに べんきょうしよう。…やっぱり ひるねしよう。", "Estudiemos juntos. …Mejor echemos la siesta.", ""),
    ],
}

# Kansai-ben y «matón de película»: NO entra en el examen, sirve para sorprender (y entender las pelis)
KANSAI = [
    ("なんでやねん", "なんでやねん", "¡¿pero qué dices?! / ¡¿por qué?!", "La réplica (tsukkomi) de Osaka. Úsala cuando alguien diga una tontería y la sala entera se reirá.", "kansai"),
    ("めっちゃ", "めっちゃ", "muy (= とても)", "めっちゃ おいしい = riquísimo. Ya lo dice toda Japón, pero nació en Kansai.", "kansai"),
    ("ほんま", "ほんま", "de verdad (= ほんとう)", "ほんまに？ = ¿en serio? Dilo con cara de sospecha.", "kansai"),
    ("あかん", "あかん", "no vale / mal (= だめ)", "それは あかん = eso no. Para todo lo que sale mal.", "kansai"),
    ("おおきに", "おおきに", "gracias (= ありがとう)", "El gracias de los comerciantes de Kioto y Osaka. Los mayores sonríen al oírlo.", "kansai"),
    ("ちゃう", "ちゃう", "no es eso (= ちがう)", "ちゃうちゃう = que no, que no. (Y ちゃうちゃう también es el perro chow chow.)", "kansai"),
    ("ええやん", "ええやん", "¡qué bien! / ¡mola! (= いいじゃない)", "Para aprobar lo que sea: ええやん、それ！", "kansai"),
    ("せやな", "せやな", "ya, es verdad (= そうだね)", "La respuesta comodín cuando no has escuchado nada.", "kansai"),
    ("なんぼ", "なんぼ", "¿cuánto? (= いくら)", "これ なんぼ？ En un mercado de Osaka luego se regatea.", "kansai"),
    ("しんどい", "しんどい", "estoy molido (= つかれた)", "あー、しんどい。 = Ay, qué cansancio.", "kansai"),
    ("ほな", "ほな", "pues / venga, me voy (= じゃあ)", "ほな、また = venga, hasta luego.", "kansai"),
    ("〜へん", "いかへん / わからへん", "no … (= 〜ない)", "いかへん = no voy. わからへん = no lo sé. Cambia ない por へん.", "kansai"),
    ("しらんけど", "知らんけど", "…aunque yo qué sé", "Se añade al final de un consejo muy seguro: «Ese restaurante es el mejor de Japón. しらんけど». Sarcasmo puro de Osaka.", "kansai"),
    ("あほ", "あほ", "tonto (cariñoso en Kansai)", "En Osaka あほ es casi cariñoso; ばか ofende. En Tokio, al revés.", "kansai"),
    ("もうかりまっか / ぼちぼちでんな", "儲かりまっか / ぼちぼちでんな", "¿qué tal el negocio? / tirando", "El saludo clásico de los comerciantes de Osaka. Si lo dices bien, te invitan a té.", "kansai"),
    ("じぶん", "自分", "tú (en Kansai)", "じぶん、どこから きたん？ = ¿tú de dónde eres? Ojo: en Tokio じぶん es «yo».", "kansai"),
    ("かまへん", "かまへん", "no pasa nada (= かまわない)", "かまへん、かまへん = tranquilo, no importa.", "kansai"),
    ("しゃあない", "しゃあない", "qué le vamos a hacer (= しかたない)", "Lluvia en tu día libre: しゃあない。", "kansai"),
    ("なにみとんねん", "何見とんねん", "¿y tú qué miras?", "De película de matones de Osaka. Solo para hacer reír a tus amigos: con desconocidos, NUNCA.", "calle"),
    ("なめとんのか", "なめとんのか", "¿me estás vacilando?", "Frase de yakuza de peli. Si la dices sonriendo con una galleta en la mano, éxito asegurado.", "calle"),
    ("もんく あんのか", "文句あんのか", "¿tienes algún problema?", "El matón de la esquina. En la vida real: いいえ、ありません。", "calle"),
    ("ええかげんに せえ", "ええ加減にせえ", "¡ya está bien!", "Lo dice la madre de Osaka cuando ya no puede más. Más miedo que cualquier yakuza.", "calle"),
    ("じょうとうや", "上等や", "¡venga, a ver si te atreves!", "Desafío de manga de pandilleros (ヤンキー). Para el karaoke dramático, no para la calle.", "calle"),
    ("おぼえとけよ", "覚えとけよ", "¡esto no queda así!", "Lo grita el malo al huir en todas las series. Perfecto cuando pierdes al ajedrez.", "calle"),
    ("おい、こら", "おい、こら", "¡eh, tú!", "El policía antiguo de las pelis. Hoy suena a broma… o a problemas.", "calle"),
]

ROMA = {
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo", "しゃ": "sha", "しゅ": "shu", "しょ": "sho", "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo", "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo", "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo", "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo", "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo", "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
}
BASE = dict(zip("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ",
                ["a", "i", "u", "e", "o", "ka", "ki", "ku", "ke", "ko", "sa", "shi", "su", "se", "so", "ta", "chi", "tsu", "te", "to",
                 "na", "ni", "nu", "ne", "no", "ha", "hi", "fu", "he", "ho", "ma", "mi", "mu", "me", "mo", "ya", "yu", "yo",
                 "ra", "ri", "ru", "re", "ro", "wa", "o", "n", "ga", "gi", "gu", "ge", "go", "za", "ji", "zu", "ze", "zo",
                 "da", "ji", "zu", "de", "do", "ba", "bi", "bu", "be", "bo", "pa", "pi", "pu", "pe", "po"]))


def a_kana(texto):
    """Katakana → hiragana, para romanizar las palabras extranjeras con la misma tabla."""
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in texto)


def romaji(texto):
    t, out, i = a_kana(texto), [], 0
    while i < len(t):
        if t[i:i + 2] in ROMA:
            out.append(ROMA[t[i:i + 2]]); i += 2; continue
        c = t[i]
        if c == "っ" and i + 1 < len(t):
            nxt = ROMA.get(t[i + 1:i + 3]) or BASE.get(t[i + 1], "")
            out.append(nxt[:1] if nxt else ""); i += 1; continue
        if c == "ー" and out:
            out.append(out[-1][-1]); i += 1; continue
        out.append(BASE.get(c, c)); i += 1
    return "".join(out)


def validar():
    vistos = set()
    for tema, lista in VOCAB.items():
        for e in lista:
            assert len(e) == 6 and all(e[:5]), (tema, e)
            assert e[0] not in vistos, f"repetida: {e[0]}"
            vistos.add(e[0])
            assert not re.search(r"[a-zA-Z]", e[3]), f"romaji en la frase: {e}"
    for e in KANSAI:
        assert len(e) == 5 and e[4] in ("kansai", "calle"), e


def main():
    validar()
    ruta = os.path.join(RAIZ, "www", "kana.json")
    datos = json.load(open(ruta, encoding="utf-8"))
    datos["vocab"] = [{"c": w, "k": kj if kj != w else "", "r": " / ".join(romaji(x) for x in w.split(" / ")), "m": m, "f": f, "fe": fe, "ks": ks, "g": tema}
                      for tema, lista in VOCAB.items() for (w, kj, m, f, fe, ks) in lista]
    datos["kansai"] = [{"c": w, "k": kj if kj != w else "", "r": " / ".join(romaji(x) for x in w.split(" / ")), "m": m, "t": t, "g": g}
                       for (w, kj, m, t, g) in KANSAI]
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
    print(f"vocab: {len(datos['vocab'])} palabras en {len(VOCAB)} temas · kansai: {len(KANSAI)}")


if __name__ == "__main__":
    main()
