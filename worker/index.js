// API del Dojo: cuentas, progreso en la nube, amigos, regalos y chat.
// Todo en Cloudflare D1 (SQLite, plan gratis). La web estática la sirve ASSETS; aquí solo llega /api/*.
import { avisa } from "./push.js";

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

const EXAMENES = ["aws", "toefl", "ielts", "n5"];
// El plan gratis permite ~50 llamadas externas por petición: los avisos en grupo se cortan en 40
const PUSH_HOSTS = /(^|\.)(fcm\.googleapis\.com|push\.services\.mozilla\.com|push\.apple\.com|notify\.windows\.com)$/;
const entero = (v, a, z) => Math.max(a, Math.min(z, Math.floor(+v || 0)));
const nombreDe = u => u.mostrar || u.nombre;

// Código de recuperación: 100 bits sin letras que se confundan (0/O, 1/I). Sustituye al correo para recuperar la cuenta.
const ALF = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const normCod = c => String(c || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
async function nuevoCodigo(env, id) {
  const c = [...crypto.getRandomValues(new Uint8Array(20))].map(x => ALF[x & 31]).join("").match(/.{5}/g).join("-");
  const sal = b64u(crypto.getRandomValues(new Uint8Array(16)));
  await env.DB.prepare("UPDATE usuarios SET rec_sal=?, rec_hash=? WHERE id=?").bind(sal, await sha(sal + ":" + normCod(c)), id).run();
  return c;
}

// Lo que el profe ve de cada alumno: simulacros hechos, mejor nota y aprobados por examen, y kana dominados
function resumenDe(e) {
  const out = { ex: {}, kana: 0 };
  for (const x of EXAMENES) {
    const v = Object.values((e.exams || {})[x] || {}).filter(r => r && typeof r === "object");
    if (v.length) out.ex[x] = { hechos: v.length, mejor: Math.round(100 * Math.max(...v.map(r => +r.best || 0))), aprobados: v.filter(r => r.pass).length };
  }
  for (const s of Object.values(e.kana || {})) if (Array.isArray(s) && s[1] >= 2 && s[0] / s[1] >= 0.75) out.kana++;
  return JSON.stringify(out);
}
const CODALF = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const codigoClase = () => [...crypto.getRandomValues(new Uint8Array(6))].map(x => CODALF[x & 31]).join("");
async function miembro(env, clase, usuario) {
  return env.DB.prepare("SELECT c.*, m.rol FROM clases c JOIN clase_miembros m ON m.clase=c.id WHERE c.id=? AND m.usuario=?").bind(clase, usuario).first();
}

// Comparación en tiempo constante para no filtrar el hash por tiempos de respuesta
function igual(a, b) {
  if (a.length !== b.length) return false;
  let x = 0; for (let i = 0; i < a.length; i++) x |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return x === 0;
}

export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    if (!u.pathname.startsWith("/api/")) return env.ASSETS.fetch(req);
    try { return await api(req, env, u, ctx); }
    catch (e) { console.error(e); return mal("Error del servidor. Prueba otra vez en un momento.", 500); }
  },
  // Cada hora: recordatorio a quien tenga racha y aún no haya estudiado hoy, a la hora que eligió
  async scheduled(_ev, env, ctx) { ctx.waitUntil(recordatorios(env)); },
};

async function recordatorios(env) {
  const subs = (await env.DB.prepare("SELECT p.endpoint, p.usuario, p.tz, p.hora, p.ultimo AS avisado, u.racha, u.ultimo AS estudio FROM avisos_push p JOIN usuarios u ON u.id=p.usuario").all()).results;
  const hechos = new Set();
  for (const s of subs) {
    const local = new Date(ahora() - s.tz * 60e3), dia = local.toISOString().slice(0, 10);
    if (local.getUTCHours() !== s.hora || s.avisado === dia || s.estudio === dia) continue;   // ni a otra hora, ni dos veces, ni si ya estudió
    await env.DB.prepare("UPDATE avisos_push SET ultimo=? WHERE endpoint=?").bind(dia, s.endpoint).run();
    if (hechos.has(s.usuario)) continue;   // avisa() ya manda a todos sus dispositivos
    hechos.add(s.usuario);
    const viva = s.racha > 0 && s.estudio && (Date.parse(dia) - Date.parse(s.estudio)) / DIA <= 1;
    await avisa(env, s.usuario, viva
      ? { title: `🔥 Tu racha de ${s.racha} días`, body: "Se rompe esta noche. Con 5 minutos la salvas.", url: "/", tag: "racha" }
      : { title: "Dojo · 10 minutos hoy", body: "Un reto del día o unas tarjetas y listo.", url: "/", tag: "racha" });
  }
}

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

async function api(req, env, u, ctx) {
  const luego = p => ctx?.waitUntil(p.catch(e => console.warn(e.message)));   // avisos al móvil sin hacer esperar a quien escribe
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
    return J({ ok: true, codigo: await nuevoCodigo(env, r.id) }, 201, { "set-cookie": await abrirSesion(env, r.id) });
  }
  if (ruta === "recuperar" && M === "POST") {
    const nombre = limpio(b.usuario, 21).replace(/^@/, "").toLowerCase();
    if (await freno(env, "rec:" + ip, 10, 3600e3) || await freno(env, "recu:" + nombre, 5, 3600e3)) return mal("Demasiados intentos. Prueba dentro de una hora.", 429);
    const x = NOMBRE.test(nombre) && CLAVE.test(b.clave || "") ? await env.DB.prepare("SELECT * FROM usuarios WHERE nombre=?").bind(nombre).first() : null;
    if (!x || !x.rec_hash || !igual(await sha(x.rec_sal + ":" + normCod(b.codigo)), x.rec_hash)) return mal("Usuario o código incorrectos", 401);
    const sal = b64u(crypto.getRandomValues(new Uint8Array(16)));
    await env.DB.batch([
      env.DB.prepare("UPDATE usuarios SET sal=?, hash=? WHERE id=?").bind(sal, await sha(sal + ":" + b.clave), x.id),
      env.DB.prepare("DELETE FROM sesiones WHERE usuario=?").bind(x.id),
    ]);
    return J({ ok: true, codigo: await nuevoCodigo(env, x.id) }, 200, { "set-cookie": await abrirSesion(env, x.id) });   // el código usado deja de valer
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
  if (ruta === "cuenta/codigo" && M === "POST") {
    if (await freno(env, "cl:" + yo.id, 5, 900e3)) return mal("Demasiados intentos. Espera 15 minutos.", 429);
    if (!CLAVE.test(b.clave || "") || !igual(await sha(yo.sal + ":" + b.clave), yo.hash)) return mal("La contraseña no es esa", 401);
    return J({ codigo: await nuevoCodigo(env, yo.id) });
  }
  if (ruta === "cuenta/exportar" && M === "GET") {
    const q = (s, ...v) => env.DB.prepare(s).bind(...v).all().then(r => r.results);
    const { sal, hash, _s, rec_sal, rec_hash, ...datos } = yo;
    return J({
      cuenta: datos,
      progreso: await env.DB.prepare("SELECT * FROM progreso WHERE usuario=?").bind(yo.id).first(),
      amistades: await q("SELECT * FROM amistades WHERE a=? OR b=?", yo.id, yo.id),
      regalos: await q("SELECT * FROM regalos WHERE de=? OR para=?", yo.id, yo.id),
      mensajes: await q("SELECT * FROM mensajes WHERE de=? OR para=?", yo.id, yo.id),
      retos: await q("SELECT * FROM retos WHERE usuario=?", yo.id),
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
      env.DB.prepare("DELETE FROM retos WHERE usuario=?").bind(i),
      env.DB.prepare("DELETE FROM clase_mensajes WHERE clase IN (SELECT id FROM clases WHERE profe=?)").bind(i),
      env.DB.prepare("DELETE FROM clase_miembros WHERE clase IN (SELECT id FROM clases WHERE profe=?) OR usuario=?").bind(i, i),
      env.DB.prepare("DELETE FROM clases WHERE profe=?").bind(i),
      env.DB.prepare("DELETE FROM clase_mensajes WHERE de=?").bind(i),
      env.DB.prepare("DELETE FROM avisos_push WHERE usuario=?").bind(i),
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
      env.DB.prepare("UPDATE usuarios SET resumen=? WHERE id=?").bind(resumenDe(e), yo.id),
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
      luego(avisa(env, otro.id, { title: "🤝 ¡Ya sois amigos!", body: `${nombreDe(yo)} ha aceptado. Ya podéis competir en la liga.`, url: "/?amigos=1", tag: "amigo" }));
      return J({ estado: "amigos" });
    }
    if (f) return J({ estado: "enviada" });
    const n = await env.DB.prepare("SELECT COUNT(*) AS n FROM amistades WHERE a=?1 OR b=?1").bind(yo.id).first();
    if (n.n >= MAX_AMIGOS) return mal("Has llegado al máximo de amigos");
    await env.DB.prepare("INSERT INTO amistades(a,b,pide,estado,creado) VALUES(?,?,?,'pendiente',?)").bind(a, c, yo.id, ahora()).run();
    luego(avisa(env, otro.id, { title: "👋 Solicitud de amistad", body: `${nombreDe(yo)} (@${yo.nombre}) quiere estudiar contigo`, url: "/?amigos=1", tag: "amigo" }));
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
    luego(avisa(env, otro.id, b.tipo === "congela"
      ? { title: "❄ Te han regalado un protector de racha", body: `${nombreDe(yo)} te cubre un día sin estudiar`, url: "/?amigos=1", tag: "regalo" }
      : { title: `👏 ${nombreDe(yo)}`, body: limpio(b.nota, 120) || "¡Ánimo con el estudio!", url: "/?amigos=1", tag: "regalo" }));
    return J({ ok: true }, 201);
  }
  if (ruta === "regalos/recoger" && M === "POST") {
    const r = await env.DB.prepare(`UPDATE regalos SET recogido=? WHERE para=? AND recogido IS NULL
      RETURNING id, tipo, nota, (SELECT nombre FROM usuarios WHERE id=de) AS de_usuario, (SELECT COALESCE(mostrar,nombre) FROM usuarios WHERE id=de) AS de_nombre`)
      .bind(ahora(), yo.id).all();
    return J({ regalos: r.results });
  }

  // ---------- Avisos al móvil (Web Push) ----------
  if (ruta === "push" && M === "POST") {
    const s = b.sub || {}, ep = String(s.endpoint || "");
    let host = ""; try { host = new URL(ep).hostname; } catch {}
    // solo servicios de push reales: así nadie usa el servidor para llamar a otras webs
    if (!ep.startsWith("https://") || ep.length > 1000 || !PUSH_HOSTS.test(host) || !s.keys?.p256dh || !s.keys?.auth) return mal("Este navegador no admite avisos");
    await env.DB.prepare(`INSERT INTO avisos_push(endpoint,usuario,p256dh,auth,tz,hora,creado) VALUES(?,?,?,?,?,?,?)
      ON CONFLICT(endpoint) DO UPDATE SET usuario=excluded.usuario, p256dh=excluded.p256dh, auth=excluded.auth, tz=excluded.tz, hora=excluded.hora`)
      .bind(ep, yo.id, limpio(s.keys.p256dh, 200), limpio(s.keys.auth, 100), entero(b.tz, -840, 840), entero(b.hora, 0, 23), ahora()).run();
    if (b.probar) luego(avisa(env, yo.id, { title: "✅ Avisos activados", body: "Así te llegarán los mensajes, los regalos y el recordatorio de tu racha.", url: "/", tag: "prueba" }));
    return J({ ok: true });
  }
  if (ruta === "push" && M === "DELETE") {
    await env.DB.prepare("DELETE FROM avisos_push WHERE endpoint=? AND usuario=?").bind(String(b.endpoint || ""), yo.id).run();
    return J({ ok: true });
  }

  // ---------- Reto del día: las mismas preguntas para todos ----------
  if (ruta === "reto" && M === "POST") {
    const dia = String(b.dia || ""), ex = String(b.examen || "");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(dia) || Math.abs(Date.parse(dia) - Date.parse(diaUTC())) > 2 * DIA || !EXAMENES.includes(ex)) return mal("Reto no válido");
    const total = entero(b.total, 1, 50), ac = entero(b.aciertos, 0, total), ms = entero(b.ms, 0, 36e5);
    const r = await env.DB.prepare("INSERT OR IGNORE INTO retos(usuario,dia,examen,aciertos,total,ms,creado) VALUES(?,?,?,?,?,?,?)").bind(yo.id, dia, ex, ac, total, ms, ahora()).run();
    if (r.meta.changes) {   // primer intento del día: se lo cuenta a los amigos que aún no lo han hecho
      const otros = (await env.DB.prepare(`SELECT CASE WHEN a=?1 THEN b ELSE a END AS id FROM amistades WHERE (a=?1 OR b=?1) AND estado='amigos'
        AND CASE WHEN a=?1 THEN b ELSE a END NOT IN (SELECT usuario FROM retos WHERE dia=?2 AND examen=?3)`).bind(yo.id, dia, ex).all()).results;
      for (const o of otros.slice(0, 40)) luego(avisa(env, o.id, { title: `⚡ ${nombreDe(yo)}: ${ac}/${total} en el reto de hoy`, body: "Mismas preguntas para todos. ¿Le superas?", url: `/?reto=${ex}`, tag: "reto" }));
    }
    return J({ ok: true, nuevo: !!r.meta.changes });
  }
  if (ruta === "reto" && M === "GET") {
    const dia = String(u.searchParams.get("dia") || ""), ex = String(u.searchParams.get("examen") || "");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(dia) || !EXAMENES.includes(ex)) return mal("Reto no válido");
    const r = await env.DB.prepare(`SELECT r.aciertos, r.total, r.ms, u.* FROM retos r JOIN usuarios u ON u.id=r.usuario
      WHERE r.dia=?2 AND r.examen=?3 AND (r.usuario=?1 OR r.usuario IN (SELECT CASE WHEN a=?1 THEN b ELSE a END FROM amistades WHERE (a=?1 OR b=?1) AND estado='amigos'))
      ORDER BY r.aciertos DESC, r.ms ASC LIMIT 100`).bind(yo.id, dia, ex).all();
    return J({ tabla: r.results.map(x => ({ ...publico(x), aciertos: x.aciertos, total: x.total, ms: x.ms, yo: x.id === yo.id })) });
  }

  // ---------- Clases ----------
  if (ruta === "clases" && M === "GET") {
    const r = await env.DB.prepare(`SELECT c.id, c.codigo, c.nombre, m.rol, (SELECT COUNT(*) FROM clase_miembros WHERE clase=c.id) AS n
      FROM clases c JOIN clase_miembros m ON m.clase=c.id WHERE m.usuario=? ORDER BY c.creado DESC`).bind(yo.id).all();
    return J({ clases: r.results });
  }
  if (ruta === "clases" && M === "POST") {
    if (await freno(env, "cla:" + yo.id, 10, 86400e3)) return mal("Demasiadas clases creadas hoy", 429);
    const nombre = limpio(b.nombre, 60);
    if (nombre.length < 2) return mal("Ponle un nombre a la clase");
    const n = await env.DB.prepare("SELECT COUNT(*) AS n FROM clases WHERE profe=?").bind(yo.id).first();
    if (n.n >= 20) return mal("Máximo 20 clases por profe");
    let c = null;
    for (let i = 0; i < 5 && !c; i++) c = await env.DB.prepare("INSERT OR IGNORE INTO clases(codigo,nombre,profe,creado) VALUES(?,?,?,?) RETURNING id, codigo").bind(codigoClase(), nombre, yo.id, ahora()).first();
    if (!c) return mal("Prueba otra vez", 500);
    await env.DB.prepare("INSERT INTO clase_miembros(clase,usuario,rol,unido) VALUES(?,?,'profe',?)").bind(c.id, yo.id, ahora()).run();
    return J({ id: c.id, codigo: c.codigo }, 201);
  }
  if (ruta === "clases/unirse" && M === "POST") {
    if (await freno(env, "unir:" + yo.id, 20, 3600e3)) return mal("Demasiados intentos. Prueba dentro de una hora.", 429);
    const c = await env.DB.prepare("SELECT * FROM clases WHERE codigo=?").bind(normCod(b.codigo).slice(0, 6)).first();
    if (!c) return mal("No hay ninguna clase con ese código", 404);
    const n = await env.DB.prepare("SELECT COUNT(*) AS n FROM clase_miembros WHERE clase=?").bind(c.id).first();
    if (n.n >= 200) return mal("La clase está llena");
    const r = await env.DB.prepare("INSERT OR IGNORE INTO clase_miembros(clase,usuario,rol,unido) VALUES(?,?,'alumno',?)").bind(c.id, yo.id, ahora()).run();
    if (r.meta.changes) luego(avisa(env, c.profe, { title: `🎓 ${nombreDe(yo)} se ha unido`, body: `Nuevo alumno en «${c.nombre}»`, url: `/?clase=${c.id}`, tag: "clase-" + c.id }));
    return J({ id: c.id });
  }
  if ((m = ruta.match(/^clases\/(\d+)(?:\/(salir|chat|miembros\/([a-z0-9_.]{3,20})))?$/i))) {
    const c = await miembro(env, +m[1], yo.id);
    if (!c) return mal("No estás en esa clase", 403);
    const profe = c.rol === "profe";
    if (!m[2] && M === "GET") {
      const r = await env.DB.prepare("SELECT u.*, m.rol FROM clase_miembros m JOIN usuarios u ON u.id=m.usuario WHERE m.clase=? ORDER BY m.rol DESC, u.xp DESC").bind(c.id).all();
      // los alumnos ven la liga de la clase; el resumen de cada uno solo lo ve el profe
      const gente = r.results.map(x => ({ ...publico(x), rol: x.rol, ...(profe || x.id === yo.id ? { resumen: JSON.parse(x.resumen || "{}") } : {}) }));
      return J({ clase: { id: c.id, nombre: c.nombre, codigo: c.codigo, rol: c.rol }, gente });
    }
    if (!m[2] && M === "PATCH" && profe) {
      const nombre = limpio(b.nombre, 60);
      if (nombre.length < 2) return mal("Ponle un nombre a la clase");
      await env.DB.prepare("UPDATE clases SET nombre=? WHERE id=?").bind(nombre, c.id).run();
      return J({ ok: true });
    }
    if (!m[2] && M === "DELETE" && profe) {
      await env.DB.batch([
        env.DB.prepare("DELETE FROM clase_mensajes WHERE clase=?").bind(c.id),
        env.DB.prepare("DELETE FROM clase_miembros WHERE clase=?").bind(c.id),
        env.DB.prepare("DELETE FROM clases WHERE id=?").bind(c.id),
      ]);
      return J({ ok: true });
    }
    if (m[2] === "salir" && M === "POST") {
      if (profe) return mal("Eres el profe: borra la clase si quieres cerrarla");
      await env.DB.prepare("DELETE FROM clase_miembros WHERE clase=? AND usuario=?").bind(c.id, yo.id).run();
      return J({ ok: true });
    }
    if (m[3] && M === "DELETE" && profe) {
      const otro = await porNombre(env, m[3]);
      if (otro && otro.id !== yo.id) await env.DB.prepare("DELETE FROM clase_miembros WHERE clase=? AND usuario=?").bind(c.id, otro.id).run();
      return J({ ok: true });
    }
    if (m[2] === "chat" && M === "GET") {
      const desde = Math.max(0, Math.floor(+u.searchParams.get("desde") || 0));
      const r = await env.DB.prepare(`SELECT * FROM (SELECT x.id, x.de, x.texto, x.tipo, x.creado, u.nombre AS usuario, COALESCE(u.mostrar,u.nombre) AS nombre, u.avatar
        FROM clase_mensajes x LEFT JOIN usuarios u ON u.id=x.de WHERE x.clase=? AND x.id>? ORDER BY x.id DESC LIMIT 100) ORDER BY id`).bind(c.id, desde).all();
      return J({ mensajes: r.results.map(x => ({ id: x.id, mio: x.de === yo.id, texto: x.texto, tipo: x.tipo, creado: x.creado, nombre: x.nombre || "—", avatar: x.avatar || "🙂", usuario: x.usuario })) });
    }
    if (m[2] === "chat" && M === "POST") {
      if (await freno(env, "msg:" + yo.id, 30, 60e3)) return mal("Vas muy rápido. Espera un momento.", 429);
      const texto = limpio(b.texto, 500), tipo = profe && ["deberes", "aviso"].includes(b.tipo) ? b.tipo : null;
      if (!texto) return mal("Mensaje vacío");
      const r = await env.DB.prepare("INSERT INTO clase_mensajes(clase,de,texto,tipo,creado) VALUES(?,?,?,?,?) RETURNING id, creado").bind(c.id, yo.id, texto, tipo, ahora()).first();
      // los avisos del profe llegan a todos; los mensajes de alumnos no despiertan móviles
      if (profe) {
        const otros = (await env.DB.prepare("SELECT usuario FROM clase_miembros WHERE clase=? AND usuario<>?").bind(c.id, yo.id).all()).results;
        for (const o of otros.slice(0, 40)) luego(avisa(env, o.usuario, { title: `${tipo === "deberes" ? "📌 Deberes" : "🎓"} · ${c.nombre}`, body: texto.slice(0, 140), url: `/?clase=${c.id}`, tag: "clase-" + c.id }));
      }
      return J({ id: r.id, mio: true, texto, tipo, creado: r.creado, nombre: nombreDe(yo), avatar: yo.avatar || "🙂", usuario: yo.nombre }, 201);
    }
    return mal("No permitido", 403);
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
      luego(avisa(env, otro.id, { title: `💬 ${nombreDe(yo)}`, body: texto.slice(0, 140), url: `/?chat=${yo.nombre}`, tag: "chat-" + yo.nombre, chat: yo.nombre }));
      return J({ id: r.id, mio: true, texto, creado: r.creado }, 201);
    }
  }

  return mal("No existe", 404);
}
