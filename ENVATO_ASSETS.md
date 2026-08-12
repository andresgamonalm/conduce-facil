# Recursos de Envato · Conduce-Fácil

Registro de los recursos seleccionados en Envato Elements para este proyecto,
según `lineamientos-marca-gamonal` (`references/registro-envato.md`).

## Estado actual

| # | Uso previsto | Recurso | Autoría | Código | URL | Estado |
|---|---|---|---|---|---|---|
| 1 | Panel visual de `/login` | Man and instructor in car. Passing driving license exam | africaimages | `Z4CSKHM` | https://elements.envato.com/man-and-instructor-in-car-passing-driving-license--Z4CSKHM | Seleccionado · pendiente de descarga |
| 2 | Alternativa para `/login` | Process of driving. Woman is with instructor in car, driving school concept | mstandret | `CWM7KAN` | https://elements.envato.com/process-of-driving-woman-is-with-instructor-in-car-CWM7KAN | Alternativa aprobada |
| 3 | Alternativa vertical para `/login` | Hands of teenage girl at car steering wheel | westend61 | `VDE3AV5` | https://elements.envato.com/hands-of-teenage-girl-at-car-steering-wheel-VDE3AV5 | Alternativa aprobada |

## Por qué todavía no está integrada

La búsqueda en Envato Elements se realizó desde el conector y los recursos
quedaron seleccionados. La descarga no fue posible: la política de red del
entorno de desarrollo bloquea el dominio `elements-resized.envatousercontent.com`
(el proxy responde `403` a la conexión). No se trata de una falta de sesión ni de
permisos de Envato.

## Qué se está usando mientras tanto

El panel visual de `/login` y la portada de `/home` usan una **ilustración
oficial del Manual CONASET** (`public/assets/manual/cf038a.png`, página 38 del
Libro para la Conducción en Chile): una vía interurbana con vehículos en
circulación. Es un recurso visual real, pertinente al producto, de alta calidad y
con reproducción autorizada por CONASET. No es una caja de color, un ícono ni una
figura improvisada.

## Cómo completar la sustitución

1. Descargar desde Envato Elements el recurso **`Z4CSKHM`** en su mayor
   resolución disponible.
2. Guardarlo como:

   ```
   public/assets/img/login_conduce_facil.jpg
   ```

3. Listo. El aplicativo lo toma automáticamente: `/login` carga esa ruta y sólo
   vuelve a la ilustración de CONASET si el archivo no existe. No hay que tocar
   código ni configuración.

Recomendación de encuadre: recorte vertical con la persona conductora ubicada en
el tercio superior, de modo que el mensaje azul del pie no se superponga a la
cara. Ancho mínimo sugerido: 1600 px.
