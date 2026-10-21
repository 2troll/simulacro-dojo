// API del Dojo: cuentas, progreso en la nube, amigos, regalos y chat.
// Todo en Cloudflare D1 (SQLite, plan gratis). La web estática la sirve ASSETS; aquí solo llega /api/*.

const DIA = 864e5, SESION_DIAS = 90;
const NOMBRE = /^[a-z0-9_.]{3,20}$/;
const CLAVE = /^[A-Za-z0-9_-]{43}$/;            // 32 bytes en base64url: la clave ya viene derivada (PBKDF2) del navegador
const AVATARES = ["🙂", "😎", "🦊", "🐼", "🐯", "🐸", "🐙", "🦉", "🐢", "🌸", "🗻", "⛩️", "🍙", "🍵", "📚", "⚡", "🌙", "⭐"];
const REGALOS = { congela: "Protector de racha", animo: "Ánimo" };
const MAX_ESTADO = 400_000, MAX_AMIGOS = 150;

const J = (d, s = 200, h = {}) => new Response(JSON.stringify(d), {
  status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...h },
});
const mal = (m, s = 400) => J({ error: m }, s);
const ahora = () => Date.now();
const diaUTC = () => new Date().toISOString().slice(0, 10);
const semanaAct = () => Math.floor((ahora() / DIA + 3) / 7);   // el día 0 de 1970 fue jueves: +3 hace que la semana empiece en lunes
const b64u = buf => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const sha = async t => b64u(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)));
const limpio = (t, max) => String(t ?? "").replace(/[\u0000-\u0008\u000B-\u001F\u007F‪-‮⁦-⁩]/g, "").trim().slice(0, max);

// Comparación en tiempo constante para no filtrar el hash por tiempos de respuesta
function igual(a, b) {
  if (a.length !== b.length) return false;
  let x = 0; for (let i = 0; i < a.length; i++) x |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return x === 0;
}

export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    if (!u.pathname.startsWith("/api/")) return env.ASSETS.fetch(req);
    try { return await api(req, env, u); }
    catch (e) { console.error(e); return mal("Error del servidor. Prueba otra vez en un momento.", 500); }
  },
};

// Freno contra abusos: máximo «max» intentos por clave en «ms»
async function freno(env, k, max, ms) {
  const t = ahora();
  const r = await env.DB.prepare("SELECT n, hasta FROM intentos WHERE k=?").bind(k).first();
  if (!r || r.hasta < t) { await env.DB.prepare("INSERT OR REPLACE INTO intentos(k,n,hasta) VALUES(?,1,?)").bind(k, t + ms).run(); return false; }
  if (r.n >= max) return true;
  await env.DB.prepare("UPDATE intentos SET n=n+1 WHERE k=?").bind(k).run();
  return false;
}

async function quien(req, env) {
  const m = (req.headers.get("cookie") || "").match(/(?:^|;\s*)dojo_s=([A-Za-z0-9_-]{20,})/);
  if (!m) return null;
  const h = await sha(m[1]);
  const r = await env.DB.prepare("SELECT u.*, s.hash AS _s FROM sesiones s JOIN usuarios u ON u.id=s.usuario WHERE s.hash=? AND s.expira>?").bind(h, ahora()).first();
  if (r && (!r.visto || ahora() - r.visto > 5 * 60e3)) await env.DB.prepare("UPDATE usuarios SET visto=? WHERE id=?").bind(ahora(), r.id).run();
  return r;
}

async function abrirSesion(env, id) {
  const tok = b64u(crypto.getRandomValues(new Uint8Array(32)));
  await env.DB.prepare("INSERT INTO sesiones(hash,usuario,creado,expira) VALUES(?,?,?,?)").bind(await sha(tok), id, ahora(), ahora() + SESION_DIAS * DIA).run();
  return `dojo_s=${tok}; Path=/api; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESION_DIAS * 86400}`;
}
const cerrarCookie = "dojo_s=; Path=/api; HttpOnly; Secure; SameSite=Lax; Max-Age=0";

// Lo que ven los demás de ti
const publico = u => ({
  usuario: u.nombre, nombre: u.mostrar || u.nombre, avatar: u.avatar || "🙂",
  racha: u.racha, ultimo: u.ultimo, xp: u.xp,
  semana: u.semana === semanaAct() ? Math.max(0, u.xp - u.xp_semana0) : 0,
  hoy: u.hoy_d && u.hoy_d >= new Date(ahora() - DIA).toISOString().slice(0, 10) ? { d: u.hoy_d, n: u.hoy } : null,
  visto: u.visto,
});

async function porNombre(env, nombre) {
  const n = limpio(nombre, 21).replace(/^@/, "").toLowerCase();
  return NOMBRE.test(n) ? env.DB.prepare("SELECT * FROM usuarios WHERE nombre=?").bind(n).first() : null;
}
const par = (x, y) => (x < y ? [x, y] : [y, x]);
async function amistad(env, x, y) {
  const [a, b] = par(x, y);
  return env.DB.prepare("SELECT * FROM amistades WHERE a=? AND b=?").bind(a, b).first();
}
async function sonAmigos(env, x, y) { return (await amistad(env, x, y))?.estado === "amigos"; }

async function cuerpo(req, max = 20_000) {
  const t = await req.text();
  if (t.length > max) throw Object.assign(new Error("grande"), { status: 413 });
  try { return t ? JSON.parse(t) : {}; } catch { return {}; }
}

async function api(req, env, u) {
  const ruta = u.pathname.slice(5).replace(/\/+$/, ""), M = req.method;
  // Contra CSRF: toda escritura debe venir de esta misma web con la cabecera propia
  if (M !== "GET") {
    const o = req.headers.get("origin");
    if (req.headers.get("x-dojo") !== "1" || (o && o !== u.origin)) return mal("Petición no permitida", 403);
  }
  const ip = req.headers.get("cf-connecting-ip") || "?";
  let b;
  try { b = M === "GET" ? {} : await cuerpo(req, ruta === "progreso" ? MAX_ESTADO + 1000 : 20_000); }
  catch (e) { return mal("Demasiado grande", e.status || 400); }

  // ---------- Cuentas ----------
  if (ruta === "registro" && M === "POST") {
    if (await freno(env, "reg:" + ip, 6, 3600e3)) return mal("Demasiadas cuentas desde aquí. Prueba dentro de una hora.", 429);
    const nombre = limpio(b.usuario, 20).toLowerCase();
    if (!NOMBRE.test(nombre)) return mal("El usuario lleva de 3 a 20 letras sin tildes, números, punto o guion bajo.");
    if (!CLAVE.test(b.clave || "")) return mal("Contraseña no válida");
    if (await env.DB.prepare("SELECT 1 FROM usuarios WHERE nombre=?").bind(nombre).first()) return mal("Ese usuario ya existe. Elige otro.", 409);
    const sal = b64u(crypto.getRandomValues(new Uint8Array(16)));
    const avatar = AVATARES.includes(b.avatar) ? b.avatar : AVATARES[Math.floor(Math.random() * AVATARES.length)];
    const r = await env.DB.prepare("INSERT INTO usuarios(nombre,mostrar,avatar,sal,hash,creado,visto,semana) VALUES(?,?,?,?,?,?,?,?) RETURNING id")
      .bind(nombre, limpio(b.nombre, 30) || null, avatar, sal, await sha(sal + ":" + b.clave), ahora(), ahora(), semanaAct()).first();
    return J({ ok: true }, 201, { "set-cookie": await abrirSesion(env, r.id) });
  }
  if (ruta === "entrar" && M === "POST") {
    const nombre = limpio(b.usuario, 21).replace(/^@/, "").toLowerCase();
    if (await freno(env, "in:" + ip, 20, 900e3) || await freno(env, "inu:" + nombre, 10, 900e3)) return mal("Demasiados intentos. Espera 15 minutos.", 429);
    const x = NOMBRE.test(nombre) && CLAVE.test(b.clave || "") ? await env.DB.prepare("SELECT * FROM usuarios WHERE nombre=?").bind(nombre).first() : null;
    if (!x || !igual(await sha(x.sal + ":" + b.clave), x.hash)) return mal("Usuario o contraseña incorrectos", 401);
    await env.DB.prepare("DELETE FROM sesiones WHERE expira<?").bind(ahora()).run();
    await env.DB.prepare("DELETE FROM intentos WHERE hasta<?").bind(ahora()).run();
    return J({ ok: true }, 200, { "set-cookie": await abrirSesion(env, x.id) });
  }

  const yo = await quien(req, env);
  if (ruta === "salir" && M === "POST") {
    if (yo) await env.DB.prepare("DELETE FROM sesiones WHERE hash=?").bind(yo._s).run();
    return J({ ok: true }, 200, { "set-cookie": cerrarCookie });
  }
  if (!yo) return mal("Entra en tu cuenta", 401);

  if (ruta === "yo" && M === "GET") {
    const p = await env.DB.prepare("SELECT estado, at FROM progreso WHERE usuario=?").bind(yo.id).first();
    return J({ yo: publico(yo), avatares: AVATARES, progreso: p || null });
  }
  if (ruta === "yo" && M === "PATCH") {
    const nombre = b.nombre !== undefined ? limpio(b.nombre, 30) || null : yo.mostrar;
    const avatar = AVATARES.includes(b.avatar) ? b.avatar : yo.avatar;
    await env.DB.prepare("UPDATE usuarios SET mostrar=?, avatar=? WHERE id=?").bind(nombre, avatar, yo.id).run();
    return J({ yo: publico({ ...yo, mostrar: nombre, avatar }) });
  }
  if (ruta === "cuenta/clave" && M === "POST") {
    if (await freno(env, "cl:" + yo.id, 5, 900e3)) return mal("Demasiados intentos. Espera 15 minutos.", 429);
    if (!CLAVE.test(b.clave || "") || !CLAVE.test(b.nueva || "")) return mal("Contraseña no válida");
    if (!igual(await sha(yo.sal + ":" + b.clave), yo.hash)) return mal("La contraseña actual no es esa", 401);
    const sal = b64u(crypto.getRandomValues(new Uint8Array(16)));
    await env.DB.batch([
      env.DB.prepare("UPDATE usuarios SET sal=?, hash=? WHERE id=?").bind(sal, await sha(sal + ":" + b.nueva), yo.id),
      env.DB.prepare("DELETE FROM sesiones WHERE usuario=? AND hash<>?").bind(yo.id, yo._s),   // cierra los demás dispositivos
    ]);
    return J({ ok: true });
  }
  if (ruta === "cuenta/exportar" && M === "GET") {
    const q = (s, ...v) => env.DB.prepare(s).bind(...v).all().then(r => r.results);
    const { sal, hash, _s, ...datos } = yo;
    return J({
      cuenta: datos,
      progreso: await env.DB.prepare("SELECT * FROM progreso WHERE usuario=?").bind(yo.id).first(),
      amistades: await q("SELECT * FROM amistades WHERE a=? OR b=?", yo.id, yo.id),
      regalos: await q("SELECT * FROM regalos WHERE de=? OR para=?", yo.id, yo.id),
      mensajes: await q("SELECT * FROM mensajes WHERE de=? OR para=?", yo.id, yo.id),
    }, 200, { "content-disposition": `attachment; filename="dojo-${yo.nombre}.json"` });
  }
  if (ruta === "cuenta/borrar" && M === "POST") {
    if (!CLAVE.test(b.clave || "") || !igual(await sha(yo.sal + ":" + b.clave), yo.hash)) return mal("La contraseña no es esa", 401);
    const i = yo.id;
    await env.DB.batch([
      env.DB.prepare("DELETE FROM mensajes WHERE de=? OR para=?").bind(i, i),
      env.DB.prepare("DELETE FROM regalos WHERE de=? OR para=?").bind(i, i),
      env.DB.prepare("DELETE FROM amistades WHERE a=? OR b=?").bind(i, i),
      env.DB.prepare("DELETE FROM sesiones WHERE usuario=?").bind(i),
      env.DB.prepare("DELETE FROM progreso WHERE usuario=?").bind(i),
      env.DB.prepare("DELETE FROM usuarios WHERE id=?").bind(i),
    ]);
    return J({ ok: true }, 200, { "set-cookie": cerrarCookie });
  }

  // ---------- Progreso ----------
  if (ruta === "progreso" && M === "PUT") {
    if (typeof b.estado !== "string" || b.estado.length > MAX_ESTADO) return mal("Progreso no válido");
    let e; try { e = JSON.parse(b.estado); } catch { return mal("Progreso no válido"); }
    const xp = Math.max(0, Math.min(1e7, Math.floor(+e.xp || 0)));
    const prev = await env.DB.prepare("SELECT estado, at FROM progreso WHERE usuario=?").bind(yo.id).first();
    // Si otro dispositivo ya subió más progreso, no lo pisamos: se lo devolvemos para que lo adopte
    if (prev && !b.forzar && xp < yo.xp) return J({ conflicto: true, progreso: prev }, 409);
    const sem = semanaAct();
    // primera subida: lo que ya traía del navegador no cuenta para la liga de esta semana
    const base = !prev ? xp : yo.semana !== sem ? yo.xp : yo.xp_semana0;
    const d = e.daily && typeof e.daily.d === "string" ? e.daily : null;
    const at = ahora();
    await env.DB.batch([
      env.DB.prepare("INSERT INTO progreso(usuario,estado,at) VALUES(?,?,?) ON CONFLICT(usuario) DO UPDATE SET estado=excluded.estado, at=excluded.at").bind(yo.id, b.estado, at),
      env.DB.prepare("UPDATE usuarios SET xp=?, racha=?, ultimo=?, hoy=?, hoy_d=?, semana=?, xp_semana0=? WHERE id=?").bind(
        xp, Math.max(0, Math.min(1e5, Math.floor(+e.streak || 0))), limpio(e.last, 10) || null,
        d ? Math.max(0, Math.min(1e5, Math.floor(+d.n || 0))) : 0, d ? limpio(d.d, 10) : null, sem, Math.min(base, xp), yo.id),
    ]);
    return J({ ok: true, at });
  }

  // ---------- Amigos ----------
  if (ruta === "amigos" && M === "GET") {
    const r = await env.DB.prepare(`SELECT f.estado, f.pide, u.* ,
        (SELECT COUNT(*) FROM mensajes m WHERE m.de=u.id AND m.para=?1 AND m.leido=0) AS sin_leer
      FROM amistades f JOIN usuarios u ON u.id = CASE WHEN f.a=?1 THEN f.b ELSE f.a END
      WHERE f.a=?1 OR f.b=?1`).bind(yo.id).all();
    const out = { amigos: [], recibidas: [], enviadas: [] };
    for (const x of r.results) {
      const p = { ...publico(x), sin_leer: x.sin_leer };
      if (x.estado === "amigos") out.amigos.push(p); else (x.pide === yo.id ? out.enviadas : out.recibidas).push(p);
    }
    out.amigos.sort((a, b) => b.semana - a.semana || b.xp - a.xp);
    out.yo = publico(yo);
    return J(out);
  }
  if (ruta === "amigos" && M === "POST") {
    if (await freno(env, "am:" + yo.id, 30, 3600e3)) return mal("Demasiadas solicitudes. Prueba dentro de una hora.", 429);
    const otro = await porNombre(env, b.usuario);
    if (!otro) return mal("No hay nadie con ese usuario", 404);
    if (otro.id === yo.id) return mal("Ese eres tú 🙂");
    const f = await amistad(env, yo.id, otro.id);
    if (f?.estado === "amigos") return J({ estado: "amigos" });
    const [a, c] = par(yo.id, otro.id);
    if (f && f.pide !== yo.id) {           // te la había pedido él: queda aceptada
      await env.DB.prepare("UPDATE amistades SET estado='amigos' WHERE a=? AND b=?").bind(a, c).run();
      return J({ estado: "amigos" });
    }
    if (f) return J({ estado: "enviada" });
    const n = await env.DB.prepare("SELECT COUNT(*) AS n FROM amistades WHERE a=?1 OR b=?1").bind(yo.id).first();
    if (n.n >= MAX_AMIGOS) return mal("Has llegado al máximo de amigos");
    await env.DB.prepare("INSERT INTO amistades(a,b,pide,estado,creado) VALUES(?,?,?,'pendiente',?)").bind(a, c, yo.id, ahora()).run();
    return J({ estado: "enviada" }, 201);
  }
  let m;
  if ((m = ruta.match(/^amigos\/([a-z0-9_.]{3,20})$/i)) && M === "DELETE") {
    const otro = await porNombre(env, m[1]);
    if (otro) { const [a, c] = par(yo.id, otro.id); await env.DB.prepare("DELETE FROM amistades WHERE a=? AND b=?").bind(a, c).run(); }
    return J({ ok: true });
  }

  // ---------- Regalos ----------
  if (ruta === "regalos" && M === "POST") {
    const otro = await porNombre(env, b.usuario);
    if (!otro || !(await sonAmigos(env, yo.id, otro.id))) return mal("Solo puedes regalar a tus amigos", 403);
    if (!REGALOS[b.tipo]) return mal("Regalo no válido");
    const r = await env.DB.prepare("INSERT OR IGNORE INTO regalos(de,para,tipo,nota,dia,creado) VALUES(?,?,?,?,?,?)")
      .bind(yo.id, otro.id, b.tipo, limpio(b.nota, 120) || null, diaUTC(), ahora()).run();
    if (!r.meta.changes) return mal(`Hoy ya le has mandado un «${REGALOS[b.tipo]}». Mañana puedes otro.`, 409);
    return J({ ok: true }, 201);
  }
  if (ruta === "regalos/recoger" && M === "POST") {
    const r = await env.DB.prepare(`UPDATE regalos SET recogido=? WHERE para=? AND recogido IS NULL
      RETURNING id, tipo, nota, (SELECT nombre FROM usuarios WHERE id=de) AS de_usuario, (SELECT COALESCE(mostrar,nombre) FROM usuarios WHERE id=de) AS de_nombre`)
      .bind(ahora(), yo.id).all();
    return J({ regalos: r.results });
  }

  // ---------- Avisos (lo que se consulta de fondo cada minuto) ----------
  if (ruta === "avisos" && M === "GET") {
    const r = await env.DB.prepare(`SELECT
        (SELECT COUNT(*) FROM mensajes WHERE para=?1 AND leido=0) AS mensajes,
        (SELECT COUNT(*) FROM regalos WHERE para=?1 AND recogido IS NULL) AS regalos,
        (SELECT COUNT(*) FROM amistades WHERE (a=?1 OR b=?1) AND estado='pendiente' AND pide<>?1) AS solicitudes`).bind(yo.id).first();
    return J(r);
  }

  // ---------- Chat entre amigos ----------
  if ((m = ruta.match(/^chat\/([a-z0-9_.]{3,20})$/i))) {
    const otro = await porNombre(env, m[1]);
    if (!otro || !(await sonAmigos(env, yo.id, otro.id))) return mal("Solo puedes hablar con tus amigos", 403);
    if (M === "GET") {
      const desde = Math.max(0, Math.floor(+u.searchParams.get("desde") || 0));
      const r = await env.DB.prepare(`SELECT id, de, texto, creado FROM (
          SELECT * FROM mensajes WHERE ((de=?1 AND para=?2) OR (de=?2 AND para=?1)) AND id>?3 ORDER BY id DESC LIMIT 100
        ) ORDER BY id`).bind(yo.id, otro.id, desde).all();
      await env.DB.prepare("UPDATE mensajes SET leido=1 WHERE de=? AND para=? AND leido=0").bind(otro.id, yo.id).run();
      return J({ mensajes: r.results.map(x => ({ id: x.id, mio: x.de === yo.id, texto: x.texto, creado: x.creado })), amigo: publico(otro) });
    }
    if (M === "POST") {
      if (await freno(env, "msg:" + yo.id, 30, 60e3)) return mal("Vas muy rápido. Espera un momento.", 429);
      const texto = limpio(b.texto, 500);
      if (!texto) return mal("Mensaje vacío");
      const r = await env.DB.prepare("INSERT INTO mensajes(de,para,texto,creado) VALUES(?,?,?,?) RETURNING id, creado").bind(yo.id, otro.id, texto, ahora()).first();
      return J({ id: r.id, mio: true, texto, creado: r.creado }, 201);
    }
  }

  return mal("No existe", 404);
}
