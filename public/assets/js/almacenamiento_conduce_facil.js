/* Conduce-Fácil · Almacenamiento y cuentas
   Funciona de dos maneras según el entorno:
   · Modo local  : todo se guarda en el navegador (localStorage). Es el modo con
                   el que el aplicativo funciona apenas se abre, sin instalar nada.
   · Modo servidor: si existe la API en /api (Cloudflare Pages Functions + D1),
                   las cuentas y los resultados se guardan de forma centralizada y
                   la persona administradora ve los resultados de todas las demás.
   La interfaz es la misma en ambos casos, de modo que las vistas no cambian. */

import { derivarClave, idAleatorio, verificarClave } from './nucleo_conduce_facil.js';

const LLAVE_USUARIOS = 'conduce-facil.usuarios';
const LLAVE_SESION = 'conduce-facil.sesion';
const LLAVE_PROGRESO = 'conduce-facil.progreso.';
const LLAVE_PREFERENCIAS = 'conduce-facil.preferencias.';

/* Cuentas definidas por la propiedad del proyecto. De cada una se guarda
   únicamente la derivación PBKDF2-SHA256 de su contraseña: el texto plano no
   existe en el código ni en el repositorio.
   El campo «version» permite corregir una contraseña sembrada: cuando el
   navegador guarda una versión anterior a la de aquí, la reemplaza al abrir.
   Las contraseñas que cada persona cambie desde /configuracion quedan marcadas
   y no se sobrescriben nunca. */
const CUENTAS_INICIALES = [
  {
    id: 'usuario-inicial',
    usuario: 'andres',
    nombre: 'Andrés',
    rol: 'admin',
    salt: 'GrjxWZdtiDfqPyuVXt7OyQ==',
    hash: 'EsYwGuMMwJ4btJgbrlXqhf1REOfsQaDGZtktZwLll7M=',
    iteraciones: 150000,
    version: 3,
  },
  {
    id: 'usuario-lorena',
    usuario: 'lorena',
    nombre: 'Lorena',
    rol: 'estudiante',
    salt: 'IqnQll6mnzZtT64Y6fwjkQ==',
    hash: 'HdZVwSCXgwVlyk+7qD971W4ZQDrh+C8u0eTR0nRDnQ8=',
    iteraciones: 150000,
    version: 1,
  },
];

/* Las cuentas creadas antes de que se guardara este dato usaban 150.000
   iteraciones; se asume ese valor cuando el registro no lo indica. */
const ITERACIONES_HEREDADAS = 150000;
const iteracionesDe = (cuenta) => cuenta.iteraciones || ITERACIONES_HEREDADAS;

export const PROGRESO_VACIO = () => ({
  estudio: {},
  preguntas: {},
  senales: {},
  sesiones: [],
});

function leerJson(llave, porDefecto) {
  try {
    const crudo = localStorage.getItem(llave);
    return crudo ? JSON.parse(crudo) : porDefecto;
  } catch (error) {
    console.warn('No se pudo leer', llave, error);
    return porDefecto;
  }
}

function escribirJson(llave, valor) {
  try {
    localStorage.setItem(llave, JSON.stringify(valor));
    return true;
  } catch (error) {
    console.warn('No se pudo guardar', llave, error);
    return false;
  }
}

/* ---------------------------------------------------------- Modo local ---- */

class RepositorioLocal {
  constructor() { this.modo = 'local'; }

  /** Deja este navegador al día con las cuentas del repositorio: añade las que
   *  falten y corrige las que estén desactualizadas. Se ejecuta al abrir, de
   *  modo que cualquiera puede entrar desde cualquier dispositivo sin más que
   *  cargar la página. No toca las cuentas creadas desde /admin ni las
   *  contraseñas que cada persona haya cambiado por su cuenta. */
  async iniciar() {
    const usuarios = leerJson(LLAVE_USUARIOS, []);
    let cambios = false;

    for (const semilla of CUENTAS_INICIALES) {
      const guardada = usuarios.find((u) => u.id === semilla.id);

      if (!guardada) {
        usuarios.push({ ...semilla, creado: new Date().toISOString() });
        cambios = true;
        continue;
      }

      if (guardada.personalizada) continue;          // contraseña propia: intocable
      if ((guardada.version || 1) >= semilla.version) continue;

      Object.assign(guardada, {
        usuario: semilla.usuario,
        nombre: semilla.nombre,
        rol: semilla.rol,
        salt: semilla.salt,
        hash: semilla.hash,
        iteraciones: semilla.iteraciones,
        version: semilla.version,
      });
      cambios = true;
    }

    if (cambios) escribirJson(LLAVE_USUARIOS, usuarios);
  }

  usuarios() { return leerJson(LLAVE_USUARIOS, []); }

  async listarUsuarios() {
    return this.usuarios().map(({ salt, hash, ...resto }) => resto);
  }

  async ingresar(usuario, clave) {
    const cuenta = this.usuarios().find((u) => u.usuario.toLowerCase() === String(usuario).trim().toLowerCase());
    if (!cuenta) return { ok: false, error: 'Usuario o contraseña incorrectos.' };
    const valida = await verificarClave(clave, cuenta.salt, cuenta.hash, iteracionesDe(cuenta));
    if (!valida) return { ok: false, error: 'Usuario o contraseña incorrectos.' };
    escribirJson(LLAVE_SESION, { usuarioId: cuenta.id, iniciada: Date.now() });
    return { ok: true, usuario: { id: cuenta.id, usuario: cuenta.usuario, nombre: cuenta.nombre, rol: cuenta.rol } };
  }

  async sesion() {
    const s = leerJson(LLAVE_SESION, null);
    if (!s) return null;
    const cuenta = this.usuarios().find((u) => u.id === s.usuarioId);
    if (!cuenta) return null;
    return { id: cuenta.id, usuario: cuenta.usuario, nombre: cuenta.nombre, rol: cuenta.rol };
  }

  async salir() { localStorage.removeItem(LLAVE_SESION); }

  async crearUsuario({ usuario, nombre, clave, rol }) {
    const limpio = String(usuario).trim().toLowerCase();
    if (!/^[a-z0-9._-]{3,24}$/.test(limpio)) {
      return { ok: false, error: 'El usuario debe tener entre 3 y 24 caracteres (letras, números, punto, guion o guion bajo).' };
    }
    if (String(clave).length < 6) return { ok: false, error: 'La contraseña debe tener al menos 6 caracteres.' };
    const usuarios = this.usuarios();
    if (usuarios.some((u) => u.usuario.toLowerCase() === limpio)) {
      return { ok: false, error: 'Ya existe una cuenta con ese usuario.' };
    }
    const { salt, hash, iteraciones } = await derivarClave(clave);
    usuarios.push({
      id: idAleatorio(), usuario: limpio, nombre: String(nombre).trim() || limpio,
      rol: rol === 'admin' ? 'admin' : 'estudiante', salt, hash, iteraciones,
      creado: new Date().toISOString(),
    });
    escribirJson(LLAVE_USUARIOS, usuarios);
    return { ok: true };
  }

  async cambiarClave(usuarioId, claveActual, claveNueva) {
    if (String(claveNueva).length < 6) return { ok: false, error: 'La contraseña nueva debe tener al menos 6 caracteres.' };
    const usuarios = this.usuarios();
    const cuenta = usuarios.find((u) => u.id === usuarioId);
    if (!cuenta) return { ok: false, error: 'No se encontró la cuenta.' };
    if (!(await verificarClave(claveActual, cuenta.salt, cuenta.hash, iteracionesDe(cuenta)))) {
      return { ok: false, error: 'La contraseña actual no es correcta.' };
    }
    const { salt, hash, iteraciones } = await derivarClave(claveNueva);
    cuenta.salt = salt;
    cuenta.hash = hash;
    cuenta.iteraciones = iteraciones;
    /* A partir de aquí la contraseña es suya: el repositorio ya no la corrige. */
    cuenta.personalizada = true;
    escribirJson(LLAVE_USUARIOS, usuarios);
    return { ok: true };
  }

  async eliminarUsuario(usuarioId) {
    const usuarios = this.usuarios().filter((u) => u.id !== usuarioId);
    if (!usuarios.some((u) => u.rol === 'admin')) {
      return { ok: false, error: 'Debe quedar al menos una cuenta con permisos de administración.' };
    }
    escribirJson(LLAVE_USUARIOS, usuarios);
    localStorage.removeItem(LLAVE_PROGRESO + usuarioId);
    return { ok: true };
  }

  async progreso(usuarioId) {
    return { ...PROGRESO_VACIO(), ...leerJson(LLAVE_PROGRESO + usuarioId, {}) };
  }

  async guardarProgreso(usuarioId, progreso) {
    escribirJson(LLAVE_PROGRESO + usuarioId, progreso);
    return { ok: true };
  }

  async preferencias(usuarioId) {
    return leerJson(LLAVE_PREFERENCIAS + usuarioId, {});
  }

  async guardarPreferencias(usuarioId, preferencias) {
    escribirJson(LLAVE_PREFERENCIAS + usuarioId, preferencias);
    return { ok: true };
  }
}

/* -------------------------------------------------------- Modo servidor ---- */

class RepositorioRemoto {
  constructor() { this.modo = 'servidor'; }

  async pedir(ruta, opciones = {}) {
    const respuesta = await fetch(`/api${ruta}`, {
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      ...opciones,
      body: opciones.cuerpo ? JSON.stringify(opciones.cuerpo) : undefined,
    });
    if (!respuesta.ok && respuesta.status !== 401) {
      /* Se intenta mostrar el motivo real que devuelve el servidor; un «500»
         a secas no permite diagnosticar nada desde el navegador. */
      const detalle = await respuesta.json().catch(() => null);
      return {
        ok: false,
        error: (detalle && detalle.error) || `Error del servidor (${respuesta.status}).`,
      };
    }
    return respuesta.json();
  }

  async iniciar() { /* el servidor crea la cuenta inicial en su primera consulta */ }

  listarUsuarios() { return this.pedir('/usuarios').then((r) => r.usuarios || []); }
  ingresar(usuario, clave) { return this.pedir('/sesion', { method: 'POST', cuerpo: { usuario, clave } }); }
  sesion() { return this.pedir('/sesion').then((r) => (r.ok ? r.usuario : null)); }
  salir() { return this.pedir('/sesion', { method: 'DELETE' }); }
  crearUsuario(datos) { return this.pedir('/usuarios', { method: 'POST', cuerpo: datos }); }
  cambiarClave(usuarioId, claveActual, claveNueva) {
    return this.pedir('/clave', { method: 'POST', cuerpo: { usuarioId, claveActual, claveNueva } });
  }
  eliminarUsuario(usuarioId) { return this.pedir(`/usuarios/${usuarioId}`, { method: 'DELETE' }); }
  progreso(usuarioId) {
    return this.pedir(`/progreso/${usuarioId}`).then((r) => ({ ...PROGRESO_VACIO(), ...(r.progreso || {}) }));
  }
  guardarProgreso(usuarioId, progreso) {
    return this.pedir(`/progreso/${usuarioId}`, { method: 'PUT', cuerpo: { progreso } });
  }
  preferencias(usuarioId) { return this.pedir(`/preferencias/${usuarioId}`).then((r) => r.preferencias || {}); }
  guardarPreferencias(usuarioId, preferencias) {
    return this.pedir(`/preferencias/${usuarioId}`, { method: 'PUT', cuerpo: { preferencias } });
  }
}

/* ------------------------------------------------------------- Selección --- */

export async function crearRepositorio() {
  try {
    const control = new AbortController();
    const tiempo = setTimeout(() => control.abort(), 2500);
    const respuesta = await fetch('/api/salud', { signal: control.signal, credentials: 'same-origin' });
    clearTimeout(tiempo);
    if (respuesta.ok) {
      const cuerpo = await respuesta.json();
      if (cuerpo && cuerpo.ok) {
        const repo = new RepositorioRemoto();
        await repo.iniciar();
        return repo;
      }
    }
  } catch (error) {
    /* Sin API disponible: se continúa en modo local. */
  }
  const repo = new RepositorioLocal();
  await repo.iniciar();
  return repo;
}

/* ------------------------------------------------------------ Estadística -- */

export function registrarRespuestaPregunta(progreso, preguntaId, acierto, segundos) {
  const actual = progreso.preguntas[preguntaId] || { intentos: 0, aciertos: 0, tiempo: 0 };
  actual.intentos += 1;
  if (acierto) actual.aciertos += 1;
  actual.tiempo += segundos;
  actual.ultima = Date.now();
  progreso.preguntas[preguntaId] = actual;
  return progreso;
}

export function registrarRespuestaSenal(progreso, codigo, acierto, segundos) {
  const actual = progreso.senales[codigo] || { intentos: 0, aciertos: 0, tiempo: 0 };
  actual.intentos += 1;
  if (acierto) actual.aciertos += 1;
  actual.tiempo += segundos;
  actual.ultima = Date.now();
  progreso.senales[codigo] = actual;
  return progreso;
}

export function registrarTarjeta(progreso, tarjetaId, dominada) {
  const actual = progreso.estudio[tarjetaId] || { vistas: 0, dominada: false };
  actual.vistas += 1;
  actual.dominada = Boolean(dominada);
  actual.ultima = Date.now();
  progreso.estudio[tarjetaId] = actual;
  return progreso;
}

export function registrarSesion(progreso, sesion) {
  progreso.sesiones.unshift(sesion);
  progreso.sesiones = progreso.sesiones.slice(0, 200);
  return progreso;
}
