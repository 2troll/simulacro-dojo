-- Código de recuperación (sin correo), reto del día entre amigos y avisos al móvil (Web Push)
ALTER TABLE usuarios ADD COLUMN rec_sal TEXT;
ALTER TABLE usuarios ADD COLUMN rec_hash TEXT;
CREATE TABLE retos(usuario INTEGER NOT NULL, dia TEXT NOT NULL, examen TEXT NOT NULL, aciertos INTEGER NOT NULL, total INTEGER NOT NULL, ms INTEGER NOT NULL, creado INTEGER NOT NULL, PRIMARY KEY(usuario, dia, examen));
CREATE INDEX retos_dia ON retos(dia, examen);
CREATE TABLE avisos_push(endpoint TEXT PRIMARY KEY, usuario INTEGER NOT NULL, p256dh TEXT NOT NULL, auth TEXT NOT NULL,
  tz INTEGER NOT NULL DEFAULT 0,      -- getTimezoneOffset() del móvil, en minutos
  hora INTEGER NOT NULL DEFAULT 20,   -- hora local del recordatorio
  ultimo TEXT,                        -- último día (local) en que se mandó el recordatorio
  creado INTEGER NOT NULL);
CREATE INDEX avisos_push_usuario ON avisos_push(usuario);
