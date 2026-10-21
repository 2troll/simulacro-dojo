-- Cuentas, progreso, amigos, regalos y chat del Dojo (D1 = SQLite: se puede exportar entero con `wrangler d1 export`)
CREATE TABLE usuarios(
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL UNIQUE COLLATE NOCASE,   -- @usuario, para buscarte
  mostrar TEXT,                                 -- nombre visible
  avatar TEXT,
  sal TEXT NOT NULL,
  hash TEXT NOT NULL,                           -- sha256(sal:clave); la clave ya llega derivada del navegador (PBKDF2)
  creado INTEGER NOT NULL,
  visto INTEGER,
  xp INTEGER NOT NULL DEFAULT 0,
  racha INTEGER NOT NULL DEFAULT 0,
  ultimo TEXT,                                  -- último día con práctica (fecha local del alumno)
  hoy INTEGER NOT NULL DEFAULT 0,
  hoy_d TEXT,
  semana INTEGER NOT NULL DEFAULT 0,            -- semanas desde 1970 empezando en lunes
  xp_semana0 INTEGER NOT NULL DEFAULT 0         -- xp al empezar la semana: la liga es xp - xp_semana0
);
CREATE TABLE progreso(usuario INTEGER PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE, estado TEXT NOT NULL, at INTEGER NOT NULL);
CREATE TABLE sesiones(hash TEXT PRIMARY KEY, usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE, creado INTEGER NOT NULL, expira INTEGER NOT NULL);
CREATE INDEX sesiones_usuario ON sesiones(usuario);
-- una fila por pareja (a < b); «pide» es quien mandó la solicitud
CREATE TABLE amistades(a INTEGER NOT NULL, b INTEGER NOT NULL, pide INTEGER NOT NULL, estado TEXT NOT NULL, creado INTEGER NOT NULL, PRIMARY KEY(a,b));
CREATE INDEX amistades_b ON amistades(b);
CREATE TABLE regalos(id INTEGER PRIMARY KEY, de INTEGER NOT NULL, para INTEGER NOT NULL, tipo TEXT NOT NULL, nota TEXT, dia TEXT NOT NULL, creado INTEGER NOT NULL, recogido INTEGER);
CREATE INDEX regalos_para ON regalos(para, recogido);
CREATE UNIQUE INDEX regalos_uno_al_dia ON regalos(de, para, tipo, dia);
CREATE TABLE mensajes(id INTEGER PRIMARY KEY, de INTEGER NOT NULL, para INTEGER NOT NULL, texto TEXT NOT NULL, creado INTEGER NOT NULL, leido INTEGER NOT NULL DEFAULT 0);
CREATE INDEX mensajes_par ON mensajes(de, para, id);
CREATE INDEX mensajes_no_leidos ON mensajes(para, leido);
CREATE TABLE intentos(k TEXT PRIMARY KEY, n INTEGER NOT NULL, hasta INTEGER NOT NULL);
