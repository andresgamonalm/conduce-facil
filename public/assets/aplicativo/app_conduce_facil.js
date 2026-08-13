/* Conduce-Fácil · Arranque, estructura común y navegación.
   Aplicativo de estudio para el examen teórico de la Licencia de Conducir
   Clase B en Chile. Contenidos: Manual CONASET y Manual de Señalización. */

import {
  alNavegar, h, icono, marcaSvg, navegar, registrarRuta, resolver, vaciar,
} from './nucleo_conduce_facil.js';
import { crearRepositorio } from './almacenamiento_conduce_facil.js';
import { cargarSesionUsuario, estado } from './contexto_conduce_facil.js';
import { cargarDatos } from './datos_conduce_facil.js';
import { cerrarSesion, vistaAdmin, vistaConfiguracion, vistaLogin } from './vistas_acceso_conduce_facil.js';
import { vistaCapitulo, vistaEstudio, vistaHome, vistaRepaso } from './vistas_estudio_conduce_facil.js';
import { vistaResultados, vistaTest, vistaTrivia } from './vistas_ejercicios_conduce_facil.js';

const RAIZ = document.getElementById('raiz');

const SECCIONES = [
  { ruta: '/home', etiqueta: 'Inicio', icono: 'home' },
  { ruta: '/estudio', etiqueta: 'Estudio', icono: 'estudio' },
  { ruta: '/trivia', etiqueta: 'Trivia', icono: 'trivia' },
  { ruta: '/test', etiqueta: 'Test', icono: 'test' },
  { ruta: '/resultados', etiqueta: 'Resultados', icono: 'resultados' },
  { ruta: '/repaso', etiqueta: 'Repaso', icono: 'repaso', secundaria: true },
  { ruta: '/configuracion', etiqueta: 'Configuración', icono: 'config', secundaria: true },
  { ruta: '/admin', etiqueta: 'Administración', icono: 'admin', soloAdmin: true, secundaria: true },
];

/* ------------------------------------------------------------ Estructura --- */

function enlaceNav(seccion) {
  return h('a', {
    href: seccion.ruta, 'data-ruta': '', 'data-seccion': seccion.ruta,
    class: `nav-enlace${seccion.secundaria ? ' nav-secundario' : ''}`,
  }, [icono(seccion.icono), seccion.etiqueta]);
}

function estructura() {
  const contenido = h('div', { class: 'contenedor' });
  const visibles = SECCIONES.filter((s) => !s.soloAdmin || estado.usuario.rol === 'admin');

  /* En móvil la barra inferior muestra las cinco secciones de práctica y agrupa
     el resto tras «Más», que despliega una fila adicional sobre la barra. Los
     enlaces son los mismos nodos en ambos casos: no se duplica la navegación. */
  const botonMas = h('button', {
    type: 'button', class: 'nav-enlace nav-mas', 'aria-expanded': 'false',
    onclick: (evento) => {
      const abierto = navegacion.classList.toggle('expandida');
      evento.currentTarget.setAttribute('aria-expanded', String(abierto));
    },
  }, [icono('config'), 'Más']);

  const navegacion = h('nav', { class: 'navegacion', 'aria-label': 'Secciones' },
    h('div', { class: 'contenedor' }, [...visibles.map(enlaceNav), botonMas]));

  navegacion.addEventListener('click', (evento) => {
    if (evento.target.closest('a')) {
      navegacion.classList.remove('expandida');
      botonMas.setAttribute('aria-expanded', 'false');
    }
  });

  const iniciales = (estado.usuario.nombre || estado.usuario.usuario).trim().charAt(0).toUpperCase();

  return h('div', {}, [
    h('header', { class: 'barra-superior' }, h('div', { class: 'contenedor' }, [
      h('a', { href: '/home', 'data-ruta': '', class: 'marca-app', 'aria-label': 'Conduce-Fácil, ir al inicio' }, [
        marcaSvg(34), h('span', { class: 'palabra', html: 'Conduce<em>-Fácil</em>' }),
      ]),
      h('div', { class: 'usuario-menu' }, [
        h('span', { class: 'usuario-chip' }, [
          h('span', { class: 'usuario-avatar' }, iniciales),
          h('span', { class: 'nombre' }, estado.usuario.nombre || estado.usuario.usuario),
        ]),
        h('button', {
          type: 'button', class: 'boton boton-secundario', onclick: cerrarSesion,
          'aria-label': 'Cerrar sesión',
        }, [icono('salir'), h('span', { class: 'nombre' }, 'Salir')]),
      ]),
    ])),
    navegacion,
    h('main', {}, contenido),
    h('footer', { class: 'pie' }, h('div', { class: 'contenedor' }, [
      h('div', {}, [
        h('p', { style: 'margin:0 0 4px' }, [
          h('strong', {}, 'Conduce-Fácil'), ' · Preparación del examen teórico Clase B.',
        ]),
        h('p', { style: 'margin:0;font-size:13px' },
          'Contenidos del Libro para la Conducción en Chile (CONASET, julio 2024) y del Manual de Señalización de Tránsito (MTT). Se reproducen sin modificaciones.'),
      ]),
      h('div', { class: 'endoso' }, [
        h('span', {}, 'Desarrollado por'),
        (() => {
          const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
          svg.setAttribute('viewBox', '0 0 48 48');
          svg.setAttribute('aria-hidden', 'true');
          const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
          use.setAttribute('href', '#i-gamonal');
          svg.append(use);
          return svg;
        })(),
        h('strong', {}, 'Gamonal'),
      ]),
    ])),
  ]);
}

let contenidoActual = null;

function marcarSeccionActiva(ruta) {
  document.querySelectorAll('.nav-enlace[data-seccion]').forEach((enlace) => {
    const seccion = enlace.dataset.seccion;
    const activo = ruta === seccion || (seccion !== '/home' && ruta.startsWith(`${seccion}/`));
    if (activo) enlace.setAttribute('aria-current', 'page');
    else enlace.removeAttribute('aria-current');
  });
}

function pintarEnMarco(pintor, parametros) {
  if (!contenidoActual || !document.body.contains(contenidoActual)) {
    const marco = estructura();
    vaciar(RAIZ).append(marco);
    contenidoActual = marco.querySelector('main > .contenedor');
  }
  vaciar(contenidoActual);
  const consulta = new URLSearchParams(window.location.search);
  pintor(contenidoActual, parametros || {}, consulta);
  marcarSeccionActiva(window.location.pathname);
  window.scrollTo(0, 0);
}

function pantallaCompleta(pintor) {
  contenidoActual = null;
  vaciar(RAIZ);
  pintor(RAIZ);
}

function protegida(pintor) {
  return (parametros) => {
    if (!estado.usuario) return navegar('/login', true);
    return pintarEnMarco(pintor, parametros);
  };
}

/* --------------------------------------------------------------- Rutas ----- */

registrarRuta('/login', () => {
  if (estado.usuario) return navegar('/home', true);
  return pantallaCompleta(vistaLogin);
});
registrarRuta('/', () => navegar(estado.usuario ? '/home' : '/login', true));
registrarRuta('/home', protegida(vistaHome));
registrarRuta('/estudio', protegida(vistaEstudio));
registrarRuta('/estudio/:capitulo', protegida(vistaCapitulo));
registrarRuta('/trivia', protegida(vistaTrivia));
registrarRuta('/test', protegida(vistaTest));
registrarRuta('/repaso', protegida(vistaRepaso));
registrarRuta('/resultados', protegida(vistaResultados));
registrarRuta('/configuracion', protegida(vistaConfiguracion));
registrarRuta('/admin', protegida(vistaAdmin));

alNavegar((ruta) => marcarSeccionActiva(ruta));

/* -------------------------------------------------------------- Arranque --- */

function pantallaError(mensaje) {
  vaciar(RAIZ).append(h('div', { class: 'contenedor', style: 'padding-top:64px' }, [
    h('h1', {}, 'No se pudo iniciar Conduce-Fácil'),
    h('div', { class: 'aviso aviso-error' }, mensaje),
    h('p', {}, 'Vuelve a cargar la página. Si el problema persiste, revisa que los archivos de la carpeta datos estén disponibles.'),
  ]));
}

async function iniciar() {
  try {
    estado.repo = await crearRepositorio();
    estado.datos = await cargarDatos();
    const sesion = await estado.repo.sesion();
    if (sesion) await cargarSesionUsuario(sesion);
    resolver();
  } catch (error) {
    console.error(error);
    pantallaError(String(error && error.message ? error.message : error));
  }
}

iniciar();
