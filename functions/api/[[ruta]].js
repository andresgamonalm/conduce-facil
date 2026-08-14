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

const DURACION_SESION = 60 * 60 * 24 * 30; // 30 días

/* Las 150.000 iteraciones de PBKDF2 las ejecuta el navegador, que no tiene
   límite de tiempo de cálculo, y envía su resultado. Aquí sólo se comprueba un
   SHA-256 de ese resultado: cuesta microsegundos y cabe de sobra en los 10 ms
   de CPU que concede el plan gratuito. Lo almacenado no sirve para entrar:
   quien obtuviera la base tendría que romper antes esas 150.000 iteraciones. */
const CUENTAS_INICIALES = [
  { id: 'usuario-inicial', usuario: 'andres', nombre: 'Andrés', rol: 'admin',
    verificador: 'bpEBMjgfbis+kW/kH+pHg25vfad8U+IIG6Bl53irsNw=' },
  { id: 'usuario-lorena', usuario: 'lorena', nombre: 'Lorena', rol: 'estudiante',
    verificador: 'LgTAm/SXIDpdXyINZDrL5uR/lF7GZtVJbiltuo+0J6k=' },
  { id: 'usuario-invitado', usuario: 'invitado', nombre: 'Invitado', rol: 'estudiante',
    verificador: 'cbP2igLv3xRBCPofnBENLgKEjC1OZf5HH7LXKeytbbw=' },
];

/* --------------------------------------------------------------- Utilidad -- */

const json = (cuerpo, estado = 200, cabeceras = {}) => new Response(JSON.stringify(cuerpo), {
  status: estado,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...cabeceras },
});

const base64 = (buffer) => btoa(String.fromCharCode(...new Uint8Array(buffer)));
const desdeBase64 = (texto) => Uint8Array.from(atob(texto), (c) => c.charCodeAt(0));

async function verificadorDe(derivada) {
  return base64(await crypto.subtle.digest('SHA-256', desdeBase64(String(derivada || ''))));
}

function coincide(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let diferencia = 0;
  for (let i = 0; i < a.length; i++) diferencia |= a.charCodeAt(i) ^ b.charCodeAt(i);
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
      verificador TEXT NOT NULL,
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
    /* Ediciones del contenido hechas desde /editor. Se guarda sólo lo que
       cambia respecto del texto publicado, de modo que restaurar el original
       es simplemente borrar la fila. */
    db.prepare(`CREATE TABLE IF NOT EXISTS contenidos (
      id TEXT PRIMARY KEY,
      tipo TEXT NOT NULL,
      datos TEXT NOT NULL,
      actualizado TEXT NOT NULL
    )`),
  ]);
  /* Las cuentas definidas en el repositorio se siembran si faltan, de modo que
     la base queda al día sola tras un despliegue. Las contraseñas que cada
     persona haya cambiado no se tocan: sólo se insertan las que no existen. */
  const ahora = new Date().toISOString();
  await db.batch(CUENTAS_INICIALES.map((c) => db.prepare(
    'INSERT OR IGNORE INTO usuarios (id, usuario, nombre, rol, verificador, creado) VALUES (?, ?, ?, ?, ?, ?)',
  ).bind(c.id, c.usuario, c.nombre, c.rol, c.verificador, ahora)));
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
  /* Cualquier fallo inesperado se devuelve con su motivo: un 500 sin cuerpo no
     permite diagnosticar nada desde el navegador. */
  try {
    return await enrutar(context);
  } catch (error) {
    return json({ ok: false, error: `Fallo en el servidor: ${error && error.message ? error.message : error}` }, 500);
  }
}

async function enrutar(context) {
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

  /* Las ediciones del contenido las lee todo el mundo -son el material de
     estudio- pero sólo la administración puede modificarlas. */
  if (recurso === 'contenidos' && metodo === 'GET') {
    const { results } = await db.prepare('SELECT id, tipo, datos FROM contenidos').all();
    const ediciones = {};
    for (const fila of results) {
      try { ediciones[fila.id] = { tipo: fila.tipo, ...JSON.parse(fila.datos) }; } catch (e) { /* fila ilegible */ }
    }
    return json({ ok: true, ediciones });
  }

  /* --- Sesión ------------------------------------------------------------ */
  if (recurso === 'sesion') {
    if (metodo === 'POST') {
      const cuerpo = await request.json().catch(() => ({}));
      const nombreUsuario = String(cuerpo.usuario || '').trim().toLowerCase();
      const cuenta = await db.prepare('SELECT * FROM usuarios WHERE lower(usuario) = ?').bind(nombreUsuario).first();
      const generico = { ok: false, error: 'Usuario o contraseña incorrectos.' };
      if (!cuenta) return json(generico, 401);
      if (!coincide(await verificadorDe(cuerpo.derivada), cuenta.verificador)) return json(generico, 401);
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

  /* --- Contenidos -------------------------------------------------------- */
  if (recurso === 'contenidos') {
    if (!esAdmin) return json({ ok: false, error: 'Sólo la administración puede editar los contenidos.' }, 403);
    if (!identificadorRuta) return json({ ok: false, error: 'Falta el identificador del contenido.' }, 400);

    if (metodo === 'PUT') {
      const cuerpo = await request.json().catch(() => ({}));
      const tipo = cuerpo.tipo === 'pregunta' ? 'pregunta' : 'estudio';
      await db.prepare(
        `INSERT INTO contenidos (id, tipo, datos, actualizado) VALUES (?, ?, ?, ?)
         ON CONFLICT(id) DO UPDATE SET tipo = excluded.tipo, datos = excluded.datos, actualizado = excluded.actualizado`,
      ).bind(identificadorRuta, tipo, JSON.stringify(cuerpo.datos || {}), new Date().toISOString()).run();
      return json({ ok: true });
    }

    if (metodo === 'DELETE') {
      await db.prepare('DELETE FROM contenidos WHERE id = ?').bind(identificadorRuta).run();
      return json({ ok: true });
    }
  }

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
      await db.prepare('INSERT INTO usuarios (id, usuario, nombre, rol, verificador, creado) VALUES (?, ?, ?, ?, ?, ?)')
        .bind(identificador(), nombreUsuario, String(cuerpo.nombre || nombreUsuario).trim(),
          cuerpo.rol === 'admin' ? 'admin' : 'estudiante', String(cuerpo.verificador || ''), new Date().toISOString()).run();
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
    const cuenta = await db.prepare('SELECT verificador FROM usuarios WHERE id = ?').bind(sesion.id).first();
    if (!coincide(await verificadorDe(cuerpo.derivadaActual), cuenta.verificador)) {
      return json({ ok: false, error: 'La contraseña actual no es correcta.' });
    }
    await db.prepare('UPDATE usuarios SET verificador = ? WHERE id = ?')
      .bind(String(cuerpo.verificadorNuevo || ''), sesion.id).run();
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
