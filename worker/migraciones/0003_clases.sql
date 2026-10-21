-- Clases: un profe crea la clase, los alumnos entran con un código y comparten tablón, liga y deberes
ALTER TABLE usuarios ADD COLUMN resumen TEXT;   -- resumen de exámenes y kana, calculado al subir el progreso (lo ve el profe)
CREATE TABLE clases(id INTEGER PRIMARY KEY, codigo TEXT NOT NULL UNIQUE, nombre TEXT NOT NULL, profe INTEGER NOT NULL, creado INTEGER NOT NULL);
CREATE TABLE clase_miembros(clase INTEGER NOT NULL, usuario INTEGER NOT NULL, rol TEXT NOT NULL, unido INTEGER NOT NULL, PRIMARY KEY(clase, usuario));
CREATE INDEX clase_miembros_usuario ON clase_miembros(usuario);
CREATE TABLE clase_mensajes(id INTEGER PRIMARY KEY, clase INTEGER NOT NULL, de INTEGER NOT NULL, texto TEXT NOT NULL, tipo TEXT, creado INTEGER NOT NULL);
CREATE INDEX clase_mensajes_clase ON clase_mensajes(clase, id);
