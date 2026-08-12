/* Conduce-Fácil · Vistas de acceso, configuración y administración. */

import { formatearFecha, h, icono, marcaSvg, navegar, porcentaje } from './nucleo_conduce_facil.js';
import { cargarSesionUsuario, estado, guardarPreferencias, limpiarSesion } from './contexto_conduce_facil.js';
import { desempenoPorCapitulo, resumenGeneral } from './datos_conduce_facil.js';
import { PROGRESO_VACIO } from './almacenamiento_conduce_facil.js';

const FOTO_ACCESO = '/assets/img/login_conduce_facil.jpg';
const ILUSTRACION_ACCESO = '/assets/manual/cf038a.png';

/* --------------------------------------------------------------- /login ---- */

export function vistaLogin(raiz) {
  document.title = 'Ingresar · Conduce-Fácil';

  const aviso = h('div', { class: 'aviso aviso-error oculto', role: 'alert' });
  const campoUsuario = h('input', {
    type: 'text', id: 'usuario', name: 'usuario', autocomplete: 'username',
    required: true, placeholder: 'Tu nombre de usuario',
  });
  const campoClave = h('input', {
    type: 'password', id: 'clave', name: 'clave', autocomplete: 'current-password',
    required: true, minlength: '6', placeholder: 'Mínimo 6 caracteres',
  });
  const boton = h('button', { type: 'submit', class: 'boton boton-principal boton-bloque' }, 'Entrar a estudiar');

  const formulario = h('form', {
    novalidate: true,
    onsubmit: async (evento) => {
      evento.preventDefault();
      aviso.classList.add('oculto');
      boton.disabled = true;
      boton.textContent = 'Verificando…';
      const resultado = await estado.repo.ingresar(campoUsuario.value, campoClave.value);
      if (!resultado.ok) {
        aviso.textContent = resultado.error || 'No fue posible iniciar sesión.';
        aviso.classList.remove('oculto');
        campoUsuario.setAttribute('aria-invalid', 'true');
        campoClave.setAttribute('aria-invalid', 'true');
        boton.disabled = false;
        boton.textContent = 'Entrar a estudiar';
        return;
      }
      await cargarSesionUsuario(resultado.usuario);
      navegar('/home');
    },
  }, [
    h('div', { class: 'campo' }, [h('label', { for: 'usuario' }, 'Usuario'), campoUsuario]),
    h('div', { class: 'campo' }, [h('label', { for: 'clave' }, 'Contraseña'), campoClave]),
    boton,
  ]);

  const foto = h('img', {
    src: FOTO_ACCESO,
    alt: 'Vía interurbana con vehículos circulando, ilustración del Manual CONASET para la Licencia Clase B',
    onerror: (evento) => { evento.currentTarget.src = ILUSTRACION_ACCESO; },
  });

  raiz.append(h('div', { class: 'pantalla-acceso' }, [
    h('section', { class: 'acceso-formulario' }, [
      h('div', { class: 'interior' }, [
        h('div', { class: 'acceso-marca' }, [
          marcaSvg(52),
          h('span', { class: 'palabra', html: 'Conduce<em>-Fácil</em>' }),
        ]),
        h('h1', {}, 'Prepara tu examen teórico Clase B'),
        h('p', { style: 'color:var(--gris-medio);margin-bottom:32px' },
          'Ingresa con tu cuenta para continuar donde quedaste: estudio por capítulos, trivia de señaléticas y tests cronometrados.'),
        aviso,
        formulario,
        h('p', { class: 'pie-desarrollo' }, [
          'Contenidos oficiales del Libro para la Conducción en Chile (CONASET) y del Manual de Señalización de Tránsito. ',
          h('br'), 'Desarrollado por ', h('strong', {}, 'Gamonal'), '.',
        ]),
      ]),
    ]),
    h('aside', { class: 'acceso-visual' }, [
      foto,
      h('div', { class: 'mensaje' }, [
        h('p', {}, [
          h('strong', {}, '35 preguntas, máximo 2 errores.'),
          'Practica con los contenidos textuales del manual y con las 186 señaléticas oficiales hasta que el examen deje de ser un problema.',
        ]),
      ]),
    ]),
  ]));
}

/* ------------------------------------------------------- /configuracion ---- */

export function vistaConfiguracion(raiz) {
  document.title = 'Configuración · Conduce-Fácil';
  const usuario = estado.usuario;

  raiz.append(h('div', { class: 'cabecera-pagina' }, [
    h('h1', {}, 'Configuración'),
    h('p', {}, 'Ajusta tu cuenta y la forma en que quieres practicar.'),
  ]));

  /* --- Cuenta --- */
  const avisoClave = h('div', { class: 'aviso oculto', role: 'status' });
  const actual = h('input', { type: 'password', id: 'clave-actual', autocomplete: 'current-password', required: true });
  const nueva = h('input', { type: 'password', id: 'clave-nueva', autocomplete: 'new-password', required: true, minlength: '6' });
  const repetida = h('input', { type: 'password', id: 'clave-repetida', autocomplete: 'new-password', required: true, minlength: '6' });

  const formClave = h('form', {
    onsubmit: async (evento) => {
      evento.preventDefault();
      avisoClave.className = 'aviso oculto';
      if (nueva.value !== repetida.value) {
        avisoClave.className = 'aviso aviso-error';
        avisoClave.textContent = 'La contraseña nueva y su repetición no coinciden.';
        return;
      }
      const resultado = await estado.repo.cambiarClave(usuario.id, actual.value, nueva.value);
      avisoClave.className = resultado.ok ? 'aviso aviso-exito' : 'aviso aviso-error';
      avisoClave.textContent = resultado.ok
        ? 'Contraseña actualizada correctamente.'
        : resultado.error || 'No fue posible cambiar la contraseña.';
      if (resultado.ok) formClave.reset();
    },
  }, [
    h('div', { class: 'campo' }, [h('label', { for: 'clave-actual' }, 'Contraseña actual'), actual]),
    h('div', { class: 'campo' }, [
      h('label', { for: 'clave-nueva' }, 'Contraseña nueva'), nueva,
      h('p', { class: 'ayuda' }, 'Al menos 6 caracteres.'),
    ]),
    h('div', { class: 'campo' }, [h('label', { for: 'clave-repetida' }, 'Repite la contraseña nueva'), repetida]),
    h('button', { type: 'submit', class: 'boton boton-principal' }, 'Guardar contraseña'),
  ]);

  /* --- Preferencias --- */
  const cronometro = h('input', {
    type: 'checkbox', id: 'pref-cronometro', checked: estado.preferencias.mostrarCronometro,
    onchange: (evento) => {
      estado.preferencias.mostrarCronometro = evento.currentTarget.checked;
      guardarPreferencias();
    },
  });
  const limite = h('select', {
    id: 'pref-limite',
    onchange: (evento) => {
      estado.preferencias.segundosPorPregunta = Number(evento.currentTarget.value);
      guardarPreferencias();
    },
  }, [
    h('option', { value: '0' }, 'Sin límite'),
    h('option', { value: '30' }, '30 segundos por pregunta'),
    h('option', { value: '45' }, '45 segundos por pregunta'),
    h('option', { value: '60' }, '60 segundos por pregunta'),
  ]);
  limite.value = String(estado.preferencias.segundosPorPregunta || 0);

  const avisoDatos = h('div', { class: 'aviso oculto', role: 'status' });

  raiz.append(h('div', { class: 'rejilla rejilla-2' }, [
    h('section', { class: 'tarjeta' }, [
      h('h2', {}, 'Tu cuenta'),
      h('p', { style: 'color:var(--gris-medio)' }, [
        'Usuario: ', h('strong', {}, usuario.usuario), ' · Perfil: ',
        h('strong', {}, usuario.rol === 'admin' ? 'Administración' : 'Estudiante'),
      ]),
      h('h3', { style: 'margin-top:24px' }, 'Cambiar contraseña'),
      avisoClave,
      formClave,
    ]),
    h('section', { class: 'tarjeta' }, [
      h('h2', {}, 'Preferencias de práctica'),
      h('div', { class: 'opcion-caja' }, [
        cronometro, h('label', { for: 'pref-cronometro' }, 'Mostrar el cronómetro durante los ejercicios'),
      ]),
      h('div', { class: 'campo', style: 'margin-top:16px' }, [
        h('label', { for: 'pref-limite' }, 'Tiempo máximo por pregunta en el test'),
        limite,
        h('p', { class: 'ayuda' }, 'Al agotarse el tiempo la pregunta se marca como incorrecta y el test avanza.'),
      ]),
      h('h3', { style: 'margin-top:24px' }, 'Tus datos de práctica'),
      avisoDatos,
      h('p', { style: 'color:var(--gris-medio)' },
        'Puedes reiniciar tus estadísticas si quieres empezar de cero. Los contenidos del manual no se modifican.'),
      h('button', {
        type: 'button', class: 'boton boton-secundario',
        onclick: async (evento) => {
          const boton = evento.currentTarget;
          if (boton.dataset.confirmar !== 'si') {
            boton.dataset.confirmar = 'si';
            boton.textContent = 'Pulsa otra vez para confirmar el reinicio';
            setTimeout(() => {
              boton.dataset.confirmar = 'no';
              boton.textContent = 'Reiniciar mis estadísticas';
            }, 6000);
            return;
          }
          estado.progreso = PROGRESO_VACIO();
          await estado.repo.guardarProgreso(usuario.id, estado.progreso);
          boton.dataset.confirmar = 'no';
          boton.textContent = 'Reiniciar mis estadísticas';
          avisoDatos.className = 'aviso aviso-exito';
          avisoDatos.textContent = 'Estadísticas reiniciadas.';
        },
      }, 'Reiniciar mis estadísticas'),
      h('h3', { style: 'margin-top:24px' }, 'Almacenamiento'),
      h('p', { style: 'color:var(--gris-medio);margin:0' }, estado.repo.modo === 'servidor'
        ? 'Modo servidor: tus resultados se guardan de forma centralizada y quedan disponibles desde cualquier dispositivo.'
        : 'Modo local: tus resultados se guardan en este navegador. Al conectar la base de datos del proyecto pasan a guardarse de forma centralizada.'),
    ]),
  ]));
}

/* --------------------------------------------------------------- /admin ---- */

export async function vistaAdmin(raiz) {
  document.title = 'Administración · Conduce-Fácil';
  if (estado.usuario.rol !== 'admin') {
    raiz.append(h('div', { class: 'aviso aviso-alerta' }, 'Esta sección está disponible sólo para cuentas de administración.'));
    return;
  }

  raiz.append(h('div', { class: 'cabecera-pagina' }, [
    h('h1', {}, 'Administración'),
    h('p', {}, 'Gestiona las cuentas del aplicativo y revisa el avance de todas las personas usuarias.'),
  ]));

  const contenedorTabla = h('div', { class: 'tabla-envoltorio' });
  const avisoAlta = h('div', { class: 'aviso oculto', role: 'status' });

  const nuevoUsuario = h('input', { type: 'text', id: 'nuevo-usuario', required: true, placeholder: 'ej.: camila' });
  const nuevoNombre = h('input', { type: 'text', id: 'nuevo-nombre', placeholder: 'ej.: Camila Rojas' });
  const nuevaClave = h('input', { type: 'password', id: 'nueva-clave', required: true, minlength: '6', autocomplete: 'new-password' });
  const nuevoRol = h('select', { id: 'nuevo-rol' }, [
    h('option', { value: 'estudiante' }, 'Estudiante'),
    h('option', { value: 'admin' }, 'Administración'),
  ]);

  async function pintarTabla() {
    const usuarios = await estado.repo.listarUsuarios();
    const filas = [];
    for (const cuenta of usuarios) {
      const progreso = await estado.repo.progreso(cuenta.id);
      const resumen = resumenGeneral(estado.datos, progreso);
      const ultima = progreso.sesiones[0];
      filas.push(h('tr', {}, [
        h('td', {}, [
          h('strong', {}, cuenta.nombre || cuenta.usuario),
          h('div', { style: 'font-size:13px;color:var(--gris-medio)' }, `@${cuenta.usuario}`),
        ]),
        h('td', {}, h('span', {
          class: `etiqueta ${cuenta.rol === 'admin' ? 'etiqueta-info' : 'etiqueta-neutra'}`,
        }, cuenta.rol === 'admin' ? 'Administración' : 'Estudiante')),
        h('td', { class: 'num' }, String(resumen.tests)),
        h('td', { class: 'num' }, `${resumen.exito}%`),
        h('td', { class: 'num' }, `${resumen.avanceEstudio}%`),
        h('td', {}, ultima ? formatearFecha(ultima.fecha) : 'Sin actividad'),
        h('td', {}, cuenta.id === estado.usuario.id ? h('span', { style: 'color:var(--gris-medio)' }, 'Tu cuenta')
          : h('button', {
            type: 'button', class: 'boton boton-texto',
            onclick: async (evento) => {
              const boton = evento.currentTarget;
              if (boton.dataset.confirmar !== 'si') {
                boton.dataset.confirmar = 'si';
                boton.textContent = 'Confirmar';
                setTimeout(() => { boton.dataset.confirmar = 'no'; boton.textContent = 'Eliminar'; }, 5000);
                return;
              }
              const resultado = await estado.repo.eliminarUsuario(cuenta.id);
              avisoAlta.className = resultado.ok ? 'aviso aviso-exito' : 'aviso aviso-error';
              avisoAlta.textContent = resultado.ok ? 'Cuenta eliminada.' : resultado.error;
              pintarTabla();
            },
          }, 'Eliminar')),
      ]));
    }

    contenedorTabla.replaceChildren(h('table', { class: 'tabla' }, [
      h('thead', {}, h('tr', {}, [
        h('th', {}, 'Persona'), h('th', {}, 'Perfil'),
        h('th', { class: 'num' }, 'Tests'), h('th', { class: 'num' }, 'Aciertos'),
        h('th', { class: 'num' }, 'Estudio'), h('th', {}, 'Última actividad'), h('th', {}, ''),
      ])),
      h('tbody', {}, filas),
    ]));
  }

  raiz.append(h('section', { class: 'tarjeta', style: 'margin-bottom:24px' }, [
    h('h2', {}, 'Personas usuarias'),
    h('p', { style: 'color:var(--gris-medio)' },
      'Cada persona ve únicamente sus propios resultados. Desde aquí puedes revisar el avance de todas.'),
    contenedorTabla,
  ]));

  raiz.append(h('section', { class: 'tarjeta' }, [
    h('h2', {}, 'Crear una cuenta'),
    avisoAlta,
    h('form', {
      onsubmit: async (evento) => {
        evento.preventDefault();
        const formulario = evento.currentTarget;
        const nombreCreado = nuevoUsuario.value;
        const resultado = await estado.repo.crearUsuario({
          usuario: nuevoUsuario.value,
          nombre: nuevoNombre.value,
          clave: nuevaClave.value,
          rol: nuevoRol.value,
        });
        avisoAlta.className = resultado.ok ? 'aviso aviso-exito' : 'aviso aviso-error';
        avisoAlta.textContent = resultado.ok
          ? `Cuenta creada. ${nombreCreado} ya puede ingresar con la contraseña indicada.`
          : resultado.error;
        if (resultado.ok) {
          formulario.reset();
          await pintarTabla();
        }
      },
    }, [
      h('div', { class: 'rejilla rejilla-2' }, [
        h('div', { class: 'campo' }, [h('label', { for: 'nuevo-usuario' }, 'Usuario'), nuevoUsuario]),
        h('div', { class: 'campo' }, [h('label', { for: 'nuevo-nombre' }, 'Nombre para mostrar'), nuevoNombre]),
        h('div', { class: 'campo' }, [
          h('label', { for: 'nueva-clave' }, 'Contraseña inicial'), nuevaClave,
          h('p', { class: 'ayuda' }, 'Al menos 6 caracteres. La persona puede cambiarla desde Configuración.'),
        ]),
        h('div', { class: 'campo' }, [h('label', { for: 'nuevo-rol' }, 'Perfil'), nuevoRol]),
      ]),
      h('button', { type: 'submit', class: 'boton boton-principal' }, 'Crear cuenta'),
    ]),
  ]));

  await pintarTabla();
}

/* -------------------------------------------------------------- Utilidad --- */

export async function cerrarSesion() {
  await estado.repo.salir();
  limpiarSesion();
  navegar('/login');
}

export { desempenoPorCapitulo, icono, porcentaje };
