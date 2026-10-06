# Esquema de los bancos de preguntas

Salida: UN array JSON válido (sin comentarios, sin texto fuera del JSON, sin ```), de "sets".

Set:
{
  "sec": "reading" | "listening" | "vocab" | "grammar" | "writing" | "speaking",
  "task": "<nombre oficial de la tarea del examen real, p. ej. 'Read in Daily Life'>",
  "lvl": 1 | 2 | 3,              // 1 = fácil, 2 = medio, 3 = difícil (reparte ~30/45/25 %)
  "passage": "<texto a leer>",   // opcional (lectura, consigna de writing/speaking)
  "audio": "<guion que se leerá con voz sintética>", // opcional (listening). Diálogos: una línea por turno, "M: ..." (hombre) / "W: ..." (mujer). Nada de efectos de sonido.
  "qs": [Q, ...],                 // [] en writing/speaking
  "model": "<respuesta modelo de nivel alto>", // solo writing/speaking
  "tips": ["<consejo corto en español>", ...]    // solo writing/speaking, 2-4
}

Q (una de tres formas):
- Opción múltiple: {"t":"mcq","q":"<pregunta>","o":["A","B","C","D"],"a":<índice 0-3 de la correcta>,"e":"<explicación en español, 1-2 frases, que enseñe el truco>"}
- Hueco:           {"t":"fill","q":"<frase con ___ en el hueco>","a":["<respuesta>","<variante aceptada>"],"e":"<explicación en español>"}
- Ordenar:         {"t":"order","q":"<contexto o instrucción>","w":["palabras","desordenadas"],"a":"<frase correcta completa con las palabras separadas por espacios exactamente como en w>","e":"<explicación en español>"}

Reglas obligatorias:
- La respuesta correcta debe ser inequívocamente correcta; los distractores, plausibles pero claramente incorrectos.
- Reparte la posición de la correcta (a) entre 0, 1, 2 y 3 de forma equilibrada.
- Contenido apto para todos y halal: nada de alcohol, cerdo, apuestas, préstamos con interés, citas románticas, discotecas. Temas buenos: ciencia, naturaleza, historia, viajes, estudios, trabajo, deporte, comida sana, tecnología, ciudades.
- Nunca uses hebreo.
- Las explicaciones ("e", "tips") van SIEMPRE en español, claras y con el truco para acertar rápido.
- Los textos del examen van en el idioma del examen (inglés o japonés).
