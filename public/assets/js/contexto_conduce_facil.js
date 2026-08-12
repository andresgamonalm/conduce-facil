/* Conduce-Fácil · Estado compartido de la sesión en curso. */

import { PROGRESO_VACIO } from './almacenamiento_conduce_facil.js';

export const estado = {
  repo: null,
  datos: null,
  usuario: null,
  progreso: PROGRESO_VACIO(),
  preferencias: { mostrarCronometro: true, segundosPorPregunta: 0 },
};

let guardadoPendiente = null;
let hayCambiosSinGuardar = false;

/** Guarda el progreso.
 *  En modo local la escritura es inmediata (localStorage es síncrono y muy
 *  barato). En modo servidor se agrupa con un pequeño retardo para no lanzar una
 *  petición por cada clic, y se fuerza el envío antes de abandonar la página. */
export function guardarProgreso() {
  if (!estado.usuario) return;
  if (estado.repo.modo === 'local') {
    estado.repo.guardarProgreso(estado.usuario.id, estado.progreso);
    return;
  }
  hayCambiosSinGuardar = true;
  clearTimeout(guardadoPendiente);
  guardadoPendiente = setTimeout(() => {
    hayCambiosSinGuardar = false;
    estado.repo.guardarProgreso(estado.usuario.id, estado.progreso);
  }, 600);
}

export async function guardarProgresoAhora() {
  if (!estado.usuario) return;
  clearTimeout(guardadoPendiente);
  hayCambiosSinGuardar = false;
  await estado.repo.guardarProgreso(estado.usuario.id, estado.progreso);
}

/* Ningún avance se pierde al cerrar la pestaña o cambiar de página. */
window.addEventListener('pagehide', () => {
  if (hayCambiosSinGuardar) guardarProgresoAhora();
});
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden' && hayCambiosSinGuardar) guardarProgresoAhora();
});

export function guardarPreferencias() {
  if (!estado.usuario) return;
  estado.repo.guardarPreferencias(estado.usuario.id, estado.preferencias);
}

export async function cargarSesionUsuario(usuario) {
  estado.usuario = usuario;
  estado.progreso = await estado.repo.progreso(usuario.id);
  const preferencias = await estado.repo.preferencias(usuario.id);
  estado.preferencias = { mostrarCronometro: true, segundosPorPregunta: 0, ...preferencias };
}

export function limpiarSesion() {
  estado.usuario = null;
  estado.progreso = PROGRESO_VACIO();
  estado.preferencias = { mostrarCronometro: true, segundosPorPregunta: 0 };
}
