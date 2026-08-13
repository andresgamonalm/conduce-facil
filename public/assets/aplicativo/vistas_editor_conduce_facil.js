/* Conduce-Fácil · Editor de contenidos.
   Permite a la persona administradora corregir el material de estudio y las
   preguntas del test desde el propio aplicativo. Lo editado se guarda aparte
   del texto publicado, de modo que restaurar el original siempre es posible, y
   se aplica de inmediato para todas las personas. */

import { h, icono, idAleatorio, vaciar } from './nucleo_conduce_facil.js';
import { estado } from './contexto_conduce_facil.js';
import { reagrupar } from './datos_conduce_facil.js';

const POR_PAGINA = 25;

function esPregunta(elemento) {
  return typeof elemento.enunciado === 'string';
}

function tituloDe(elemento) {
  return esPregunta(elemento) ? elemento.enunciado : elemento.pregunta;
}

function cuerpoDe(elemento) {
  return esPregunta(elemento) ? elemento.fundamento : elemento.respuesta;
}

function normalizar(texto) {
  return String(texto || '').toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '');
}

export function vistaEditor(raiz) {
  document.title = 'Editor de contenidos · Conduce-Fácil';
  const { datos } = estado;

  if (!estado.usuario || estado.usuario.rol !== 'admin') {
    raiz.append(h('div', { class: 'aviso aviso-error' },
      'Esta sección es sólo para la cuenta de administración.'));
    return;
  }

  let tipo = 'estudio';
  let capitulo = 'todos';
  let busqueda = '';
  let pagina = 0;
  let verEliminados = false;

  const lista = h('div', { class: 'lista-edicion' });
  const resumenLista = h('p', { style: 'color:var(--gris-medio);margin:0 0 16px' });
  const paginador = h('div', { class: 'grupo-botones', style: 'margin-top:24px' });

  /* Contenidos quitados: se guardan aparte para poder recuperarlos. */
  const eliminados = (datos.eliminados || []).slice();

  function universo() {
    if (verEliminados) return eliminados.filter((e) => esPregunta(e) === (tipo === 'pregunta'));
    return tipo === 'estudio' ? datos.tarjetas : datos.preguntas;
  }

  function coleccion(elemento) {
    return esPregunta(elemento) ? datos.preguntas : datos.tarjetas;
  }

  function quitarDelMaterial(elemento) {
    const lista = coleccion(elemento);
    const i = lista.indexOf(elemento);
    if (i >= 0) lista.splice(i, 1);
    if (!eliminados.includes(elemento)) eliminados.push(elemento);
    reagrupar(datos);
  }

  function devolverAlMaterial(elemento) {
    const i = eliminados.indexOf(elemento);
    if (i >= 0) eliminados.splice(i, 1);
    delete elemento.eliminado;
    coleccion(elemento).push(elemento);
    reagrupar(datos);
  }

  function filtrados() {
    const q = normalizar(busqueda);
    return universo().filter((el) => {
      if (capitulo !== 'todos' && el.capitulo !== capitulo) return false;
      if (!q) return true;
      return normalizar(`${el.id} ${tituloDe(el)} ${cuerpoDe(el)}`).includes(q);
    });
  }

  /* ------------------------------------------------------- Ficha editable -- */

  function ficha(elemento) {
    const pregunta = esPregunta(elemento);
    const aviso = h('div', { class: 'aviso oculto', role: 'status', style: 'margin:12px 0 0' });

    const campoTitulo = h('textarea', { rows: '2', id: `t-${elemento.id}` }, tituloDe(elemento));
    const campoCuerpo = h('textarea', { rows: '7', id: `c-${elemento.id}` }, cuerpoDe(elemento));
    const contador = h('span', { class: 'contador-texto' });

    function actualizarContador() {
      const n = campoCuerpo.value.length;
      contador.textContent = `${n} caracteres`;
      contador.className = `contador-texto${n > 700 ? ' largo' : ''}`;
    }
    campoCuerpo.addEventListener('input', actualizarContador);
    actualizarContador();

    /* Alternativas, sólo en las preguntas del test. */
    const alternativas = [];
    let bloqueAlternativas = null;
    if (pregunta) {
      const grupo = h('div', { class: 'opciones-edicion' });
      elemento.opciones.forEach((texto, i) => {
        const radio = h('input', {
          type: 'radio', name: `correcta-${elemento.id}`, value: String(i),
          checked: i === elemento.correcta, 'aria-label': `Marcar la alternativa ${i + 1} como correcta`,
        });
        const campo = h('input', { type: 'text', value: texto, 'aria-label': `Alternativa ${i + 1}` });
        alternativas.push({ radio, campo });
        grupo.append(h('div', { class: 'opcion-edicion' }, [radio, campo]));
      });
      bloqueAlternativas = h('div', { class: 'campo' }, [
        h('label', {}, 'Alternativas · marca la correcta'),
        grupo,
      ]);
    }

    async function guardar(boton) {
      boton.disabled = true;
      const textoPrevio = boton.textContent;
      boton.textContent = 'Guardando…';

      const cambios = pregunta
        ? {
          enunciado: campoTitulo.value.trim(),
          fundamento: campoCuerpo.value.trim(),
          opciones: alternativas.map((a) => a.campo.value.trim()),
          correcta: alternativas.findIndex((a) => a.radio.checked),
        }
        : { pregunta: campoTitulo.value.trim(), respuesta: campoCuerpo.value.trim() };

      if (!cambios[pregunta ? 'enunciado' : 'pregunta']) {
        mostrar(aviso, 'error', 'La pregunta no puede quedar vacía.');
        boton.disabled = false; boton.textContent = textoPrevio;
        return;
      }
      if (pregunta) {
        if (cambios.opciones.some((o) => !o)) {
          mostrar(aviso, 'error', 'Ninguna alternativa puede quedar vacía.');
          boton.disabled = false; boton.textContent = textoPrevio;
          return;
        }
        if (cambios.correcta < 0) {
          mostrar(aviso, 'error', 'Marca cuál es la alternativa correcta.');
          boton.disabled = false; boton.textContent = textoPrevio;
          return;
        }
      }

      /* En los contenidos creados aquí hay que conservar lo que los define
         como propios; si no, al recargar dejarían de reconocerse y
         desaparecerían. */
      const carga = elemento.nuevo
        ? { nuevo: true, capitulo: elemento.capitulo, ...cambios }
        : cambios;

      const resultado = await estado.repo.guardarContenido(
        elemento.id, pregunta ? 'pregunta' : 'estudio', carga,
      );

      if (!resultado || !resultado.ok) {
        mostrar(aviso, 'error', (resultado && resultado.error) || 'No se pudo guardar.');
        boton.disabled = false; boton.textContent = textoPrevio;
        return;
      }

      /* Se refleja en memoria para que el cambio se note al instante en el
         resto del aplicativo, sin recargar. */
      if (!elemento.original) {
        elemento.original = {};
        for (const clave of Object.keys(cambios)) elemento.original[clave] = elemento[clave];
      }
      Object.assign(elemento, cambios);
      elemento.editado = true;
      mostrar(aviso, 'exito', 'Guardado. Ya está aplicado en el aplicativo.');
      boton.disabled = false; boton.textContent = textoPrevio;
      reflejar();
      actualizarResumen();
    }

    async function restaurar(boton) {
      boton.disabled = true;
      const resultado = await estado.repo.restaurarContenido(elemento.id);
      if (!resultado || !resultado.ok) {
        mostrar(aviso, 'error', (resultado && resultado.error) || 'No se pudo restaurar.');
        boton.disabled = false;
        return;
      }
      if (elemento.original) Object.assign(elemento, elemento.original);
      delete elemento.original;
      delete elemento.editado;
      campoTitulo.value = tituloDe(elemento);
      campoCuerpo.value = cuerpoDe(elemento);
      if (pregunta) {
        alternativas.forEach((a, i) => {
          a.campo.value = elemento.opciones[i];
          a.radio.checked = i === elemento.correcta;
        });
      }
      boton.disabled = false;
      mostrar(aviso, 'info', 'Restaurado el texto original del manual.');
      reflejar();
      actualizarResumen();
    }

    const marca = h('span', { class: `etiqueta etiqueta-turquesa${elemento.editado ? '' : ' oculto'}` }, 'Editado');
    const rotuloResumen = h('span', { class: 'resumen-titulo' }, tituloDe(elemento));
    const botonRestaurar = h('button', {
      type: 'button', class: `boton boton-secundario${elemento.editado ? '' : ' oculto'}`,
      onclick: (e) => restaurar(e.currentTarget),
    }, 'Restaurar el original');

    /* La ficha se actualiza en el sitio: repintar la lista cerraría el panel
       abierto y se perdería el mensaje de confirmación. */
    function reflejar() {
      marca.classList.toggle('oculto', !elemento.editado);
      botonRestaurar.classList.toggle('oculto', !elemento.editado);
      rotuloResumen.textContent = tituloDe(elemento);
      actualizarContador();
    }

    /* Eliminar no destruye nada: se marca como quitado y deja de aparecer en
       el aplicativo. Se recupera desde el filtro «Eliminados». */
    async function eliminar(boton) {
      boton.disabled = true;
      const resultado = await estado.repo.guardarContenido(
        elemento.id, pregunta ? 'pregunta' : 'estudio', { eliminado: true },
      );
      if (!resultado || !resultado.ok) {
        mostrar(aviso, 'error', (resultado && resultado.error) || 'No se pudo eliminar.');
        boton.disabled = false;
        return;
      }
      elemento.eliminado = true;
      quitarDelMaterial(elemento);
      ficha.remove();
      actualizarResumen();
    }

    async function recuperar(boton) {
      boton.disabled = true;
      const resultado = await estado.repo.restaurarContenido(elemento.id);
      if (!resultado || !resultado.ok) {
        mostrar(aviso, 'error', (resultado && resultado.error) || 'No se pudo recuperar.');
        boton.disabled = false;
        return;
      }
      devolverAlMaterial(elemento);
      ficha.remove();
      actualizarResumen();
    }

    const acciones = elemento.eliminado
      ? h('div', { class: 'grupo-botones', style: 'margin-top:16px' }, [
        h('button', {
          type: 'button', class: 'boton boton-turquesa',
          onclick: (e) => recuperar(e.currentTarget),
        }, 'Devolver al aplicativo'),
      ])
      : h('div', { class: 'grupo-botones', style: 'margin-top:16px' }, [
        h('button', {
          type: 'button', class: 'boton boton-principal',
          onclick: (e) => guardar(e.currentTarget),
        }, [icono('config'), 'Guardar cambios']),
        botonRestaurar,
        h('button', {
          type: 'button', class: 'boton boton-texto', style: 'color:var(--error-fuerte)',
          onclick: (e) => {
            if (!window.confirm('¿Quitar este contenido del aplicativo? Podrás recuperarlo desde el filtro «Eliminados».')) return;
            eliminar(e.currentTarget);
          },
        }, 'Eliminar'),
      ]);

    const ficha = h('details', { class: 'tarjeta ficha-edicion' }, [
      h('summary', {}, [
        h('span', { class: 'etiqueta etiqueta-neutra' }, elemento.id),
        rotuloResumen,
        marca,
        h('span', { class: 'resumen-pagina' }, elemento.pagina ? `p. ${elemento.pagina}` : 'propio'),
      ]),
      h('div', { class: 'cuerpo-edicion' }, [
        h('div', { class: 'campo' }, [
          h('label', { for: `t-${elemento.id}` }, pregunta ? 'Enunciado' : 'Pregunta'),
          campoTitulo,
        ]),
        bloqueAlternativas,
        h('div', { class: 'campo' }, [
          h('label', { for: `c-${elemento.id}` }, [pregunta ? 'Fundamento' : 'Respuesta', contador]),
          campoCuerpo,
          h('p', { class: 'ayuda' },
            elemento.pagina
              ? `Texto tomado de la página ${elemento.pagina} del manual. Puedes acortarlo o reescribirlo.`
              : 'Contenido añadido por ti; no proviene del manual.'),
        ]),
        acciones,
        aviso,
      ]),
    ]);
    return ficha;
  }

  function mostrar(nodo, clase, texto) {
    nodo.className = `aviso aviso-${clase}`;
    nodo.textContent = texto;
  }

  /* ------------------------------------------------------------- Listado -- */

  function actualizarResumen() {
    const todos = filtrados();
    const editados = todos.filter((e) => e.editado).length;
    const desde = pagina * POR_PAGINA;
    const mostrados = Math.min(POR_PAGINA, todos.length - desde);
    resumenLista.textContent = todos.length
      ? `${todos.length} ${tipo === 'estudio' ? 'contenidos' : 'preguntas'} · ${editados} editado${editados === 1 ? '' : 's'} · mostrando ${desde + 1}-${desde + mostrados}`
      : 'No hay nada que coincida con la búsqueda.';
  }

  function pintarLista() {
    const todos = filtrados();
    const desde = pagina * POR_PAGINA;
    const trozo = todos.slice(desde, desde + POR_PAGINA);
    actualizarResumen();

    vaciar(lista).append(...trozo.map(ficha));

    const paginas = Math.ceil(todos.length / POR_PAGINA);
    vaciar(paginador);
    if (paginas > 1) {
      paginador.append(
        h('button', {
          type: 'button', class: 'boton boton-secundario', disabled: pagina === 0,
          onclick: () => { pagina -= 1; pintarLista(); window.scrollTo(0, 0); },
        }, 'Anteriores'),
        h('span', { style: 'align-self:center;color:var(--gris-medio)' }, `Página ${pagina + 1} de ${paginas}`),
        h('button', {
          type: 'button', class: 'boton boton-secundario', disabled: pagina >= paginas - 1,
          onclick: () => { pagina += 1; pintarLista(); window.scrollTo(0, 0); },
        }, 'Siguientes'),
      );
    }
  }

  /* --------------------------------------------------------- Controles ---- */

  /* --- Añadir un contenido propio --- */
  async function anadir() {
    const destino = capitulo !== 'todos' ? capitulo : datos.capitulos[0].id;
    const id = `propio-${idAleatorio().toLowerCase()}`;
    const campos = tipo === 'pregunta'
      ? {
        capitulo: destino,
        enunciado: 'Escribe aquí la pregunta',
        opciones: ['Alternativa correcta', 'Alternativa 2', 'Alternativa 3', 'Alternativa 4'],
        correcta: 0,
        fundamento: '',
      }
      : { capitulo: destino, pregunta: 'Escribe aquí la pregunta', respuesta: '' };

    const resultado = await estado.repo.guardarContenido(id, tipo === 'pregunta' ? 'pregunta' : 'estudio',
      { nuevo: true, ...campos });
    if (!resultado || !resultado.ok) {
      window.alert((resultado && resultado.error) || 'No se pudo crear el contenido.');
      return;
    }
    const creado = { id, pagina: null, figuras: [], nuevo: true, editado: true, ...campos };
    (tipo === 'pregunta' ? datos.preguntas : datos.tarjetas).unshift(creado);
    reagrupar(datos);
    verEliminados = false;
    busqueda = '';
    campoBusqueda.value = '';
    capitulo = destino;
    selectorCapitulo.value = destino;
    pagina = 0;
    pintarLista();
    const primera = lista.querySelector('.ficha-edicion');
    if (primera) { primera.open = true; primera.scrollIntoView({ block: 'center' }); }
  }

  const chipsTipo = h('div', { class: 'lista-chips' }, [
    ['estudio', `Estudio (${datos.tarjetas.length})`],
    ['pregunta', `Preguntas del test (${datos.preguntas.length})`],
  ].map(([valor, rotulo]) => h('button', {
    type: 'button', class: 'chip', 'aria-pressed': tipo === valor ? 'true' : 'false',
    onclick: (e) => {
      tipo = valor; pagina = 0;
      e.currentTarget.parentElement.querySelectorAll('.chip')
        .forEach((c) => c.setAttribute('aria-pressed', String(c === e.currentTarget)));
      pintarLista();
    },
  }, rotulo)));

  const selectorCapitulo = h('select', {
    id: 'filtro-capitulo',
    onchange: (e) => { capitulo = e.currentTarget.value; pagina = 0; pintarLista(); },
  }, [
    h('option', { value: 'todos' }, 'Todos los capítulos'),
    ...datos.capitulos.map((c) => h('option', { value: c.id }, c.titulo)),
  ]);

  const casillaEliminados = h('input', {
    type: 'checkbox', id: 'ver-eliminados',
    onchange: (e) => { verEliminados = e.currentTarget.checked; pagina = 0; pintarLista(); },
  });

  const campoBusqueda = h('input', {
    type: 'text', id: 'buscar-contenido', placeholder: 'Buscar en preguntas y respuestas…',
    oninput: (e) => { busqueda = e.currentTarget.value; pagina = 0; pintarLista(); },
  });

  raiz.append(
    h('div', { class: 'cabecera-pagina' }, [
      h('h1', {}, 'Editor de contenidos'),
      h('p', {}, 'Corrige el texto de cualquier contenido de estudio o pregunta del test. Los cambios se guardan al instante y quedan aplicados para todas las personas; el original puede recuperarse siempre.'),
    ]),
    h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
      h('div', { style: 'display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between' }, [
        chipsTipo,
        h('button', {
          type: 'button', class: 'boton boton-turquesa', onclick: () => anadir(),
        }, [icono('flecha'), 'Añadir contenido']),
      ]),
      h('div', { class: 'rejilla rejilla-2', style: 'margin-top:16px' }, [
        h('div', { class: 'campo', style: 'margin:0' }, [
          h('label', { for: 'filtro-capitulo' }, 'Capítulo'), selectorCapitulo,
        ]),
        h('div', { class: 'campo', style: 'margin:0' }, [
          h('label', { for: 'buscar-contenido' }, 'Buscar'), campoBusqueda,
        ]),
      ]),
      h('div', { class: 'opcion-caja', style: 'margin-top:8px' }, [
        casillaEliminados,
        h('label', { for: 'ver-eliminados' }, 'Ver los contenidos que quité, para recuperarlos'),
      ]),
    ]),
    resumenLista,
    lista,
    paginador,
  );

  pintarLista();
}
