# Conduce-Fácil

Aplicativo web para preparar el **examen teórico de la Licencia de Conducir
Clase B en Chile**: 35 preguntas, máximo 2 respuestas erróneas.

Todo el contenido proviene de los manuales oficiales incluidos en este
repositorio y se publica **sin modificaciones**:

- *Libro para la Conducción en Chile · Licencia Clase B* (CONASET, julio 2024)
- *Manual de Señalización de Tránsito* (Ministerio de Transportes y Telecomunicaciones)

---

## Abrir el aplicativo

**Doble clic** en el archivo correspondiente a tu sistema:

| Sistema | Archivo |
|---|---|
| macOS y Linux | `abrir_conduce_facil.command` |
| Windows | `abrir_conduce_facil.bat` |

Levanta el servidor local y abre el navegador en la pantalla de acceso. No hay
que instalar nada ni escribir comandos.

---

## Qué incluye

| Módulo | Contenido |
|---|---|
| **Estudio** | 555 contenidos del Manual CONASET en formato pregunta y respuesta, con la página citada y 349 imágenes originales del propio manual. |
| **Trivia de señalética** | 186 señaléticas oficiales extraídas del Manual de Señalización. Se muestra la señal sin su nombre y se elige entre cuatro alternativas. |
| **Test de prueba** | 188 preguntas de alternativas con su fundamento literal citado. Cantidad, capítulos, señalética y tiempo por pregunta configurables. Cronómetro por pregunta. |
| **Repaso** | Capítulos, familias de señales, señales y preguntas ordenados por debilidad, con acceso directo a la práctica. |
| **Resultados** | Historial de cada test y trivia con puntaje, tiempo total, tiempo por pregunta, veces respondida y tasa de éxito. |
| **Configuración** | Cambio de contraseña, cronómetro, límite de tiempo por pregunta y reinicio de estadísticas. |
| **Administración** | Alta y baja de cuentas y avance de todas las personas usuarias. Sólo para el perfil de administración. |

Cada persona ve únicamente sus propios resultados. El perfil de administración
puede verlos todos, pero no modificarlos.

---

## Fidelidad de los contenidos

Las respuestas de estudio y los fundamentos de las preguntas **no están
redactados ni resumidos**: se recortan literalmente del PDF mediante anclas de
texto. Si un ancla no existe en el manual, la generación falla y el contenido no
se publica.

Un script comprueba, contra los PDF oficiales, que cada contenido publicado
exista literalmente en la página que cita:

```
python3 herramientas/verificar_contenidos.py
```

Resultado actual: **929 contenidos verificados, sin discrepancias**
(555 tarjetas de estudio, 188 preguntas y 186 señaléticas).

---

## Estructura

```
public/                     Sitio publicable en Cloudflare Pages
  index.html                Documento del aplicativo y biblioteca de íconos
  assets/css|js|fonts       Estilos, módulos JavaScript y tipografía Roboto
  assets/marca              Logotipo, ícono, ICO, favicon y PNG 1000 × 1000
  assets/senales            186 señaléticas del Manual de Señalización
  assets/manual             349 figuras del Manual CONASET
  datos                     Contenidos generados (estudio, preguntas, señales)
functions/api               API opcional (Cloudflare Pages Functions + D1)
herramientas                Extracción, generación, verificación y servidor local
documentacion               Documentos Word, capturas y portada
Manual-Conaset              PDF oficial de CONASET (fuente del contenido)
Manual-Señalizacion         PDF oficiales del Manual de Señalización
```

---

## Regenerar contenidos

```bash
python3 herramientas/generar_datos.py         # reconstruye los JSON desde los PDF
python3 herramientas/verificar_contenidos.py  # comprueba la fidelidad
python3 herramientas/generar_marca.py         # rehace la identidad visual
python3 herramientas/generar_portada.py       # rehace la portada
python3 herramientas/generar_documentos.py    # rehace los documentos Word
```

Requiere Python 3.11 o superior con `pymupdf`, `Pillow`, `cairosvg` y
`python-docx`.

---

## Publicación

El aplicativo funciona en **dos modos**, sin cambios en el código:

- **Modo local** (por defecto): las cuentas y los resultados se guardan en el
  navegador. Funciona apenas se abre, sin infraestructura.
- **Modo servidor**: al enlazar una base de datos D1, las cuentas y los
  resultados se guardan de forma centralizada y quedan disponibles desde
  cualquier dispositivo.

Publicar en Cloudflare Pages:

```bash
npx wrangler pages deploy public --project-name conduce-facil
```

Activar el modo servidor:

```bash
npx wrangler d1 create conduce-facil
# copiar el database_id en el bloque [[d1_databases]] de wrangler.toml y descomentarlo
```

La publicación y el enlace del subdominio `conduce-facil.gamonal.app` requieren
autorización de la persona propietaria de la cuenta: no se ejecutaron.

---

## Documentación

- `documentacion/documentacion_general_tecnica_conduce_facil.docx`
- `documentacion/descripcion_publicitaria_conduce_facil.docx`
- `documentacion/capturas/` · capturas del producto en 1920 × 1080
- `documentacion/portada_presentacion_conduce_facil.jpg`
- `DECISIONES-VISUALES.md` · registro de decisiones de identidad
- `ENVATO_ASSETS.md` · recursos de Envato seleccionados y su estado

---

Desarrollado por **Gamonal**.
