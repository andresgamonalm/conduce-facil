/**
 * Conduce-Fácil · API opcional para Cloudflare Pages Functions.
 *
 * Se activa sola cuando el proyecto tiene enlazada una base de datos D1 con el
 * binding `DB`. Mientras no exista ese enlace, el aplicativo funciona en modo
 * local (todo en el navegador) y esta API responde que no está disponible.
 *
 * Endpoints:
 *   GET    /api/salud
 *   POST   /api/sesion              { usuario, clave }
 *   GET    /api/sesion
 *   DELETE /api/sesion
 *   GET    /api/usuarios                       (administración)
 *   POST   /api/usuarios            { usuario, nombre, clave, rol }   (administración)
 *   DELETE /api/usuarios/:id                   (administración)
 *   POST   /api/clave               { usuarioId, claveActual, claveNueva }
 *   GET    /api/progreso/:id        · PUT /api/progreso/:id      { progreso }
 *   GET    /api/preferencias/:id    · PUT /api/preferencias/:id  { preferencias }
 */

const ITERACIONES = 150000;
const DURACION_SESION = 60 * 60 * 24 * 30; // 30 días
const CUENTA_INICIAL = {
  usuario: 'andres',
  nombre: 'Andrés',
  rol: 'admin',
  salt: 'CAEQKGj5WOgwzMWd/rYSSg==',
  hash: 'XPv9/N7mO97o4hfwIT/focAKGwV9kZmwqnxsy4XOUi4=',
};

/* --------------------------------------------------------------- Utilidad -- */

const json = (cuerpo, estado = 200, cabeceras = {}) => new Response(JSON.stringify(cuerpo), {
  status: estado,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...cabeceras },
});

const base64 = (buffer) => btoa(String.fromCharCode(...new Uint8Array(buffer)));
const desdeBase64 = (texto) => Uint8Array.from(atob(texto), (c) => c.charCodeAt(0));

async function derivar(clave, saltBase64) {
  const salt = saltBase64 ? desdeBase64(saltBase64) : crypto.getRandomValues(new Uint8Array(16));
  const material = await crypto.subtle.importKey('raw', new TextEncoder().encode(clave), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits(
    { name: 'PBKDF2', salt, iterations: ITERACIONES, hash: 'SHA-256' }, material, 256,
  );
  return { salt: base64(salt), hash: base64(bits) };
}

async function verificar(clave, salt, hash) {
  const derivada = await derivar(clave, salt);
  if (derivada.hash.length !== hash.length) return false;
  let diferencia = 0;
  for (let i = 0; i < hash.length; i++) diferencia |= derivada.hash.charCodeAt(i) ^ hash.charCodeAt(i);
  return diferencia === 0;
}

function identificador() {
  return base64(crypto.getRandomValues(new Uint8Array(12))).replace(/[^a-zA-Z0-9]/g, '').slice(0, 12);
}

/* ------------------------------------------------------- Esquema y semilla -- */

async function preparar(db) {
  await db.batch([
    db.prepare(`CREATE TABLE IF NOT EXISTS usuarios (
      id TEXT PRIMARY KEY,
      usuario TEXT NOT NULL UNIQUE,
      nombre TEXT NOT NULL,
      rol TEXT NOT NULL DEFAULT 'estudiante',
      salt TEXT NOT NULL,
      hash TEXT NOT NULL,
      creado TEXT NOT NULL
    )`),
    db.prepare(`CREATE TABLE IF NOT EXISTS sesiones (
      token TEXT PRIMARY KEY,
      usuario_id TEXT NOT NULL,
      expira INTEGER NOT NULL
    )`),
    db.prepare(`CREATE TABLE IF NOT EXISTS progreso (
      usuario_id TEXT PRIMARY KEY,
      datos TEXT NOT NULL,
      actualizado TEXT NOT NULL
    )`),
    db.prepare(`CREATE TABLE IF NOT EXISTS preferencias (
      usuario_id TEXT PRIMARY KEY,
      datos TEXT NOT NULL
    )`),
  ]);
  const { total } = await db.prepare('SELECT COUNT(*) AS total FROM usuarios').first();
  if (!total) {
    await db.prepare(
      'INSERT INTO usuarios (id, usuario, nombre, rol, salt, hash, creado) VALUES (?, ?, ?, ?, ?, ?, ?)',
    ).bind(
      'usuario-inicial', CUENTA_INICIAL.usuario, CUENTA_INICIAL.nombre, CUENTA_INICIAL.rol,
      CUENTA_INICIAL.salt, CUENTA_INICIAL.hash, new Date().toISOString(),
    ).run();
  }
}

/* -------------------------------------------------------------- Sesiones --- */

function leerCookie(request, nombre) {
  const cookies = request.headers.get('Cookie') || '';
  for (const parte of cookies.split(';')) {
    const [clave, ...valor] = parte.trim().split('=');
    if (clave === nombre) return valor.join('=');
  }
  return null;
}

function cookieSesion(token, segundos) {
  const atributos = [
    `cf_sesion=${token}`, 'Path=/', 'HttpOnly', 'Secure', 'SameSite=Lax',
    `Max-Age=${segundos}`,
  ];
  return atributos.join('; ');
}

async function usuarioDeSesion(db, request) {
  const token = leerCookie(request, 'cf_sesion');
  if (!token) return null;
  const fila = await db.prepare(
    `SELECT u.id, u.usuario, u.nombre, u.rol, s.expira
       FROM sesiones s JOIN usuarios u ON u.id = s.usuario_id
      WHERE s.token = ?`,
  ).bind(token).first();
  if (!fila) return null;
  if (fila.expira < Math.floor(Date.now() / 1000)) {
    await db.prepare('DELETE FROM sesiones WHERE token = ?').bind(token).run();
    return null;
  }
  return { id: fila.id, usuario: fila.usuario, nombre: fila.nombre, rol: fila.rol };
}

/* ------------------------------------------------------------- Enrutador --- */

export async function onRequest(context) {
  const { request, env, params } = context;
  const partes = [].concat(params.ruta || []).filter(Boolean);
  const db = env.DB;

  if (!db) {
    return json({ ok: false, error: 'La base de datos no está enlazada. El aplicativo funciona en modo local.' }, 200);
  }

  try {
    await preparar(db);
  } catch (error) {
    return json({ ok: false, error: `No se pudo preparar la base de datos: ${error.message}` }, 500);
  }

  const metodo = request.method.toUpperCase();
  const recurso = partes[0] || '';
  const identificadorRuta = partes[1] || null;

  if (recurso === 'salud') return json({ ok: true, modo: 'servidor' });

  /* --- Sesión ------------------------------------------------------------ */
  if (recurso === 'sesion') {
    if (metodo === 'POST') {
      const cuerpo = await request.json().catch(() => ({}));
      const nombreUsuario = String(cuerpo.usuario || '').trim().toLowerCase();
      const cuenta = await db.prepare('SELECT * FROM usuarios WHERE lower(usuario) = ?').bind(nombreUsuario).first();
      const generico = { ok: false, error: 'Usuario o contraseña incorrectos.' };
      if (!cuenta) return json(generico, 401);
      if (!(await verificar(String(cuerpo.clave || ''), cuenta.salt, cuenta.hash))) return json(generico, 401);
      const token = `${identificador()}${identificador()}`;
      const expira = Math.floor(Date.now() / 1000) + DURACION_SESION;
      await db.prepare('INSERT INTO sesiones (token, usuario_id, expira) VALUES (?, ?, ?)')
        .bind(token, cuenta.id, expira).run();
      return json(
        { ok: true, usuario: { id: cuenta.id, usuario: cuenta.usuario, nombre: cuenta.nombre, rol: cuenta.rol } },
        200,
        { 'Set-Cookie': cookieSesion(token, DURACION_SESION) },
      );
    }
    if (metodo === 'DELETE') {
      const token = leerCookie(request, 'cf_sesion');
      if (token) await db.prepare('DELETE FROM sesiones WHERE token = ?').bind(token).run();
      return json({ ok: true }, 200, { 'Set-Cookie': cookieSesion('', 0) });
    }
    const usuario = await usuarioDeSesion(db, request);
    return usuario ? json({ ok: true, usuario }) : json({ ok: false }, 401);
  }

  const sesion = await usuarioDeSesion(db, request);
  if (!sesion) return json({ ok: false, error: 'Sesión no válida.' }, 401);
  const esAdmin = sesion.rol === 'admin';

  /* --- Usuarios ---------------------------------------------------------- */
  if (recurso === 'usuarios') {
    if (metodo === 'GET') {
      if (!esAdmin) return json({ ok: true, usuarios: [{ id: sesion.id, usuario: sesion.usuario, nombre: sesion.nombre, rol: sesion.rol }] });
      const { results } = await db.prepare('SELECT id, usuario, nombre, rol, creado FROM usuarios ORDER BY creado').all();
      return json({ ok: true, usuarios: results });
    }
    if (metodo === 'POST') {
      if (!esAdmin) return json({ ok: false, error: 'Sólo la administración puede crear cuentas.' }, 403);
      const cuerpo = await request.json().catch(() => ({}));
      const nombreUsuario = String(cuerpo.usuario || '').trim().toLowerCase();
      if (!/^[a-z0-9._-]{3,24}$/.test(nombreUsuario)) {
        return json({ ok: false, error: 'El usuario debe tener entre 3 y 24 caracteres (letras, números, punto, guion o guion bajo).' });
      }
      if (String(cuerpo.clave || '').length < 6) {
        return json({ ok: false, error: 'La contraseña debe tener al menos 6 caracteres.' });
      }
      const existente = await db.prepare('SELECT id FROM usuarios WHERE lower(usuario) = ?').bind(nombreUsuario).first();
      if (existente) return json({ ok: false, error: 'Ya existe una cuenta con ese usuario.' });
      const { salt, hash } = await derivar(String(cuerpo.clave));
      await db.prepare('INSERT INTO usuarios (id, usuario, nombre, rol, salt, hash, creado) VALUES (?, ?, ?, ?, ?, ?, ?)')
        .bind(identificador(), nombreUsuario, String(cuerpo.nombre || nombreUsuario).trim(),
          cuerpo.rol === 'admin' ? 'admin' : 'estudiante', salt, hash, new Date().toISOString()).run();
      return json({ ok: true });
    }
    if (metodo === 'DELETE' && identificadorRuta) {
      if (!esAdmin) return json({ ok: false, error: 'Sólo la administración puede eliminar cuentas.' }, 403);
      if (identificadorRuta === sesion.id) return json({ ok: false, error: 'No puedes eliminar tu propia cuenta.' });
      const admins = await db.prepare("SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'admin'").first();
      const objetivo = await db.prepare('SELECT rol FROM usuarios WHERE id = ?').bind(identificadorRuta).first();
      if (!objetivo) return json({ ok: false, error: 'No se encontró la cuenta.' });
      if (objetivo.rol === 'admin' && admins.total <= 1) {
        return json({ ok: false, error: 'Debe quedar al menos una cuenta con permisos de administración.' });
      }
      await db.batch([
        db.prepare('DELETE FROM usuarios WHERE id = ?').bind(identificadorRuta),
        db.prepare('DELETE FROM sesiones WHERE usuario_id = ?').bind(identificadorRuta),
        db.prepare('DELETE FROM progreso WHERE usuario_id = ?').bind(identificadorRuta),
        db.prepare('DELETE FROM preferencias WHERE usuario_id = ?').bind(identificadorRuta),
      ]);
      return json({ ok: true });
    }
  }

  /* --- Contraseña -------------------------------------------------------- */
  if (recurso === 'clave' && metodo === 'POST') {
    const cuerpo = await request.json().catch(() => ({}));
    if (cuerpo.usuarioId !== sesion.id) return json({ ok: false, error: 'Sólo puedes cambiar tu propia contraseña.' }, 403);
    if (String(cuerpo.claveNueva || '').length < 6) {
      return json({ ok: false, error: 'La contraseña nueva debe tener al menos 6 caracteres.' });
    }
    const cuenta = await db.prepare('SELECT salt, hash FROM usuarios WHERE id = ?').bind(sesion.id).first();
    if (!(await verificar(String(cuerpo.claveActual || ''), cuenta.salt, cuenta.hash))) {
      return json({ ok: false, error: 'La contraseña actual no es correcta.' });
    }
    const { salt, hash } = await derivar(String(cuerpo.claveNueva));
    await db.prepare('UPDATE usuarios SET salt = ?, hash = ? WHERE id = ?').bind(salt, hash, sesion.id).run();
    return json({ ok: true });
  }

  /* --- Progreso y preferencias ------------------------------------------- */
  const puedeVer = (objetivo) => objetivo === sesion.id || esAdmin;
  const puedeEscribir = (objetivo) => objetivo === sesion.id;

  if (recurso === 'progreso' && identificadorRuta) {
    if (metodo === 'GET') {
      if (!puedeVer(identificadorRuta)) return json({ ok: false, error: 'Sin permisos.' }, 403);
      const fila = await db.prepare('SELECT datos FROM progreso WHERE usuario_id = ?').bind(identificadorRuta).first();
      return json({ ok: true, progreso: fila ? JSON.parse(fila.datos) : null });
    }
    if (metodo === 'PUT') {
      if (!puedeEscribir(identificadorRuta)) return json({ ok: false, error: 'Sin permisos.' }, 403);
      const cuerpo = await request.json().catch(() => ({}));
      await db.prepare(
        `INSERT INTO progreso (usuario_id, datos, actualizado) VALUES (?, ?, ?)
         ON CONFLICT(usuario_id) DO UPDATE SET datos = excluded.datos, actualizado = excluded.actualizado`,
      ).bind(identificadorRuta, JSON.stringify(cuerpo.progreso || {}), new Date().toISOString()).run();
      return json({ ok: true });
    }
  }

  if (recurso === 'preferencias' && identificadorRuta) {
    if (metodo === 'GET') {
      if (!puedeVer(identificadorRuta)) return json({ ok: false, error: 'Sin permisos.' }, 403);
      const fila = await db.prepare('SELECT datos FROM preferencias WHERE usuario_id = ?').bind(identificadorRuta).first();
      return json({ ok: true, preferencias: fila ? JSON.parse(fila.datos) : {} });
    }
    if (metodo === 'PUT') {
      if (!puedeEscribir(identificadorRuta)) return json({ ok: false, error: 'Sin permisos.' }, 403);
      const cuerpo = await request.json().catch(() => ({}));
      await db.prepare(
        `INSERT INTO preferencias (usuario_id, datos) VALUES (?, ?)
         ON CONFLICT(usuario_id) DO UPDATE SET datos = excluded.datos`,
      ).bind(identificadorRuta, JSON.stringify(cuerpo.preferencias || {})).run();
      return json({ ok: true });
    }
  }

  return json({ ok: false, error: 'Recurso no encontrado.' }, 404);
}
