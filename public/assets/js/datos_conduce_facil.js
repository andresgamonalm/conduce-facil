/* Conduce-Fácil · Carga y consulta de los contenidos oficiales.
   Los tres archivos JSON se generan con herramientas/generar_datos.py a partir
   del Manual CONASET y del Manual de Señalización incluidos en el repositorio. */

import { mezclar, porcentaje } from './nucleo_conduce_facil.js';

const RUTAS = {
  estudio: '/datos/estudio_conduce_facil.json',
  preguntas: '/datos/preguntas_conduce_facil.json',
  senales: '/datos/senales_conduce_facil.json',
};

let cache = null;

export async function cargarDatos() {
  if (cache) return cache;
  const [estudio, preguntas, senales] = await Promise.all(
    Object.values(RUTAS).map(async (ruta) => {
      const respuesta = await fetch(ruta);
      if (!respuesta.ok) throw new Error(`No se pudo cargar ${ruta}`);
      return respuesta.json();
    }),
  );

  const porCapitulo = new Map();
  for (const capitulo of estudio.capitulos) {
    porCapitulo.set(capitulo.id, {
      ...capitulo,
      tarjetas: estudio.tarjetas.filter((t) => t.capitulo === capitulo.id),
      preguntas: preguntas.preguntas.filter((p) => p.capitulo === capitulo.id),
    });
  }

  cache = {
    fuenteEstudio: estudio.fuente,
    fuenteSenales: senales.fuente,
    capitulos: estudio.capitulos,
    tarjetas: estudio.tarjetas,
    preguntas: preguntas.preguntas,
    senales: senales.senales,
    gruposSenales: senales.grupos,
    porCapitulo,
  };
  return cache;
}

export function capitulo(datos, id) {
  return datos.porCapitulo.get(id) || null;
}

export function seccionesDe(capituloDatos) {
  const mapa = new Map();
  for (const tarjeta of capituloDatos.tarjetas) {
    if (!mapa.has(tarjeta.seccion)) mapa.set(tarjeta.seccion, []);
    mapa.get(tarjeta.seccion).push(tarjeta);
  }
  return [...mapa.entries()].map(([nombre, tarjetas]) => ({ nombre, tarjetas }));
}

/* ------------------------------------------------- Armado de ejercicios ---- */

/** Convierte una señal del catálogo en una pregunta de cuatro alternativas.
 *  Los distractores se toman del mismo grupo para que el ejercicio sea exigente. */
export function preguntaDeSenal(senal, catalogo) {
  const mismoGrupo = catalogo.filter(
    (s) => s.grupo === senal.grupo && s.codigo !== senal.codigo && s.nombre !== senal.nombre,
  );
  const otros = catalogo.filter((s) => s.codigo !== senal.codigo && s.nombre !== senal.nombre);
  const candidatos = mismoGrupo.length >= 3 ? mismoGrupo : otros;
  const vistos = new Set([senal.nombre]);
  const distractores = [];
  for (const opcion of mezclar(candidatos)) {
    if (vistos.has(opcion.nombre)) continue;
    vistos.add(opcion.nombre);
    distractores.push(opcion.nombre);
    if (distractores.length === 3) break;
  }
  const opciones = mezclar([senal.nombre, ...distractores]);
  return {
    tipo: 'senal',
    id: `senal-${senal.codigo}`,
    codigo: senal.codigo,
    imagen: `/assets/senales/${senal.archivo}`,
    grupo: senal.grupo,
    fuente: senal.fuente,
    pagina: senal.pagina,
    enunciado: '¿Qué señal es la que aparece en la imagen?',
    opciones,
    correcta: opciones.indexOf(senal.nombre),
  };
}

export function preguntaDeTest(pregunta) {
  const orden = mezclar(pregunta.opciones.map((texto, indice) => ({ texto, indice })));
  return {
    tipo: 'texto',
    id: pregunta.id,
    capitulo: pregunta.capitulo,
    enunciado: pregunta.enunciado,
    opciones: orden.map((o) => o.texto),
    correcta: orden.findIndex((o) => o.indice === pregunta.correcta),
    fundamento: pregunta.fundamento,
    pagina: pregunta.pagina,
    /* Dibujo con que el manual plantea el caso: el examen teórico lo incorpora,
       de modo que la pregunta debe mostrarse con la misma ilustración. */
    figuras: (pregunta.figuras || []).map((archivo) => `/assets/manual/${archivo}`),
  };
}

/** Construye un test respetando la cantidad, los capítulos y la señalética. */
export function armarTest(datos, opciones) {
  const {
    cantidad = 35,
    capitulos = [],
    incluirSenaletica = true,
    proporcionSenaletica = 0.25,
    grupoSenales = 'todos',
  } = opciones;

  const capitulosElegidos = capitulos.length ? capitulos : datos.capitulos.map((c) => c.id);
  const banco = datos.preguntas.filter((p) => capitulosElegidos.includes(p.capitulo));

  let cupoSenales = incluirSenaletica ? Math.round(cantidad * proporcionSenaletica) : 0;
  const catalogo = grupoSenales === 'todos'
    ? datos.senales
    : datos.senales.filter((s) => s.grupo === grupoSenales);
  cupoSenales = Math.min(cupoSenales, catalogo.length);

  const cupoTexto = Math.min(cantidad - cupoSenales, banco.length);
  const faltan = cantidad - cupoTexto - cupoSenales;
  if (faltan > 0 && catalogo.length) cupoSenales = Math.min(cupoSenales + faltan, catalogo.length);

  const preguntasTexto = mezclar(banco).slice(0, cupoTexto).map(preguntaDeTest);
  const preguntasSenales = mezclar(catalogo).slice(0, cupoSenales).map((s) => preguntaDeSenal(s, datos.senales));
  return mezclar([...preguntasTexto, ...preguntasSenales]);
}

export function armarTrivia(datos, { cantidad = 20, grupo = 'todos' } = {}) {
  const catalogo = grupo === 'todos' ? datos.senales : datos.senales.filter((s) => s.grupo === grupo);
  return mezclar(catalogo).slice(0, Math.min(cantidad, catalogo.length))
    .map((s) => preguntaDeSenal(s, datos.senales));
}

/** Máximo de errores tolerados: 2 en un examen de 35 preguntas, proporcional
 *  en los ejercicios de otra extensión, siempre con un mínimo de 1. */
export function maximoErrores(cantidad) {
  return Math.max(1, Math.round((cantidad * 2) / 35));
}

/* ---------------------------------------------------------- Diagnóstico ---- */

export function desempenoPorCapitulo(datos, progreso) {
  const filas = [];
  for (const cap of datos.capitulos) {
    const preguntas = datos.porCapitulo.get(cap.id).preguntas;
    let intentos = 0;
    let aciertos = 0;
    let tiempo = 0;
    for (const p of preguntas) {
      const registro = progreso.preguntas[p.id];
      if (!registro) continue;
      intentos += registro.intentos;
      aciertos += registro.aciertos;
      tiempo += registro.tiempo;
    }
    const tarjetas = datos.porCapitulo.get(cap.id).tarjetas;
    const dominadas = tarjetas.filter((t) => progreso.estudio[t.id]?.dominada).length;
    filas.push({
      ...cap,
      intentos,
      aciertos,
      exito: porcentaje(aciertos, intentos),
      tiempoMedio: intentos ? tiempo / intentos : 0,
      tarjetas: tarjetas.length,
      dominadas,
      avanceEstudio: porcentaje(dominadas, tarjetas.length),
    });
  }
  return filas;
}

export function desempenoPorGrupoSenales(datos, progreso) {
  const mapa = new Map();
  for (const senal of datos.senales) {
    if (!mapa.has(senal.grupo)) mapa.set(senal.grupo, { grupo: senal.grupo, total: 0, intentos: 0, aciertos: 0 });
    const fila = mapa.get(senal.grupo);
    fila.total += 1;
    const registro = progreso.senales[senal.codigo];
    if (registro) {
      fila.intentos += registro.intentos;
      fila.aciertos += registro.aciertos;
    }
  }
  return [...mapa.values()].map((f) => ({ ...f, exito: porcentaje(f.aciertos, f.intentos) }));
}

/** Señales y preguntas con peor rendimiento, para el módulo de Repaso. */
export function puntosDebiles(datos, progreso, limite = 12) {
  const preguntas = datos.preguntas
    .map((p) => ({ pregunta: p, registro: progreso.preguntas[p.id] }))
    .filter((x) => x.registro && x.registro.intentos > 0)
    .map((x) => ({ ...x, exito: porcentaje(x.registro.aciertos, x.registro.intentos) }))
    .filter((x) => x.exito < 100)
    .sort((a, b) => a.exito - b.exito || b.registro.intentos - a.registro.intentos)
    .slice(0, limite);

  const senales = datos.senales
    .map((s) => ({ senal: s, registro: progreso.senales[s.codigo] }))
    .filter((x) => x.registro && x.registro.intentos > 0)
    .map((x) => ({ ...x, exito: porcentaje(x.registro.aciertos, x.registro.intentos) }))
    .filter((x) => x.exito < 100)
    .sort((a, b) => a.exito - b.exito || b.registro.intentos - a.registro.intentos)
    .slice(0, limite);

  return { preguntas, senales };
}

export function resumenGeneral(datos, progreso) {
  const sesiones = progreso.sesiones || [];
  const tests = sesiones.filter((s) => s.tipo === 'test');
  const aprobados = tests.filter((s) => s.aprobado).length;
  let intentos = 0;
  let aciertos = 0;
  for (const registro of Object.values(progreso.preguntas)) {
    intentos += registro.intentos;
    aciertos += registro.aciertos;
  }
  for (const registro of Object.values(progreso.senales)) {
    intentos += registro.intentos;
    aciertos += registro.aciertos;
  }
  const dominadas = Object.values(progreso.estudio).filter((e) => e.dominada).length;
  return {
    sesiones: sesiones.length,
    tests: tests.length,
    aprobados,
    intentos,
    aciertos,
    exito: porcentaje(aciertos, intentos),
    dominadas,
    totalTarjetas: datos.tarjetas.length,
    avanceEstudio: porcentaje(dominadas, datos.tarjetas.length),
  };
}
