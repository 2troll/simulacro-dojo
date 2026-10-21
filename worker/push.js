// Web Push gratis y sin servicios externos: VAPID (RFC 8292) + cifrado aes128gcm (RFC 8291) con WebCrypto.
const te = new TextEncoder();
const b64u = buf => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const deB64u = s => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/") + "===".slice((s.length + 3) % 4)), c => c.charCodeAt(0));
const junta = (...ps) => { const o = new Uint8Array(ps.reduce((n, p) => n + p.length, 0)); let i = 0; for (const p of ps) { o.set(p, i); i += p.length; } return o; };

async function hkdf(salt, ikm, info, n) {
  const k = await crypto.subtle.importKey("raw", ikm, "HKDF", false, ["deriveBits"]);
  return new Uint8Array(await crypto.subtle.deriveBits({ name: "HKDF", hash: "SHA-256", salt, info }, k, n * 8));
}

export async function vapid(env, endpoint) {
  const jwk = JSON.parse(env.VAPID_JWK);
  const key = await crypto.subtle.importKey("jwk", jwk, { name: "ECDSA", namedCurve: "P-256" }, false, ["sign"]);
  const cab = b64u(te.encode(JSON.stringify({ typ: "JWT", alg: "ES256" })));
  const cuerpo = b64u(te.encode(JSON.stringify({ aud: new URL(endpoint).origin, exp: Math.floor(Date.now() / 1000) + 12 * 3600, sub: "mailto:tony@tonykansaiguide.com" })));
  const firma = await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, key, te.encode(cab + "." + cuerpo));   // WebCrypto ya da r||s, el formato de JWT
  const pub = b64u(junta(new Uint8Array([4]), deB64u(jwk.x), deB64u(jwk.y)));
  return `vapid t=${cab}.${cuerpo}.${b64u(firma)}, k=${pub}`;
}

export async function cifra(sub, texto) {
  const uaPub = deB64u(sub.p256dh), auth = deB64u(sub.auth);
  const efimera = await crypto.subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveBits"]);
  const asPub = new Uint8Array(await crypto.subtle.exportKey("raw", efimera.publicKey));
  const ua = await crypto.subtle.importKey("raw", uaPub, { name: "ECDH", namedCurve: "P-256" }, false, []);
  const secreto = new Uint8Array(await crypto.subtle.deriveBits({ name: "ECDH", public: ua }, efimera.privateKey, 256));
  const ikm = await hkdf(auth, secreto, junta(te.encode("WebPush: info\0"), uaPub, asPub), 32);
  const sal = crypto.getRandomValues(new Uint8Array(16));
  const cek = await hkdf(sal, ikm, te.encode("Content-Encoding: aes128gcm\0"), 16);
  const nonce = await hkdf(sal, ikm, te.encode("Content-Encoding: nonce\0"), 12);
  const k = await crypto.subtle.importKey("raw", cek, "AES-GCM", false, ["encrypt"]);
  const cifrado = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv: nonce }, k, junta(te.encode(texto), new Uint8Array([2]))));
  const rs = new Uint8Array([0, 0, 16, 0]);   // tamaño de registro 4096
  return junta(sal, rs, new Uint8Array([asPub.length]), asPub, cifrado);
}

// Manda un aviso a una suscripción. Devuelve false si el navegador ya la dio de baja (hay que borrarla).
export async function empuja(env, sub, datos) {
  const r = await fetch(sub.endpoint, {
    method: "POST",
    headers: { authorization: await vapid(env, sub.endpoint), "content-encoding": "aes128gcm", "content-type": "application/octet-stream", ttl: "86400", urgency: "normal" },
    body: await cifra(sub, JSON.stringify(datos)),
  });
  if (r.status === 404 || r.status === 410) return false;
  if (!r.ok) console.warn("push", r.status, await r.text().catch(() => ""));
  return true;
}

// Avisa a todos los dispositivos de un usuario (y limpia los que ya no existen)
export async function avisa(env, usuario, datos) {
  if (!env.VAPID_JWK) return;
  const subs = (await env.DB.prepare("SELECT * FROM avisos_push WHERE usuario=?").bind(usuario).all()).results;
  for (const s of subs) {
    try { if (!(await empuja(env, s, datos))) await env.DB.prepare("DELETE FROM avisos_push WHERE endpoint=?").bind(s.endpoint).run(); }
    catch (e) { console.warn("push", e.message); }
  }
}
