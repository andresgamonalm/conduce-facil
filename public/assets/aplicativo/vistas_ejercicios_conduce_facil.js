/* Conduce-Fácil · Trivia de señalética, Test de prueba y Resultados. */

import {
  formatearDuracion, formatearFecha, formatearSegundos, h, icono, idAleatorio,
  navegar, porcentaje, vaciar,
} from './nucleo_conduce_facil.js';
import { estado, guardarProgreso, guardarProgresoAhora } from './contexto_conduce_facil.js';
import {
  registrarRespuestaPregunta, registrarRespuestaSenal, registrarSesion,
} from './almacenamiento_conduce_facil.js';
import { armarTest, armarTrivia, maximoErrores } from './datos_conduce_facil.js';

const LETRAS = ['A', 'B', 'C', 'D', 'E'];

/** Dibujo con que el Manual CONASET plantea el caso de la pregunta. Se muestra
 *  junto al enunciado porque el examen teórico presenta esas mismas
 *  ilustraciones. La imagen es la del manual, sin adaptaciones. */
function ilustracionesDelCaso(pregunta) {
  const figuras = pregunta.figuras || [];
  if (!figuras.length) return null;
  return h('figure', { class: 'caso-manual' }, [
    h('div', { class: 'caso-manual-imagenes' }, figuras.map((src) => h('img', {
      src, alt: 'Ilustración del Manual CONASET que acompaña a este caso', loading: 'lazy',
    }))),
    h('figcaption', {}, `Ilustración del Manual CONASET, página ${pregunta.pagina}.`),
  ]);
}

/* ================================================================= Motor === */

/** Ejecuta una tanda de preguntas con cronómetro por pregunta y por sesión. */
function ejecutarEjercicio(raiz, config) {
  const {
    titulo, subtitulo, preguntas, tipo, limitePorPregunta = 0,
    revisionInmediata = true, alTerminar,
  } = config;

  const respuestas = [];
  let indice = 0;
  let inicioPregunta = 0;
  const inicioSesion = Date.now();
  let cronometro = null;

  const contador = h('span', { class: 'contador-preguntas' });
  const relojPregunta = h('span', {}, '00:00');
  const cajaReloj = h('div', { class: 'cronometro' }, [icono('reloj'), relojPregunta]);
  if (!estado.preferencias.mostrarCronometro) cajaReloj.classList.add('oculto');
  const barra = h('span', { style: 'width:0%' });
  const escenario = h('div', { class: 'escenario' });

  const cabecera = h('div', {}, [
    h('div', { class: 'migas' }, [h('a', { href: '/home', 'data-ruta': '' }, 'Inicio'), ' › ', titulo]),
    h('div', { class: 'cabecera-ejercicio' }, [
      h('div', {}, [h('h1', { style: 'margin-bottom:4px' }, titulo), h('p', { style: 'margin:0;color:var(--gris-medio)' }, subtitulo)]),
      h('div', { style: 'display:flex;align-items:center;gap:16px' }, [contador, cajaReloj]),
    ]),
    h('div', { class: 'barra-progreso', style: 'margin-bottom:24px' }, barra),
  ]);

  raiz.append(cabecera, escenario);

  function tictac() {
    const transcurrido = (Date.now() - inicioPregunta) / 1000;
    if (limitePorPregunta > 0) {
      const restante = Math.max(0, limitePorPregunta - transcurrido);
      relojPregunta.textContent = formatearSegundos(restante);
      cajaReloj.classList.toggle('alerta', restante <= 10);
      if (restante <= 0) responder(null);
    } else {
      relojPregunta.textContent = formatearSegundos(transcurrido);
    }
  }

  function pintar() {
    clearInterval(cronometro);
    if (indice >= preguntas.length) return terminar();

    const pregunta = preguntas[indice];
    contador.textContent = `Pregunta ${indice + 1} de ${preguntas.length}`;
    barra.style.width = `${porcentaje(indice, preguntas.length)}%`;
    inicioPregunta = Date.now();
    relojPregunta.textContent = limitePorPregunta > 0 ? formatearSegundos(limitePorPregunta) : '00:00';
    cajaReloj.classList.remove('alerta');
    cronometro = setInterval(tictac, 250);

    const botones = pregunta.opciones.map((texto, i) => h('button', {
      type: 'button', class: 'opcion', 'data-indice': String(i),
      onclick: () => responder(i),
    }, [h('span', { class: 'letra' }, LETRAS[i]), h('span', {}, texto)]));

    const cuerpo = [
      pregunta.imagen
        ? h('figure', { class: 'marco-senal', style: 'margin:0' }, [
          h('img', { src: pregunta.imagen, alt: 'Señal de tránsito del Manual de Señalización de Tránsito' }),
        ])
        : null,
      ilustracionesDelCaso(pregunta),
      h('h2', { style: 'margin:0' }, pregunta.enunciado),
      h('div', { class: 'opciones', role: 'group', 'aria-label': 'Alternativas' }, botones),
      h('div', { class: 'retroalimentacion' }),
    ].filter(Boolean);

    vaciar(escenario).append(...cuerpo);
  }

  function responder(eleccion) {
    clearInterval(cronometro);
    const pregunta = preguntas[indice];
    const segundos = (Date.now() - inicioPregunta) / 1000;
    const acierto = eleccion === pregunta.correcta;
    respuestas.push({ pregunta, eleccion, acierto, segundos });

    if (pregunta.tipo === 'senal') registrarRespuestaSenal(estado.progreso, pregunta.codigo, acierto, segundos);
    else registrarRespuestaPregunta(estado.progreso, pregunta.id, acierto, segundos);
    guardarProgreso();

    const botones = [...escenario.querySelectorAll('.opcion')];
    botones.forEach((boton, i) => {
      boton.disabled = true;
      if (i === pregunta.correcta) boton.classList.add('correcta');
      else if (i === eleccion) boton.classList.add('incorrecta');
    });

    const zona = escenario.querySelector('.retroalimentacion');
    const ultimaPregunta = indice === preguntas.length - 1;
    const siguiente = h('button', {
      type: 'button', class: 'boton boton-principal',
      onclick: () => { indice += 1; pintar(); },
    }, ultimaPregunta ? ['Ver mi resultado', icono('flecha')] : ['Siguiente pregunta', icono('flecha')]);

    if (revisionInmediata) {
      vaciar(zona).append(
        h('div', { class: `aviso ${acierto ? 'aviso-exito' : 'aviso-error'}`, style: 'margin:0 0 16px' },
          acierto
            ? `Correcto. Respondiste en ${formatearDuracion(segundos)}.`
            : (eleccion === null
              ? `Se agotó el tiempo. La respuesta correcta es: ${pregunta.opciones[pregunta.correcta]}.`
              : `Incorrecto. La respuesta correcta es: ${pregunta.opciones[pregunta.correcta]}.`)),
        pregunta.fundamento
          ? h('div', { class: 'tarjeta-turquesa', style: 'margin-bottom:16px' }, [
            h('p', { style: 'margin:0' }, pregunta.fundamento),
            h('p', { class: 'cita', style: 'margin:8px 0 0' }, `Manual CONASET, página ${pregunta.pagina}.`),
          ])
          : h('p', { class: 'cita', style: 'margin:0 0 16px' },
            `Señal ${pregunta.codigo} · ${pregunta.grupo} · Manual de Señalización de Tránsito, ${pregunta.fuente.replace('.pdf', '')}, página ${pregunta.pagina}.`),
        siguiente,
      );
    } else {
      vaciar(zona).append(siguiente);
    }
    zona.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  async function terminar() {
    clearInterval(cronometro);
    barra.style.width = '100%';
    const correctas = respuestas.filter((r) => r.acierto).length;
    const duracion = (Date.now() - inicioSesion) / 1000;
    const maxErr = maximoErrores(preguntas.length);
    const sesion = {
      id: idAleatorio(),
      tipo,
      fecha: Date.now(),
      total: preguntas.length,
      correctas,
      duracion,
      maxErrores: maxErr,
      aprobado: preguntas.length - correctas <= maxErr,
      detalle: respuestas.map((r) => ({
        id: r.pregunta.id,
        tipo: r.pregunta.tipo,
        enunciado: r.pregunta.enunciado,
        codigo: r.pregunta.codigo || null,
        correcta: r.pregunta.opciones[r.pregunta.correcta],
        elegida: r.eleccion === null ? null : r.pregunta.opciones[r.eleccion],
        acierto: r.acierto,
        segundos: Math.round(r.segundos * 10) / 10,
        pagina: r.pregunta.pagina || null,
      })),
    };
    registrarSesion(estado.progreso, sesion);
    await guardarProgresoAhora();
    cabecera.remove();
    vaciar(escenario);
    escenario.classList.remove('escenario');
    alTerminar(escenario, sesion, respuestas);
  }

  pintar();
}

/* ------------------------------------------------------ Resumen de tanda --- */

function pintarResumen(contenedor, sesion, respuestas, opcionesRepetir) {
  const errores = sesion.total - sesion.correctas;
  const tiempoMedio = sesion.detalle.reduce((a, d) => a + d.segundos, 0) / Math.max(1, sesion.total);

  contenedor.append(h('section', {
    class: `resumen-resultado ${sesion.aprobado ? 'resumen-aprobado' : 'resumen-reprobado'}`,
  }, [
    h('div', { class: 'puntaje' }, [
      h('div', { class: 'valor' }, `${sesion.correctas}`),
      h('div', { class: 'total' }, `de ${sesion.total} correctas`),
    ]),
    h('div', {}, [
      h('h1', { style: 'margin-bottom:8px' }, sesion.aprobado ? '¡Aprobado!' : 'Todavía no alcanza'),
      h('p', { style: 'margin-bottom:12px' }, sesion.aprobado
        ? `Cometiste ${errores} ${errores === 1 ? 'error' : 'errores'} y el máximo permitido en esta práctica es ${sesion.maxErrores}.`
        : `Cometiste ${errores} ${errores === 1 ? 'error' : 'errores'} y el máximo permitido en esta práctica es ${sesion.maxErrores}. Repasa y vuelve a intentarlo.`),
      h('p', { style: 'margin:0;font-size:15px' }, [
        `Tiempo total: ${formatearDuracion(sesion.duracion)} · Promedio por pregunta: ${formatearDuracion(tiempoMedio)}`,
      ]),
    ]),
  ]));

  contenedor.append(h('div', { class: 'grupo-botones', style: 'margin-bottom:32px' }, [
    h('button', { type: 'button', class: 'boton boton-principal', onclick: opcionesRepetir.repetir }, 'Repetir la práctica'),
    h('a', { href: '/repaso', 'data-ruta': '', class: 'boton boton-secundario' }, [icono('repaso'), 'Ver qué repasar']),
    h('a', { href: '/resultados', 'data-ruta': '', class: 'boton boton-secundario' }, [icono('resultados'), 'Historial completo']),
  ]));

  contenedor.append(h('h2', {}, 'Revisión pregunta por pregunta'));
  contenedor.append(h('div', { class: 'lista-debilidades' }, respuestas.map((r, i) => {
    const p = r.pregunta;
    return h('details', { class: 'tarjeta', open: !r.acierto }, [
      h('summary', { style: 'cursor:pointer;list-style:none;display:flex;gap:12px;justify-content:space-between;align-items:flex-start' }, [
        h('span', { style: 'font-weight:500;color:var(--azul)' }, `${i + 1}. ${p.enunciado}`),
        h('span', { style: 'display:flex;gap:8px;flex:0 0 auto;align-items:center' }, [
          h('span', { style: 'font-size:13px;color:var(--gris-medio)' }, formatearDuracion(r.segundos)),
          h('span', { class: `etiqueta ${r.acierto ? 'etiqueta-exito' : 'etiqueta-error'}` }, r.acierto ? 'Correcta' : 'Incorrecta'),
        ]),
      ]),
      h('div', { style: 'padding-top:16px' }, [
        p.imagen ? h('figure', { class: 'marco-senal', style: 'margin:0 0 16px;min-height:0;padding:16px' }, [
          h('img', { src: p.imagen, alt: p.opciones[p.correcta], style: 'max-height:150px' }),
        ]) : null,
        ilustracionesDelCaso(p),
        h('p', { style: 'margin-bottom:6px' }, [h('strong', {}, 'Correcta: '), p.opciones[p.correcta]]),
        r.acierto ? null : h('p', { style: 'margin-bottom:6px;color:var(--error-fuerte)' }, [
          h('strong', {}, 'Tu respuesta: '), r.eleccion === null ? 'Sin responder (se agotó el tiempo)' : p.opciones[r.eleccion],
        ]),
        p.fundamento
          ? h('div', { class: 'tarjeta-turquesa' }, [
            h('p', { style: 'margin:0' }, p.fundamento),
            h('p', { class: 'cita', style: 'margin:8px 0 0' }, `Manual CONASET, página ${p.pagina}.`),
          ])
          : h('p', { class: 'cita', style: 'margin:0' },
            `Señal ${p.codigo} · ${p.grupo} · Manual de Señalización de Tránsito, página ${p.pagina}.`),
      ]),
    ]);
  })));
}

/* -------------------------------------------------------------- /trivia ---- */

export function vistaTrivia(raiz, parametros, consulta) {
  document.title = 'Trivia de señalética · Conduce-Fácil';
  const { datos } = estado;
  const grupoInicial = consulta.get('grupo') || 'todos';

  let grupo = grupoInicial;
  let cantidad = 20;

  const contenedor = h('div', {});
  raiz.append(contenedor);

  function pintarConfiguracion() {
    vaciar(contenedor);
    const disponibles = grupo === 'todos' ? datos.senales.length : datos.senales.filter((s) => s.grupo === grupo).length;

    const chipsGrupo = h('div', { class: 'lista-chips' }, [
      chip('Todas las familias', grupo === 'todos', () => { grupo = 'todos'; pintarConfiguracion(); },
        `${datos.senales.length}`),
      ...datos.gruposSenales.map((g) => chip(
        g.nombre, grupo === g.nombre, () => { grupo = g.nombre; pintarConfiguracion(); },
        String(datos.senales.filter((s) => s.grupo === g.nombre).length),
      )),
    ]);

    const chipsCantidad = h('div', { class: 'lista-chips' }, [10, 20, 30, 50].map((n) => chip(
      `${n} señales`, cantidad === n, () => { cantidad = n; pintarConfiguracion(); },
    )));

    const descripcion = grupo === 'todos'
      ? 'Se mezclan todas las familias del Manual de Señalización.'
      : (datos.gruposSenales.find((g) => g.nombre === grupo) || {}).descripcion || '';

    contenedor.append(
      h('div', { class: 'cabecera-pagina' }, [
        h('h1', {}, 'Trivia de señalética'),
        h('p', {}, [
          'Se muestra la señal sin su nombre y eliges entre cuatro alternativas. Las ',
          h('strong', {}, `${datos.senales.length} señales`),
          ' provienen del ', h('strong', {}, datos.fuenteSenales), '.',
        ]),
      ]),
      h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
        h('h2', {}, 'Familia de señales'),
        chipsGrupo,
        descripcion ? h('p', { style: 'color:var(--gris-medio);margin:16px 0 0' }, descripcion) : null,
      ]),
      h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
        h('h2', {}, 'Cantidad de señales'),
        chipsCantidad,
        h('p', { style: 'color:var(--gris-medio);margin:16px 0 0' },
          `Disponibles en esta familia: ${disponibles}. Se usarán ${Math.min(cantidad, disponibles)}.`),
      ]),
      h('div', { class: 'grupo-botones' }, [
        h('button', {
          type: 'button', class: 'boton boton-turquesa',
          onclick: () => iniciar(),
        }, [icono('trivia'), 'Comenzar la trivia']),
        h('a', { href: '/home', 'data-ruta': '', class: 'boton boton-secundario' }, 'Volver al inicio'),
      ]),
      galeriaSenales(datos, grupo),
    );
  }

  function iniciar() {
    const preguntas = armarTrivia(datos, { cantidad, grupo });
    vaciar(contenedor);
    ejecutarEjercicio(contenedor, {
      titulo: 'Trivia de señalética',
      subtitulo: grupo === 'todos' ? 'Todas las familias' : grupo,
      preguntas,
      tipo: 'trivia',
      limitePorPregunta: 0,
      alTerminar: (destino, sesion, respuestas) => {
        pintarResumen(destino, sesion, respuestas, { repetir: () => { pintarConfiguracion(); window.scrollTo(0, 0); } });
      },
    });
    window.scrollTo(0, 0);
  }

  pintarConfiguracion();
}

/** Catálogo completo de la familia seleccionada: se muestran todas las señales,
 *  nunca una muestra parcial, de modo que la cifra del filtro y lo que se ve en
 *  pantalla siempre coinciden. Cada imagen es la del Manual de Señalización. */
function galeriaSenales(datos, grupo) {
  const lista = grupo === 'todos' ? datos.senales : datos.senales.filter((s) => s.grupo === grupo);
  const rotulo = grupo === 'todos' ? 'todas las familias' : `la familia ${grupo}`;
  return h('section', { class: 'tarjeta', style: 'margin-top:24px' }, [
    h('h2', {}, 'Catálogo de señales'),
    h('p', { style: 'color:var(--gris-medio)' },
      `Las ${lista.length} señales de ${rotulo}, tal como aparecen en el manual oficial. Entran todas en la trivia.`),
    h('div', { class: 'catalogo-senales' }, lista.map((s) => h('figure', {
      class: 'ficha-senal', title: `${s.nombre} (${s.codigo})`,
    }, [
      h('div', { class: 'ficha-senal-imagen' },
        h('img', { src: `/assets/senales/${s.archivo}`, alt: s.nombre, loading: 'lazy', decoding: 'async' })),
      h('figcaption', {}, [
        h('span', { class: 'ficha-senal-codigo' }, s.codigo),
        h('span', { class: 'ficha-senal-nombre' }, s.nombre),
      ]),
    ]))),
  ]);
}

function chip(texto, activo, alPulsar, sufijo) {
  return h('button', {
    type: 'button', class: 'chip', 'aria-pressed': activo ? 'true' : 'false', onclick: alPulsar,
  }, [texto, sufijo ? h('span', { style: 'opacity:.75' }, sufijo) : null]);
}

/* ---------------------------------------------------------------- /test ---- */

export function vistaTest(raiz, parametros, consulta) {
  document.title = 'Test de prueba · Conduce-Fácil';
  const { datos } = estado;

  const capituloInicial = consulta.get('capitulo');
  let cantidad = 35;
  let capitulos = capituloInicial ? [capituloInicial] : datos.capitulos.map((c) => c.id);
  let incluirSenaletica = !capituloInicial;
  let limite = estado.preferencias.segundosPorPregunta || 0;

  const contenedor = h('div', {});
  raiz.append(contenedor);

  function pintarConfiguracion() {
    vaciar(contenedor);
    const maxErr = maximoErrores(cantidad);
    const bancoDisponible = datos.preguntas.filter((p) => capitulos.includes(p.capitulo)).length;

    const chipsCantidad = h('div', { class: 'lista-chips' }, [10, 20, 35, 50].map((n) => chip(
      `${n} preguntas`, cantidad === n, () => { cantidad = n; pintarConfiguracion(); },
    )));

    const casillasCapitulos = h('div', { class: 'rejilla rejilla-2', style: 'gap:0 24px' },
      datos.capitulos.map((cap) => {
        const id = `cap-${cap.id}`;
        return h('div', { class: 'opcion-caja' }, [
          h('input', {
            type: 'checkbox', id, checked: capitulos.includes(cap.id),
            onchange: (evento) => {
              if (evento.currentTarget.checked) capitulos = [...new Set([...capitulos, cap.id])];
              else capitulos = capitulos.filter((c) => c !== cap.id);
              if (!capitulos.length) {
                capitulos = [cap.id];
                evento.currentTarget.checked = true;
              }
              pintarConfiguracion();
            },
          }),
          h('label', { for: id }, [
            cap.titulo,
            h('span', { style: 'color:var(--gris-medio)' }, ` · ${datos.porCapitulo.get(cap.id).preguntas.length} preguntas`),
          ]),
        ]);
      }));

    const casillaSenales = h('input', {
      type: 'checkbox', id: 'incluir-senales', checked: incluirSenaletica,
      onchange: (evento) => { incluirSenaletica = evento.currentTarget.checked; pintarConfiguracion(); },
    });

    const selectorLimite = h('select', {
      id: 'limite-pregunta',
      onchange: (evento) => { limite = Number(evento.currentTarget.value); },
    }, [
      h('option', { value: '0' }, 'Sin límite (sólo mide el tiempo)'),
      h('option', { value: '30' }, '30 segundos por pregunta'),
      h('option', { value: '45' }, '45 segundos por pregunta'),
      h('option', { value: '60' }, '60 segundos por pregunta'),
    ]);
    selectorLimite.value = String(limite);

    contenedor.append(
      h('div', { class: 'cabecera-pagina' }, [
        h('h1', {}, 'Test de prueba'),
        h('p', {}, 'Arma un examen simulado con la extensión, los temas y el ritmo que necesites. Cada pregunta se cronometra por separado.'),
      ]),
      h('section', { class: 'tarjeta-azul', style: 'margin-bottom:24px' }, [
        h('h2', { style: 'margin-bottom:8px' }, `${cantidad} preguntas · máximo ${maxErr} ${maxErr === 1 ? 'error' : 'errores'}`),
        h('p', { style: 'margin:0' },
          'El examen oficial de la Licencia Clase B tiene 35 preguntas y permite un máximo de 2 respuestas erróneas. Ese mismo criterio se aplica proporcionalmente en los tests más cortos.'),
      ]),
      h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
        h('h2', {}, 'Cantidad de preguntas'), chipsCantidad,
      ]),
      h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
        h('h2', {}, 'Temas del manual'),
        h('div', { class: 'grupo-botones', style: 'margin-bottom:8px' }, [
          h('button', {
            type: 'button', class: 'boton boton-texto',
            onclick: () => { capitulos = datos.capitulos.map((c) => c.id); pintarConfiguracion(); },
          }, 'Seleccionar todos'),
          h('button', {
            type: 'button', class: 'boton boton-texto',
            onclick: () => { capitulos = [datos.capitulos[0].id]; pintarConfiguracion(); },
          }, 'Dejar sólo el primero'),
        ]),
        casillasCapitulos,
        h('p', { style: 'color:var(--gris-medio);margin:8px 0 0' },
          `Preguntas disponibles con esta selección: ${bancoDisponible}.`),
      ]),
      h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
        h('h2', {}, 'Señalética'),
        h('div', { class: 'opcion-caja' }, [
          casillaSenales,
          h('label', { for: 'incluir-senales' }, 'Incluir preguntas de señalética (aproximadamente un cuarto del test)'),
        ]),
      ]),
      h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
        h('h2', {}, 'Ritmo'),
        h('div', { class: 'campo', style: 'max-width:420px;margin:0' }, [
          h('label', { for: 'limite-pregunta' }, 'Tiempo máximo por pregunta'),
          selectorLimite,
          h('p', { class: 'ayuda' }, 'Si se agota el tiempo, la pregunta se marca como incorrecta y el test continúa.'),
        ]),
      ]),
      h('div', { class: 'grupo-botones' }, [
        h('button', {
          type: 'button', class: 'boton boton-principal',
          onclick: () => iniciar(),
        }, [icono('test'), `Comenzar el test de ${cantidad} preguntas`]),
        h('a', { href: '/home', 'data-ruta': '', class: 'boton boton-secundario' }, 'Volver al inicio'),
      ]),
    );
  }

  function iniciar() {
    const preguntas = armarTest(datos, { cantidad, capitulos, incluirSenaletica });
    if (!preguntas.length) return;
    vaciar(contenedor);
    ejecutarEjercicio(contenedor, {
      titulo: 'Test de prueba',
      subtitulo: `${preguntas.length} preguntas · máximo ${maximoErrores(preguntas.length)} errores`,
      preguntas,
      tipo: 'test',
      limitePorPregunta: limite,
      alTerminar: (destino, sesion, respuestas) => {
        pintarResumen(destino, sesion, respuestas, { repetir: () => { pintarConfiguracion(); window.scrollTo(0, 0); } });
      },
    });
    window.scrollTo(0, 0);
  }

  pintarConfiguracion();
}

/* ---------------------------------------------------------- /resultados ---- */

export function vistaResultados(raiz) {
  document.title = 'Resultados · Conduce-Fácil';
  const { datos, progreso } = estado;
  const sesiones = progreso.sesiones || [];

  raiz.append(h('div', { class: 'cabecera-pagina' }, [
    h('h1', {}, 'Resultados'),
    h('p', {}, 'Cada test y cada trivia queda registrada con su puntaje, su tiempo y el detalle por pregunta.'),
  ]));

  if (!sesiones.length) {
    raiz.append(h('div', { class: 'estado-vacio' }, [
      h('h3', {}, 'Aún no registras prácticas'),
      h('p', {}, 'Cuando rindas tu primer test o juegues la trivia, aquí verás tu historial completo con tiempos y tasa de acierto.'),
      h('div', { class: 'grupo-botones', style: 'justify-content:center' }, [
        h('a', { href: '/test', 'data-ruta': '', class: 'boton boton-principal' }, 'Rendir un test'),
        h('a', { href: '/trivia', 'data-ruta': '', class: 'boton boton-secundario' }, 'Jugar la trivia'),
      ]),
    ]));
    return;
  }

  const tests = sesiones.filter((s) => s.tipo === 'test');
  const trivias = sesiones.filter((s) => s.tipo === 'trivia');
  const mejor = tests.reduce((a, b) => (!a || porcentaje(b.correctas, b.total) > porcentaje(a.correctas, a.total) ? b : a), null);

  raiz.append(h('section', { class: 'cifras', style: 'margin-bottom:32px' }, [
    h('div', { class: 'cifra' }, [h('div', { class: 'valor' }, String(tests.length)), h('div', { class: 'rotulo' }, 'Tests rendidos')]),
    h('div', { class: 'cifra' }, [h('div', { class: 'valor' }, String(tests.filter((s) => s.aprobado).length)), h('div', { class: 'rotulo' }, 'Tests aprobados')]),
    h('div', { class: 'cifra' }, [h('div', { class: 'valor' }, String(trivias.length)), h('div', { class: 'rotulo' }, 'Trivias jugadas')]),
    h('div', { class: 'cifra' }, [
      h('div', { class: 'valor' }, mejor ? `${porcentaje(mejor.correctas, mejor.total)}%` : '—'),
      h('div', { class: 'rotulo' }, 'Mejor test'),
    ]),
  ]));

  /* Detalle por contenido */
  const filasPreguntas = datos.preguntas
    .map((p) => ({ p, r: progreso.preguntas[p.id] }))
    .filter((x) => x.r)
    .sort((a, b) => porcentaje(a.r.aciertos, a.r.intentos) - porcentaje(b.r.aciertos, b.r.intentos));

  raiz.append(h('h2', {}, 'Historial de prácticas'));
  raiz.append(h('div', { class: 'tabla-envoltorio', style: 'margin-bottom:32px' }, h('table', { class: 'tabla' }, [
    h('thead', {}, h('tr', {}, [
      h('th', {}, 'Fecha'), h('th', {}, 'Tipo'), h('th', { class: 'num' }, 'Resultado'),
      h('th', { class: 'num' }, 'Aciertos'), h('th', { class: 'num' }, 'Tiempo'),
      h('th', { class: 'num' }, 'Por pregunta'), h('th', {}, 'Estado'),
    ])),
    h('tbody', {}, sesiones.slice(0, 60).map((s) => h('tr', {}, [
      h('td', {}, formatearFecha(s.fecha)),
      h('td', {}, s.tipo === 'test' ? 'Test' : 'Trivia'),
      h('td', { class: 'num' }, `${s.correctas}/${s.total}`),
      h('td', { class: 'num' }, `${porcentaje(s.correctas, s.total)}%`),
      h('td', { class: 'num' }, formatearDuracion(s.duracion)),
      h('td', { class: 'num' }, formatearDuracion(s.duracion / Math.max(1, s.total))),
      h('td', {}, h('span', { class: `etiqueta ${s.aprobado ? 'etiqueta-exito' : 'etiqueta-error'}` },
        s.aprobado ? 'Aprobado' : 'Reprobado')),
    ]))),
  ])));

  if (filasPreguntas.length) {
    raiz.append(h('h2', {}, 'Rendimiento por pregunta'));
    raiz.append(h('p', { style: 'color:var(--gris-medio)' },
      'Ordenado de menor a mayor tasa de acierto: arriba están las preguntas que más te conviene repasar.'));
    raiz.append(h('div', { class: 'tabla-envoltorio', style: 'margin-bottom:32px' }, h('table', { class: 'tabla' }, [
      h('thead', {}, h('tr', {}, [
        h('th', {}, 'Pregunta'), h('th', { class: 'num' }, 'Veces'),
        h('th', { class: 'num' }, 'Aciertos'), h('th', { class: 'num' }, 'Tiempo medio'), h('th', {}, 'Página'),
      ])),
      h('tbody', {}, filasPreguntas.slice(0, 40).map(({ p, r }) => h('tr', {}, [
        h('td', {}, p.enunciado),
        h('td', { class: 'num' }, String(r.intentos)),
        h('td', { class: 'num' }, `${porcentaje(r.aciertos, r.intentos)}%`),
        h('td', { class: 'num' }, formatearDuracion(r.tiempo / r.intentos)),
        h('td', {}, String(p.pagina)),
      ]))),
    ])));
  }

  const filasSenales = datos.senales
    .map((s) => ({ s, r: progreso.senales[s.codigo] }))
    .filter((x) => x.r)
    .sort((a, b) => porcentaje(a.r.aciertos, a.r.intentos) - porcentaje(b.r.aciertos, b.r.intentos));

  if (filasSenales.length) {
    raiz.append(h('h2', {}, 'Rendimiento por señal'));
    raiz.append(h('div', { class: 'tabla-envoltorio' }, h('table', { class: 'tabla' }, [
      h('thead', {}, h('tr', {}, [
        h('th', {}, 'Señal'), h('th', {}, 'Nombre'), h('th', {}, 'Familia'),
        h('th', { class: 'num' }, 'Veces'), h('th', { class: 'num' }, 'Aciertos'), h('th', { class: 'num' }, 'Tiempo medio'),
      ])),
      h('tbody', {}, filasSenales.slice(0, 40).map(({ s, r }) => h('tr', {}, [
        h('td', {}, h('img', { src: `/assets/senales/${s.archivo}`, alt: s.nombre, loading: 'lazy', style: 'height:44px;width:auto' })),
        h('td', {}, [h('strong', {}, s.nombre), h('div', { style: 'font-size:12px;color:var(--gris-medio)' }, s.codigo)]),
        h('td', {}, s.grupo),
        h('td', { class: 'num' }, String(r.intentos)),
        h('td', { class: 'num' }, `${porcentaje(r.aciertos, r.intentos)}%`),
        h('td', { class: 'num' }, formatearDuracion(r.tiempo / r.intentos)),
      ]))),
    ])));
  }
}
