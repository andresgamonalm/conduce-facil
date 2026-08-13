/* Conduce-Fácil · Home, Estudio y Repaso. */

import {
  formatearDuracion, formatearFecha, h, icono, navegar, porcentaje,
} from './nucleo_conduce_facil.js';
import { estado, guardarProgreso } from './contexto_conduce_facil.js';
import { registrarTarjeta } from './almacenamiento_conduce_facil.js';
import {
  capitulo as buscarCapitulo, desempenoPorCapitulo, desempenoPorGrupoSenales,
  puntosDebiles, resumenGeneral, seccionesDe,
} from './datos_conduce_facil.js';


/* ---------------------------------------------------------------- /home ---- */

export function vistaHome(raiz) {
  document.title = 'Inicio · Conduce-Fácil';
  const { datos, progreso, usuario } = estado;
  const resumen = resumenGeneral(datos, progreso);
  const capitulos = desempenoPorCapitulo(datos, progreso);
  const pendiente = capitulos.find((c) => c.avanceEstudio < 100) || capitulos[0];
  const ultimaSesion = progreso.sesiones[0];

  raiz.append(h('section', { class: 'portada-home' }, [
    h('div', {}, [
      h('p', { style: 'font-size:15px;margin-bottom:8px;color:var(--amarillo)' },
        `Hola, ${usuario.nombre || usuario.usuario}`),
      h('h1', {}, 'Rinde el examen teórico con margen de sobra'),
      h('p', {}, 'El examen tiene 35 preguntas y admite un máximo de 2 respuestas erróneas. Practica hasta que ese margen te sobre.'),
      h('div', { class: 'grupo-botones' }, [
        h('a', {
          href: '/test', 'data-ruta': '', class: 'boton boton-amarillo',
        }, [icono('test'), 'Lanzar un test de 35 preguntas']),
        h('a', {
          href: '/estudio', 'data-ruta': '', class: 'boton boton-secundario',
        }, [icono('estudio'), 'Continuar el estudio']),
      ]),
      h('div', { style: 'margin-top:28px' }, [
        h('div', { style: 'display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px' }, [
          h('span', {}, 'Avance del estudio'),
          h('strong', {}, `${resumen.avanceEstudio}%`),
        ]),
        h('div', { class: 'barra-progreso sobre-azul' }, h('span', { style: `width:${resumen.avanceEstudio}%` })),
      ]),
    ]),
    /* Ilustración decorativa: se pinta como fondo desde la hoja de estilos y
       sólo en la composición de dos columnas. En móvil no se descarga. */
    h('figure', {
      class: 'portada-figura', style: 'margin:0', role: 'img',
      'aria-label': 'Ilustración de un cruce urbano con vehículos, semáforos y una ambulancia',
    }),
  ]));

  raiz.append(h('section', { class: 'cifras', style: 'margin-bottom:32px' }, [
    tarjetaCifra(String(resumen.tests), 'Tests rendidos'),
    tarjetaCifra(`${resumen.exito}%`, 'Aciertos acumulados'),
    tarjetaCifra(`${resumen.dominadas}/${resumen.totalTarjetas}`, 'Contenidos dominados'),
    tarjetaCifra(String(resumen.aprobados), 'Tests aprobados'),
  ]));

  raiz.append(h('h2', {}, 'Dónde practicar'));
  raiz.append(h('div', { class: 'rejilla rejilla-2', style: 'margin-bottom:32px' }, [
    tarjetaModulo('estudio', 'icono-azul', 'Estudio',
      `${datos.tarjetas.length} contenidos del Manual CONASET en formato pregunta y respuesta, con las imágenes del propio manual.`,
      '/estudio', 'Ir al estudio'),
    tarjetaModulo('trivia', 'icono-turquesa', 'Trivia de señalética',
      `${datos.senales.length} señaléticas oficiales del Manual de Señalización: reconoce la señal entre cuatro alternativas.`,
      '/trivia', 'Jugar la trivia'),
    tarjetaModulo('test', 'icono-magenta', 'Test de prueba',
      'Simula el examen: elige la cantidad de preguntas, los capítulos y si quieres incluir señalética. Con cronómetro por pregunta.',
      '/test', 'Configurar un test'),
    tarjetaModulo('repaso', 'icono-secundario', 'Repaso',
      'El sistema detecta tus capítulos y señales más débiles y arma la práctica que te conviene.',
      '/repaso', 'Ver mi repaso'),
  ]));

  if (pendiente) {
    raiz.append(h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
      h('h3', {}, 'Continúa por aquí'),
      h('p', { style: 'color:var(--gris-medio)' },
        `Capítulo ${pendiente.numero}: ${pendiente.titulo} — ${pendiente.dominadas} de ${pendiente.tarjetas} contenidos dominados.`),
      h('a', { href: `/estudio/${pendiente.id}`, 'data-ruta': '', class: 'boton boton-principal' },
        [icono('flecha'), `Seguir con ${pendiente.titulo}`]),
    ]));
  }

  if (ultimaSesion) {
    raiz.append(h('section', { class: 'tarjeta' }, [
      h('h3', {}, 'Tu última práctica'),
      h('p', { style: 'color:var(--gris-medio)' }, [
        `${ultimaSesion.tipo === 'test' ? 'Test' : 'Trivia'} del ${formatearFecha(ultimaSesion.fecha)}: `,
        h('strong', {}, `${ultimaSesion.correctas} de ${ultimaSesion.total} correctas`),
        ` en ${formatearDuracion(ultimaSesion.duracion)}.`,
      ]),
      h('a', { href: '/resultados', 'data-ruta': '', class: 'boton boton-secundario' }, 'Ver todos mis resultados'),
    ]));
  }
}

function tarjetaCifra(valor, rotulo) {
  return h('div', { class: 'cifra' }, [
    h('div', { class: 'valor' }, valor),
    h('div', { class: 'rotulo' }, rotulo),
  ]);
}

function tarjetaModulo(nombreIcono, claseIcono, titulo, descripcion, ruta, cta) {
  return h('a', { href: ruta, 'data-ruta': '', class: 'tarjeta enlace-tarjeta' }, [
    h('div', { class: 'modulo-acceso' }, [
      h('div', { class: `modulo-icono ${claseIcono}` }, icono(nombreIcono)),
      h('div', {}, [
        h('h3', { style: 'margin-bottom:6px' }, titulo),
        h('p', { style: 'color:var(--gris-medio);margin-bottom:12px' }, descripcion),
        h('span', { class: 'boton boton-texto', style: 'padding:0' }, [cta, icono('flecha')]),
      ]),
    ]),
  ]);
}

/* ------------------------------------------------------------- /estudio ---- */

export function vistaEstudio(raiz) {
  document.title = 'Estudio · Conduce-Fácil';
  const { datos, progreso } = estado;
  const capitulos = desempenoPorCapitulo(datos, progreso);

  raiz.append(h('div', { class: 'cabecera-pagina' }, [
    h('h1', {}, 'Estudio'),
    h('p', {}, [
      'Todo el contenido del ', h('strong', {}, datos.fuenteEstudio),
      ', dividido en preguntas y respuestas. Las respuestas son el texto literal del manual y se acompañan con sus imágenes originales.',
    ]),
  ]));

  raiz.append(h('div', { class: 'rejilla rejilla-2' }, capitulos.map((cap) => h('a', {
    href: `/estudio/${cap.id}`, 'data-ruta': '', class: 'tarjeta enlace-tarjeta',
  }, [
    h('div', { style: 'display:flex;align-items:baseline;gap:10px;margin-bottom:6px' }, [
      h('span', { class: 'etiqueta etiqueta-neutra' }, cap.id.startsWith('anexo') ? 'Anexo' : `Capítulo ${cap.numero}`),
      h('span', { style: 'font-size:13px;color:var(--gris-medio)' }, `Páginas ${cap.paginas}`),
    ]),
    h('h3', { style: 'margin-bottom:8px' }, cap.titulo),
    h('p', { style: 'color:var(--gris-medio);margin-bottom:12px' },
      `${cap.tarjetas} contenidos · ${cap.dominadas} dominados`),
    h('div', { class: 'barra-progreso' }, h('span', { style: `width:${cap.avanceEstudio}%` })),
  ]))));
}

/* --------------------------------------------------- /estudio/:capitulo ---- */

export function vistaCapitulo(raiz, { capitulo: idCapitulo }) {
  const { datos, progreso } = estado;
  const cap = buscarCapitulo(datos, idCapitulo);
  if (!cap) { navegar('/estudio', true); return; }
  document.title = `${cap.titulo} · Conduce-Fácil`;

  const contadorAvance = h('strong', {});

  function actualizarAvance() {
    const dominadas = cap.tarjetas.filter((t) => progreso.estudio[t.id]?.dominada).length;
    contadorAvance.textContent = `${dominadas} de ${cap.tarjetas.length} dominados (${porcentaje(dominadas, cap.tarjetas.length)}%)`;
    barra.style.width = `${porcentaje(dominadas, cap.tarjetas.length)}%`;
  }

  const barra = h('span', { style: 'width:0%' });

  raiz.append(h('div', { class: 'migas' }, [
    h('a', { href: '/estudio', 'data-ruta': '' }, 'Estudio'), ' › ', cap.titulo,
  ]));
  raiz.append(h('div', { class: 'cabecera-pagina' }, [
    h('h1', {}, cap.titulo),
    h('p', {}, `Páginas ${cap.paginas} del Manual CONASET · ${cap.tarjetas.length} contenidos · ${cap.preguntas.length} preguntas de test disponibles`),
    h('div', { style: 'margin-top:16px;max-width:420px' }, [
      h('div', { style: 'display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px' }, [
        h('span', {}, 'Tu avance en este capítulo'), contadorAvance,
      ]),
      h('div', { class: 'barra-progreso' }, barra),
    ]),
  ]));

  raiz.append(h('div', { class: 'grupo-botones', style: 'margin-bottom:32px' }, [
    h('button', {
      type: 'button', class: 'boton boton-secundario',
      onclick: () => raiz.querySelectorAll('details.tarjeta-estudio').forEach((d) => { d.open = true; }),
    }, 'Abrir todas las respuestas'),
    h('button', {
      type: 'button', class: 'boton boton-secundario',
      onclick: () => raiz.querySelectorAll('details.tarjeta-estudio').forEach((d) => { d.open = false; }),
    }, 'Cerrar todas'),
    cap.preguntas.length ? h('a', {
      href: `/test?capitulo=${cap.id}`, 'data-ruta': '', class: 'boton boton-principal',
    }, [icono('test'), 'Rendir un test de este capítulo']) : null,
  ]));

  for (const seccion of seccionesDe(cap)) {
    raiz.append(h('h2', { style: 'margin-top:32px' }, seccion.nombre));
    for (const tarjeta of seccion.tarjetas) {
      raiz.append(tarjetaContenido(tarjeta, actualizarAvance));
    }
  }

  actualizarAvance();
}

function tarjetaContenido(tarjeta, alCambiar) {
  const registro = estado.progreso.estudio[tarjeta.id];
  const marcaDominio = h('span', {
    class: `etiqueta ${registro?.dominada ? 'etiqueta-exito' : 'etiqueta-neutra'}`,
  }, registro?.dominada ? 'Dominado' : 'Por repasar');

  function marcar(dominada) {
    registrarTarjeta(estado.progreso, tarjeta.id, dominada);
    guardarProgreso();
    marcaDominio.className = `etiqueta ${dominada ? 'etiqueta-exito' : 'etiqueta-alerta'}`;
    marcaDominio.textContent = dominada ? 'Dominado' : 'Para repasar';
    alCambiar();
  }

  const figuras = (tarjeta.figuras || []).length
    ? h('div', { class: 'figuras-manual' }, tarjeta.figuras.map((archivo) => h('figure', {}, [
      h('img', {
        src: `/assets/manual/${archivo}`, loading: 'lazy',
        alt: `Imagen del Manual CONASET, página ${tarjeta.pagina}`,
      }),
    ])))
    : null;

  return h('details', { class: 'tarjeta-estudio' }, [
    h('summary', { style: 'cursor:pointer;list-style:none' }, [
      h('div', { style: 'display:flex;gap:12px;align-items:flex-start;justify-content:space-between' }, [
        h('span', { class: 'pregunta', style: 'margin:0' }, tarjeta.pregunta),
        marcaDominio,
      ]),
    ]),
    h('div', { style: 'padding-top:16px' }, [
      h('div', { class: 'respuesta' }, [
        h('p', {}, tarjeta.respuesta),
        h('p', { class: 'cita' }, `Texto literal del Manual CONASET, página ${tarjeta.pagina}.`),
      ]),
      figuras,
      h('div', { class: 'acciones-estudio' }, [
        h('span', { style: 'font-size:14px;color:var(--gris-medio)' }, '¿Te quedó claro?'),
        h('button', { type: 'button', class: 'boton boton-turquesa', onclick: () => marcar(true) }, 'Sí, lo domino'),
        h('button', { type: 'button', class: 'boton boton-secundario', onclick: () => marcar(false) }, 'Necesito repasarlo'),
      ]),
    ]),
  ]);
}

/* -------------------------------------------------------------- /repaso ---- */

export function vistaRepaso(raiz) {
  document.title = 'Repaso · Conduce-Fácil';
  const { datos, progreso } = estado;
  const capitulos = desempenoPorCapitulo(datos, progreso).filter((c) => c.intentos > 0);
  const gruposSenales = desempenoPorGrupoSenales(datos, progreso).filter((g) => g.intentos > 0);
  const debiles = puntosDebiles(datos, progreso);

  raiz.append(h('div', { class: 'cabecera-pagina' }, [
    h('h1', {}, 'Repaso'),
    h('p', {}, 'A partir de tus resultados, esto es lo que conviene reforzar antes de rendir el examen.'),
  ]));

  if (!capitulos.length && !gruposSenales.length) {
    raiz.append(h('div', { class: 'estado-vacio' }, [
      h('h3', {}, 'Todavía no hay datos suficientes'),
      h('p', {}, 'Rinde un test o juega una trivia de señalética y aquí aparecerán los capítulos y las señales que más te conviene repasar.'),
      h('div', { class: 'grupo-botones', style: 'justify-content:center' }, [
        h('a', { href: '/test', 'data-ruta': '', class: 'boton boton-principal' }, 'Rendir un test'),
        h('a', { href: '/trivia', 'data-ruta': '', class: 'boton boton-secundario' }, 'Jugar la trivia'),
      ]),
    ]));
    return;
  }

  const ordenados = capitulos.slice().sort((a, b) => a.exito - b.exito);
  const criticos = ordenados.filter((c) => c.exito < 80);

  raiz.append(h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
    h('h2', {}, 'Capítulos que debes repasar'),
    criticos.length
      ? h('p', { style: 'color:var(--gris-medio)' },
        `Tienes menos de 80% de aciertos en ${criticos.length} ${criticos.length === 1 ? 'capítulo' : 'capítulos'}. Empieza por el primero de la lista.`)
      : h('div', { class: 'aviso aviso-exito' }, 'Superas el 80% de aciertos en todos los capítulos que has practicado. Mantén el ritmo con tests completos.'),
    h('div', { class: 'lista-debilidades' }, ordenados.map((cap) => h('div', { class: 'fila-debilidad' }, [
      h('div', {}, [
        h('strong', {}, cap.titulo),
        h('div', { style: 'font-size:13px;color:var(--gris-medio)' },
          `${cap.aciertos} de ${cap.intentos} respuestas correctas · ${cap.dominadas}/${cap.tarjetas} contenidos dominados`),
      ]),
      h('div', {}, [
        h('div', { style: 'display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px' }, [
          h('span', {}, 'Aciertos'), h('strong', {}, `${cap.exito}%`),
        ]),
        h('div', { class: 'barra-progreso' }, h('span', { style: `width:${cap.exito}%` })),
      ]),
      h('div', { class: 'grupo-botones' }, [
        h('a', { href: `/estudio/${cap.id}`, 'data-ruta': '', class: 'boton boton-secundario' }, 'Estudiar'),
        h('a', { href: `/test?capitulo=${cap.id}`, 'data-ruta': '', class: 'boton boton-principal' }, 'Practicar'),
      ]),
    ]))),
  ]));

  if (gruposSenales.length) {
    raiz.append(h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
      h('h2', {}, 'Señalética por familia'),
      h('div', { class: 'lista-debilidades' }, gruposSenales.slice().sort((a, b) => a.exito - b.exito)
        .map((g) => h('div', { class: 'fila-debilidad' }, [
          h('div', {}, [
            h('strong', {}, g.grupo),
            h('div', { style: 'font-size:13px;color:var(--gris-medio)' },
              `${g.aciertos} de ${g.intentos} correctas · ${g.total} señales en el catálogo`),
          ]),
          h('div', {}, [
            h('div', { style: 'display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px' }, [
              h('span', {}, 'Aciertos'), h('strong', {}, `${g.exito}%`),
            ]),
            h('div', { class: 'barra-progreso' }, h('span', { style: `width:${g.exito}%` })),
          ]),
          h('div', {}, h('a', {
            href: `/trivia?grupo=${encodeURIComponent(g.grupo)}`, 'data-ruta': '', class: 'boton boton-turquesa',
          }, 'Practicar')),
        ]))),
    ]));
  }

  if (debiles.senales.length) {
    raiz.append(h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
      h('h2', {}, 'Señales que más se te resisten'),
      h('div', { style: 'display:flex;flex-wrap:wrap;gap:16px' }, debiles.senales.map(({ senal, exito, registro }) => h('figure', {
        style: 'margin:0;width:150px;background:var(--gris-claro);border-radius:8px;padding:12px;text-align:center',
      }, [
        h('img', {
          src: `/assets/senales/${senal.archivo}`, loading: 'lazy', alt: senal.nombre,
          style: 'max-height:88px;width:auto',
        }),
        h('figcaption', { style: 'font-size:13px;margin-top:8px' }, [
          h('strong', { style: 'display:block;color:var(--azul)' }, senal.nombre),
          h('span', { style: 'color:var(--gris-medio)' }, `${exito}% en ${registro.intentos} intentos`),
        ]),
      ]))),
    ]));
  }

  if (debiles.preguntas.length) {
    raiz.append(h('section', { class: 'tarjeta' }, [
      h('h2', {}, 'Preguntas con más fallos'),
      h('div', { class: 'lista-debilidades' }, debiles.preguntas.map(({ pregunta, exito, registro }) => h('details', {
        class: 'tarjeta-plana',
      }, [
        h('summary', { style: 'cursor:pointer;list-style:none;display:flex;gap:12px;justify-content:space-between;align-items:flex-start' }, [
          h('span', { style: 'font-weight:500;color:var(--azul)' }, pregunta.enunciado),
          h('span', { class: 'etiqueta etiqueta-error' }, `${exito}%`),
        ]),
        h('div', { style: 'padding-top:12px' }, [
          h('p', { style: 'margin-bottom:8px' }, [
            h('strong', {}, 'Respuesta correcta: '), pregunta.opciones[pregunta.correcta],
          ]),
          h('div', { class: 'tarjeta-turquesa' }, [
            h('p', { style: 'margin:0' }, pregunta.fundamento),
            h('p', { class: 'cita', style: 'margin:8px 0 0' }, `Manual CONASET, página ${pregunta.pagina} · ${registro.intentos} intentos`),
          ]),
        ]),
      ]))),
    ]));
  }
}
