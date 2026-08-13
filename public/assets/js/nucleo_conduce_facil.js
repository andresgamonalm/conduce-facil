/* Conduce-Fácil · Núcleo
   Utilidades compartidas: creación de nodos, formato, aleatoriedad reproducible
   y el enrutador de la aplicación. */

export const NOMBRE_APP = 'Conduce-Fácil';

/* ------------------------------------------------------------------ DOM ---- */

export function h(etiqueta, atributos = {}, hijos = []) {
  const nodo = document.createElement(etiqueta);
  for (const [clave, valor] of Object.entries(atributos)) {
    if (valor === null || valor === undefined || valor === false) continue;
    if (clave === 'class') nodo.className = valor;
    else if (clave === 'html') nodo.innerHTML = valor;
    else if (clave === 'texto') nodo.textContent = valor;
    else if (clave === 'dataset') Object.assign(nodo.dataset, valor);
    else if (clave.startsWith('on') && typeof valor === 'function') {
      nodo.addEventListener(clave.slice(2), valor);
    } else nodo.setAttribute(clave, valor === true ? '' : valor);
  }
  for (const hijo of [].concat(hijos)) {
    if (hijo === null || hijo === undefined || hijo === false) continue;
    nodo.append(hijo instanceof Node ? hijo : document.createTextNode(String(hijo)));
  }
  return nodo;
}

export function icono(nombre, clase = '') {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('focusable', 'false');
  if (clase) svg.setAttribute('class', clase);
  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
  use.setAttribute('href', `#i-${nombre}`);
  svg.append(use);
  return svg;
}

export function marcaSvg(alto = 34, negativo = false) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 128 128');
  svg.setAttribute('width', alto);
  svg.setAttribute('height', alto);
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', NOMBRE_APP);
  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
  use.setAttribute('href', negativo ? '#i-marca-negativo' : '#i-marca');
  svg.append(use);
  return svg;
}

export function vaciar(nodo) {
  while (nodo.firstChild) nodo.removeChild(nodo.firstChild);
  return nodo;
}

/* --------------------------------------------------------------- Formato --- */

export function formatearSegundos(segundos) {
  const s = Math.max(0, Math.round(segundos));
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${String(m).padStart(2, '0')}:${String(r).padStart(2, '0')}`;
}

export function formatearDuracion(segundos) {
  const s = Math.max(0, Math.round(segundos));
  if (s < 60) return `${s} s`;
  const m = Math.floor(s / 60);
  const r = s % 60;
  return r ? `${m} min ${r} s` : `${m} min`;
}

export function formatearFecha(marca) {
  const d = new Date(marca);
  return d.toLocaleString('es-CL', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

export function porcentaje(parte, total) {
  if (!total) return 0;
  return Math.round((parte / total) * 100);
}

/* ------------------------------------------------------------ Aleatorio --- */

export function mezclar(lista, aleatorio = Math.random) {
  const copia = lista.slice();
  for (let i = copia.length - 1; i > 0; i--) {
    const j = Math.floor(aleatorio() * (i + 1));
    [copia[i], copia[j]] = [copia[j], copia[i]];
  }
  return copia;
}

export function tomar(lista, cantidad) {
  return mezclar(lista).slice(0, cantidad);
}

/* --------------------------------------------------------------- Cripto --- */

const CODIF = new TextEncoder();

function base64(buffer) {
  return btoa(String.fromCharCode(...new Uint8Array(buffer)));
}

function desdeBase64(texto) {
  return Uint8Array.from(atob(texto), (c) => c.charCodeAt(0));
}

/* La contraseña se deriva en el navegador, que no tiene límite de CPU, así que
   se usa la protección completa recomendada. Cada cuenta guarda con cuántas
   iteraciones se derivó la suya, de modo que cambiar este valor no invalida las
   cuentas existentes.
   Aviso: el plan gratuito de Cloudflare Workers concede 10 ms de CPU por
   petición y este cálculo consume unos 100 ms. Si algún día se activara la API
   del servidor, habría que bajarlo o contratar el plan Workers Paid. */
export const ITERACIONES = 150000;

/* Cada cuenta guarda con cuántas iteraciones se derivó su contraseña. Así,
   cambiar el valor por omisión no invalida las cuentas ya existentes: cada una
   se verifica con el número que le corresponde. */
export async function derivarClave(clave, saltBase64, iteraciones = ITERACIONES) {
  const salt = saltBase64 ? desdeBase64(saltBase64) : crypto.getRandomValues(new Uint8Array(16));
  const material = await crypto.subtle.importKey('raw', CODIF.encode(clave), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits(
    { name: 'PBKDF2', salt, iterations: iteraciones, hash: 'SHA-256' },
    material,
    256,
  );
  return { salt: base64(salt), hash: base64(bits), iteraciones };
}

export async function verificarClave(clave, saltBase64, hashBase64, iteraciones = ITERACIONES) {
  const { hash } = await derivarClave(clave, saltBase64, iteraciones);
  if (hash.length !== hashBase64.length) return false;
  let diferencia = 0;
  for (let i = 0; i < hash.length; i++) diferencia |= hash.charCodeAt(i) ^ hashBase64.charCodeAt(i);
  return diferencia === 0;
}

export function idAleatorio() {
  return base64(crypto.getRandomValues(new Uint8Array(12))).replace(/[^a-zA-Z0-9]/g, '').slice(0, 12);
}

/* ------------------------------------------------------------- Enrutador --- */

const rutas = new Map();
let alCambiar = null;

export function registrarRuta(patron, manejador) {
  rutas.set(patron, manejador);
}

export function alNavegar(callback) {
  alCambiar = callback;
}

export function rutaActual() {
  const ruta = window.location.pathname.replace(/\/+$/, '') || '/';
  return ruta === '/index.html' ? '/' : ruta;
}

export function navegar(destino, reemplazar = false) {
  if (reemplazar) window.history.replaceState({}, '', destino);
  else window.history.pushState({}, '', destino);
  resolver();
}

export function resolver() {
  const ruta = rutaActual();
  for (const [patron, manejador] of rutas) {
    const partesPatron = patron.split('/').filter(Boolean);
    const partesRuta = ruta.split('/').filter(Boolean);
    if (partesPatron.length !== partesRuta.length) continue;
    const parametros = {};
    let coincide = true;
    for (let i = 0; i < partesPatron.length; i++) {
      if (partesPatron[i].startsWith(':')) parametros[partesPatron[i].slice(1)] = decodeURIComponent(partesRuta[i]);
      else if (partesPatron[i] !== partesRuta[i]) { coincide = false; break; }
    }
    if (coincide) {
      if (alCambiar) alCambiar(ruta, patron, parametros);
      return manejador(parametros);
    }
  }
  return navegar('/home', true);
}

window.addEventListener('popstate', () => resolver());

document.addEventListener('click', (evento) => {
  const enlace = evento.target.closest('a[data-ruta]');
  if (!enlace) return;
  evento.preventDefault();
  navegar(enlace.getAttribute('href'));
});
