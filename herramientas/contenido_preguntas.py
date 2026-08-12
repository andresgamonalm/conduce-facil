"""Banco de preguntas de alternativas del Test de prueba de Conduce-Fácil.

La alternativa correcta y el fundamento provienen del Manual CONASET: el
fundamento se recorta literalmente del PDF con anclas de texto, de modo que cada
pregunta queda trazada a su página de origen. Las alternativas incorrectas son
enunciados falsos redactados para el ejercicio; nunca son texto del manual
alterado.
"""

from __future__ import annotations

from texto_manual import TextoNoEncontrado, literal

PREGUNTAS: list[dict] = []
ERRORES: list[str] = []


def P(cap: str, enunciado: str, opciones: list[str], correcta: int, pagina: int,
      desde: str, hasta: str | None = None, extra: int = 1) -> None:
    try:
        fundamento = literal(pagina, desde, hasta, paginas_extra=extra)
    except TextoNoEncontrado as e:
        ERRORES.append(f"[{cap} p{pagina}] {enunciado[:60]} :: {e}")
        return
    if not (0 <= correcta < len(opciones)):
        ERRORES.append(f"[{cap}] índice de alternativa correcta fuera de rango: {enunciado[:60]}")
        return
    PREGUNTAS.append(
        {
            "id": f"p{len(PREGUNTAS) + 1:03d}",
            "capitulo": cap,
            "enunciado": enunciado,
            "opciones": opciones,
            "correcta": correcta,
            "fundamento": fundamento,
            "pagina": pagina,
        }
    )


# --- Capítulo 1 -------------------------------------------------------------
P("cap1", "¿Cuántos siniestros de tránsito se registran anualmente en Chile?",
  ["Más de 82.000", "Cerca de 12.000", "Alrededor de 250.000", "Menos de 5.000"], 0,
  8, "Anualmente en Chile se registran más de 82.000 siniestros", "En promedio 450 de ellas son atropelladas.")
P("cap1", "¿Qué porcentaje de los siniestros de tránsito se produce en vías o áreas urbanas?",
  ["Aproximadamente un 80%", "Aproximadamente un 20%", "Exactamente un 50%", "Menos de un 10%"], 0,
  8, "Si bien la mayor cantidad de personas fallecidas en siniestros", "se produce en zonas no urbanas (rural).")
P("cap1", "La probabilidad de que un peatón muera atropellado se multiplica por ocho cuando la velocidad del vehículo sube de:",
  ["30 a 50 km/h", "50 a 60 km/h", "20 a 30 km/h", "60 a 90 km/h"], 0,
  8, "La probabilidad de que un peatón muera atropellado", "de 30 a 50 km/h.")
P("cap1", "¿Qué probabilidad de sobrevivir tiene un peatón ante un impacto a 30 km/h o menos?",
  ["90%", "50%", "25%", "10%"], 0,
  8, "Peatones tienen 90% de posibilidades de sobrevivir", "a impactos a 30 km/h o menos.")
P("cap1", "¿En qué porcentaje de los siniestros de tránsito está presente la falla humana?",
  ["En más del 90%", "En cerca del 40%", "En un 60%", "En menos del 20%"], 0,
  8, "Además, las estadísticas indican que la falla humana", "involucrando mayormente a jóvenes, entre 18 y 29 años.")
P("cap1", "El enfoque de Sistema Seguro, conocido mundialmente como Visión Cero, establece como principio ético que:",
  ["Las muertes y lesiones graves en el tránsito son inaceptables",
   "Los siniestros son inevitables y deben asumirse",
   "Sólo la persona conductora es responsable del resultado",
   "La velocidad no incide en la gravedad de las lesiones"], 0,
  9, "establece como principio ético que las muertes y lesiones graves en el tránsito son inaceptables",
  "conocido mundialmente como la Visión Cero.")
P("cap1", "¿A cuánto alcanzan en Chile los costos de los siniestros de tránsito según cifras de la OMS?",
  ["Al 2% del PIB", "Al 0,1% del PIB", "Al 15% del PIB", "Al 25% del PIB"], 0,
  7, "Se estima que en Chile los costos de los siniestros de tránsito", "el 2% del PIB según las cifras de la OMS.")

# --- Capítulo 2 -------------------------------------------------------------
P("cap2", "¿Qué indica el tacómetro del panel de instrumentos?",
  ["La velocidad del motor en revoluciones por minuto",
   "La rapidez instantánea del vehículo",
   "La distancia total recorrida",
   "La temperatura del líquido refrigerante"], 0,
  11, "Tacómetro: Velocidad del motor en revoluciones por minuto.")
P("cap2", "¿Qué informan los testigos de color rojo del panel de instrumentos?",
  ["Atención inmediata, avería grave", "La puesta en funcionamiento", "Un posible problema a revisar", "El nivel de combustible"], 0,
  11, "Testigos color rojo: Informan atención inmediata, avería grave.")
P("cap2", "Si se enciende la luz indicadora de presión de aceite, ¿qué debes hacer?",
  ["Detener el motor de inmediato y no ponerlo en marcha hasta haberlo reparado",
   "Continuar la marcha y revisar al llegar a destino",
   "Acelerar para aumentar la presión del sistema",
   "Apagar el testigo y seguir conduciendo con normalidad"], 0,
  12, "se enciende en el panel de instrumentos la luz indicadora de la presión de aceite",
  "ya que le puedes causar averías graves.")
P("cap2", "¿Qué componente convierte la energía mecánica en eléctrica en el vehículo?",
  ["El alternador", "La batería", "El radiador", "El embrague"], 0,
  12, "El alternador convierte la energía mecánica en eléctrica", "que viene desde el motor.")
P("cap2", "Si una unidad eléctrica deja de funcionar, ¿qué debes revisar primero?",
  ["Si se ha fundido algún fusible", "El nivel de aceite", "La presión de los neumáticos", "El líquido refrigerante"], 0,
  12, "Por lo que, si alguna unidad eléctrica deja de funcionar", "si se ha fundido algún fusible.")
P("cap2", "En el indicador de combustible, ¿qué significan las letras E y F?",
  ["E significa vacío y F, estanque lleno", "E significa lleno y F, vacío", "E indica economía y F, fuerza", "E es la reserva y F, el filtro"], 0,
  13, "En el indicador de combustible, la letra E significa vacío", "del inglés \"Full\".")
P("cap2", "¿Qué gas venenoso, incoloro e inoloro contienen los gases de escape?",
  ["El monóxido de carbono", "El oxígeno", "El nitrógeno puro", "El vapor de agua"], 0,
  14, "Estos gases de escape contienen sustancias tóxicas", "incoloro e inoloro.")
P("cap2", "¿Cuáles son los primeros síntomas de intoxicación con monóxido de carbono?",
  ["El dolor de cabeza y los vómitos", "La visión borrosa y el hormigueo", "La tos seca y el estornudo", "El dolor muscular y la fiebre"], 0,
  14, "Los primeros síntomas de intoxicación con monóxido de carbono, son el dolor de cabeza y los vómitos.")
P("cap2", "Conducir presionando el embrague durante un tiempo mayor al necesario:",
  ["Reduce el control sobre el vehículo", "Aumenta la potencia del motor", "Mejora la adherencia de los neumáticos", "No tiene ningún efecto"], 0,
  14, "Debes saber que al conducir presionando el embrague", "se reduce el control sobre el vehículo.")
P("cap2", "El freno de estacionamiento (freno de mano) es:",
  ["Mecánico y generalmente actúa sobre las ruedas traseras",
   "Hidráulico y actúa sobre las cuatro ruedas",
   "Eléctrico y actúa sobre las ruedas delanteras",
   "Neumático y sólo funciona con el motor apagado"], 0,
  16, "2. El freno de estacionamiento (freno de mano) es mecánico", "sobre las ruedas traseras.")
P("cap2", "¿Qué ocurre con la dirección del vehículo cuando las ruedas se bloquean en una frenada brusca?",
  ["Es imposible controlar la dirección del vehículo",
   "La dirección se vuelve más precisa",
   "El vehículo se detiene en menos metros",
   "Se activa automáticamente el freno de mano"], 0,
  16, "Además, en estas condiciones es imposible controlar la dirección del vehículo",
  "no se pueda evitar el obstáculo.")
P("cap2", "Con frenos ABS, ¿qué debe hacer la persona conductora en una frenada de emergencia?",
  ["Mantener presionado a fondo el pedal de freno",
   "Bombear el pedal de freno repetidamente",
   "Soltar el freno cada vez que sienta vibración",
   "Usar únicamente el freno de mano"], 0,
  17, "El ABS (sistema de frenado antibloqueo) detecta", "mantenga el control sobre la dirección del vehículo.")
P("cap2", "¿Cuál es la profundidad mínima aconsejable de los dibujos o surcos de las bandas de rodamiento?",
  ["3 mm", "1,6 mm", "0,5 mm", "10 mm"], 0,
  18, "los dibujos o surcos de sus bandas de rodamiento deben tener una profundidad aconsejable mínima de 3 mm.")
P("cap2", "Por debajo de qué profundidad de dibujo empeora la fricción con el pavimento mojado:",
  ["Inferior a 1,6 mm", "Inferior a 5 mm", "Inferior a 3 cm", "Inferior a 0,1 mm"], 0,
  18, "Cuando la profundidad de tales dibujos es muy baja (inferior a 1,6 mm)",
  "que se forma adelante de los neumáticos.")
P("cap2", "¿Cada cuánto deben cambiarse los neumáticos aunque tengan poco uso?",
  ["Al menos cada 5 años", "Cada 15 años", "Sólo cuando revientan", "Cada 6 meses"], 0,
  19, "Los neumáticos deben ser cambiados al menos cada 5 años.", "pierden sus propiedades para rodar con seguridad.")
P("cap2", "Si se revienta un neumático trasero mientras conduces, debes:",
  ["Girar el volante hacia el lado en que se desvía la cola del vehículo",
   "Frenar bruscamente y girar hacia el lado contrario",
   "Acelerar para estabilizar el vehículo",
   "Soltar el volante y dejar que el vehículo se detenga solo"], 0,
  19, "Si al ir conduciendo se revienta un neumático trasero", "se desvía la cola del vehículo.")
P("cap2", "Si se revienta un neumático delantero, debes:",
  ["Frenar de forma suave sosteniendo el volante firmemente",
   "Frenar bruscamente hasta detenerte",
   "Girar el volante hacia la berma",
   "Acelerar para superar el tramo"], 0,
  19, "Si de lo contrario, se revienta un neumático delantero", "sosteniendo el volante firmemente.")
P("cap2", "Un desgaste notorio en la zona central de la banda de rodamiento significa que los neumáticos:",
  ["Se han usado con exceso de aire", "Se han usado con poca presión", "Están mal balanceados", "Están vencidos"], 0,
  19, "Un desgaste notorio en la zona central de la banda de rodamiento", "los neumáticos se han usado con exceso de aire")
P("cap2", "Al aumentar la velocidad al doble, la energía del movimiento aumenta:",
  ["4 veces", "2 veces", "8 veces", "No varía"], 0,
  23, "Al aumentar la velocidad al doble, la energía del movimiento aumenta 4 veces")
P("cap2", "¿Cuánto es un tiempo normal de reacción de una persona conductora?",
  ["Un segundo", "Cinco segundos", "Una décima de segundo", "Tres segundos"], 0,
  23, "Un tiempo normal de reacción es un segundo.")
P("cap2", "La distancia de detención (S) corresponde a:",
  ["La suma de la distancia de reacción y la distancia de frenado",
   "Sólo la distancia de frenado",
   "Sólo la distancia recorrida mientras se reacciona",
   "La distancia entre dos vehículos"], 0,
  23, "La distancia de detención (S) es la suma de la distancia de reacción (R) y la distancia de frenado (F).")
P("cap2", "Si duplicas la velocidad, la distancia de frenado aumenta:",
  ["Cuatro veces", "Dos veces", "Ocho veces", "No aumenta"], 0,
  24, "La distancia de frenado crece al cuadrado", "la distancia de frenado aumenta cuatro veces")
P("cap2", "Si el vehículo NO cuenta con frenos ABS y se bloquean las ruedas al frenar, hay que:",
  ["Reducir en seguida la presión sobre el pedal de freno soltándolo",
   "Mantener el pedal presionado a fondo hasta detenerse",
   "Accionar el freno de mano de golpe",
   "Girar el volante bruscamente"], 0,
  24, "Si el vehículo no cuenta con frenos ABS y se bloquean las ruedas",
  "la presión sobre el pedal de freno soltándolo.")
P("cap2", "¿Qué es un elemento de seguridad pasiva?",
  ["El cinturón de seguridad y el airbag", "Los frenos y las luces", "Los neumáticos", "El sistema de dirección"], 0,
  26, "Son los componentes de seguridad del vehículo que contribuyen a evitar",
  "el cinturón de seguridad y el airbag.")
P("cap2", "El uso del cinturón de seguridad en los asientos traseros es obligatorio si el vehículo:",
  ["Tiene un año de fabricación 2002 o posterior",
   "Tiene más de 10 años de antigüedad",
   "Circula en carretera solamente",
   "Transporta más de tres pasajeros"], 0,
  26, "El uso de este elemento en los asientos traseros, es obligatorio", "de fabricación 2002 o posterior.")
P("cap2", "Un choque a 50 km/h sin cinturón de seguridad equivale a:",
  ["Tirarse a la calle desde un cuarto piso sin red de seguridad",
   "Caer desde un primer piso",
   "Un golpe sin consecuencias",
   "Caer desde un piso 20"], 0,
  26, "Un choque a 50 km/h sin llevar puesto el cinturón de seguridad", "sin red de seguridad.")
P("cap2", "Quienes no usan el cinturón de seguridad tienen, respecto de quienes sí lo usan:",
  ["El doble de probabilidad de fallecer en un siniestro",
   "La misma probabilidad de fallecer",
   "Un 10% más de probabilidad de fallecer",
   "Menor probabilidad de fallecer"], 0,
  28, "El estudio de miles de siniestros demuestra que las personas que no usan el cinturón",
  "tienen el doble de probabilidad de fallecer en ellos.")
P("cap2", "Si una persona sale eyectada del vehículo por no usar cinturón, la probabilidad de sufrir una lesión medular aumenta en:",
  ["1.300%", "13%", "130%", "3%"], 0,
  28, "la probabilidad de sufrir una lesión medular aumenta en un 1.300%",
  "la probabilidad de resultar fallecida aumenta en un 300%")
P("cap2", "¿A qué velocidad se infla la bolsa de aire del airbag al producirse un siniestro?",
  ["Hasta 300 km/h", "Hasta 30 km/h", "Hasta 1.000 km/h", "Hasta 100 km/h"], 0,
  30, "Al producirse un siniestro, la bolsa de aire se infla a una velocidad de hasta 300 km/h")
P("cap2", "El uso del airbag frontal junto con el cinturón de seguridad puede reducir la probabilidad de lesiones mortales en:",
  ["Un 20%", "Un 2%", "Un 70%", "Un 100%"], 0,
  30, "Se ha estimado que el uso de airbag frontal", "reducir un 20% la probabilidad de sufrir lesiones mortales.")
P("cap2", "¿Cuál es la separación máxima que debe existir entre la cabeza y el apoya cabezas?",
  ["Nunca superior a 4 cm", "Nunca superior a 15 cm", "No importa la separación", "Exactamente 10 cm"], 0,
  31, "La separación entre la cabeza y el apoya cabezas debe ser la mínima posible", "nunca superior a 4 cm.")
P("cap2", "¿Dónde debe quedar situado el borde superior del apoya cabezas?",
  ["Entre el límite superior de la cabeza y la altura de los ojos",
   "Por debajo de la nuca",
   "A la altura de los hombros",
   "Sobre el techo del vehículo"], 0,
  31, "El borde superior del apoya cabezas debe quedar situado", "y la altura de los ojos.")

# --- Capítulo 3 -------------------------------------------------------------
P("cap3", "¿Qué porcentaje de los siniestros de tránsito con víctimas son producto de fallas humanas?",
  ["Cerca del 90%", "Cerca del 40%", "Cerca del 10%", "Cerca del 60%"], 0,
  33, "Cerca del 90% de los siniestros de tránsito con víctimas son producto de fallas humanas")
P("cap3", "¿Cuál es el principio fundamental en la conducción de un vehículo?",
  ["La precaución", "La rapidez", "La destreza mecánica", "La confianza en los demás"], 0,
  35, "La precaución es el principio fundamental en la conducción de un vehículo.")
P("cap3", "¿En qué proporción de los siniestros con víctimas está presente la velocidad inadecuada?",
  ["En la cuarta parte", "En la mitad", "En la totalidad", "En menos del 1%"], 0,
  34, "Velocidad inadecuada, presente en la cuarta parte de los siniestros con víctimas.")

# --- Capítulo 4 -------------------------------------------------------------
P("cap4", "Las personas conductoras principiantes sufren siniestros (sin otros vehículos involucrados) con una frecuencia:",
  ["10 veces mayor que quienes tienen más experiencia",
   "Igual a la de quienes tienen más experiencia",
   "2 veces menor",
   "100 veces mayor"], 0,
  37, "Estadísticas internacionales señalan que las personas conductoras principiantes",
  "que aquellas con más experiencia en la conducción.")
P("cap4", "¿Qué grupo de edad tiene la reacción más rápida en situaciones reales complejas?",
  ["Quienes tienen entre 35 y 50 años", "Quienes tienen entre 18 y 20 años", "Quienes superan los 70 años", "Quienes tienen 15 años"], 0,
  40, "El grupo de edad \"más rápido\" corresponde a quienes tienen entre 35 y 50 años.")
P("cap4", "La distancia de visibilidad en un cruce de vehículos que van con luces bajas no supera los:",
  ["15 o 20 metros", "70 metros", "150 metros", "5 metros"], 0,
  40, "la distancia de visibilidad en un cruce de vehículos que van con luces bajas no supera los 15 o 20 metros")
P("cap4", "¿Cuánta luz refleja la ropa oscura?",
  ["Sólo el 5%", "El 80%", "Entre un 90 y 98%", "El 50%"], 0,
  41, "La ropa oscura refleja sólo el 5% de la luz", "y los materiales reflectantes entre un 90 y 98%.")
P("cap4", "¿Qué ocurre con el campo visual a medida que aumenta la velocidad?",
  ["Se reduce", "Se amplía", "No varía", "Se duplica"], 0,
  44, "en donde el campo visual se reduce a medida que aumenta la velocidad")
P("cap4", "Se considera conducción bajo la influencia del alcohol cuando la persona presenta:",
  ["Entre 0,31 y 0,79 gramos por mil de alcohol en la sangre",
   "0,8 o más gramos por mil de alcohol en la sangre",
   "Cualquier cantidad sobre 1,5 gramos por mil",
   "Menos de 0,1 gramos por mil"], 0,
  50, "0,31 - 0,79 gramos por mil de alcohol en la sangre. 0,8 o más gramos por mil de alcohol en la sangre. Bajo la influencia del alcohol Estado de ebriedad")
P("cap4", "Se considera estado de ebriedad cuando la persona presenta:",
  ["0,8 o más gramos por mil de alcohol en la sangre",
   "0,2 gramos por mil de alcohol en la sangre",
   "Entre 0,31 y 0,79 gramos por mil",
   "Cualquier consumo de alcohol"], 0,
  50, "0,8 o más gramos por mil de alcohol en la sangre.")
P("cap4", "¿Qué sanción corresponde a conducir en estado de ebriedad?",
  ["Multas, cancelación de licencia y presidio (cárcel)",
   "Sólo una amonestación verbal",
   "Únicamente el retiro del vehículo",
   "Una multa fija sin otras consecuencias"], 0,
  50, "Sanción: multas, cancelación de licencia y presidio (cárcel).")
P("cap4", "La Ley Emilia sanciona con cárcel efectiva de al menos un año a quienes:",
  ["En estado de ebriedad generan lesiones gravísimas o la muerte a terceros",
   "Estacionan en un lugar prohibido",
   "Circulan sin revisión técnica",
   "Exceden en 5 km/h el límite de velocidad"], 0,
  51, "Una modificación legal en el año 2014, conocida como Ley Emilia", "o la muerte a terceros.")
P("cap4", "Con una alcoholemia entre 0,5 y 0,8 g/l, el riesgo de sufrir un siniestro es:",
  ["Cinco veces mayor que si no hubiera bebido",
   "El doble que si no hubiera bebido",
   "Igual que si no hubiera bebido",
   "Cincuenta veces mayor"], 0,
  50, "En cambio, si se llega a una alcoholemia entre 0,5 y 0,8 g/l", "que si no hubiera bebido.")
P("cap4", "¿Cuál es la única tasa de alcohol segura para conducir?",
  ["Cero", "0,3 g/l", "0,5 g/l", "0,79 g/l"], 0,
  51, "La única tasa de alcohol segura para conducir es \"0\".")
P("cap4", "¿A qué ritmo disminuye el alcohol en una persona promedio y sana de 70 kilos?",
  ["Entre 0,10 y 0,15 g por litro de sangre por hora",
   "1 g por litro de sangre por hora",
   "0,5 g por litro de sangre por minuto",
   "No disminuye con el tiempo"], 0,
  52, "la presencia de alcohol disminuye a razón de entre 0,10 a 0,15 g de alcohol por litro de sangre por hora")
P("cap4", "La metabolización del alcohol:",
  ["No se puede apresurar y se realiza a un ritmo constante",
   "Se acelera tomando café",
   "Se acelera con una ducha fría",
   "Se acelera haciendo ejercicio"], 0,
  52, "La metabolización no se puede apresurar.", "una ducha fría o ejercicios físicos.")
P("cap4", "¿En cuánto tiempo se detecta el alcohol en la sangre después de haber sido ingerido?",
  ["5 minutos", "1 hora", "3 horas", "30 segundos"], 0,
  52, "El alcohol se detecta en la sangre 5 minutos después de haber sido ingerido.")
P("cap4", "Conducir bajo los efectos de algunos antihistamínicos equivale al riesgo de conducir con una tasa de alcohol de:",
  ["0,5 g/l a 0,8 g/l", "0,1 g/l", "2 g/l", "0 g/l"], 0,
  60, "Se ha comprobado que el riesgo de conducir bajo los efectos", "conducir bajo la influencia del alcohol.")
P("cap4", "¿Qué porcentaje de los siniestros de tránsito se asocia directa o indirectamente al factor sueño?",
  ["Entre el 15 y el 30%", "Menos del 1%", "Cerca del 70%", "Exactamente el 50%"], 0,
  62, "Datos a nivel internacional revelan que entre el 15 y el 30% del total de los siniestros de tránsito ocurre porque el factor sueño está asociado directa o indirectamente")
P("cap4", "En viajes largos se recomienda descansar al menos:",
  ["20 a 30 minutos cada 2 horas o 200 kilómetros", "5 minutos cada 6 horas", "1 hora cada 500 kilómetros", "No es necesario descansar"], 0,
  66, "En viajes largos, descansa al menos 20 a 30 minutos cada 2 horas o 200 kilómetros de conducción, como máximo.")
P("cap4", "¿En qué horarios es especialmente favorable la aparición de somnolencia?",
  ["Entre las 3 y las 5 horas y entre las 14 y las 16 horas",
   "Sólo entre las 20 y las 22 horas",
   "Únicamente al mediodía",
   "Sólo durante la mañana temprano"], 0,
  63, "El momento del día. La madrugada, especialmente entre las 3 y las 5 horas", "aunque hayas dormido lo suficiente.")

# --- Capítulo 5 -------------------------------------------------------------
P("cap5", "¿Qué espacio lateral mínimo indica la normativa al pasar cerca de una persona ciclista?",
  ["Al menos 1,5 metros", "Al menos 0,5 metros", "Al menos 3 metros", "No hay distancia establecida"], 0,
  71, "la normativa indica que debes dejar un espacio lateral de al menos 1,5 metros")
P("cap5", "¿Cuál es el elemento de seguridad principal de las y los ciclistas?",
  ["El casco", "El chaleco reflectante", "Los guantes", "La luz trasera"], 0,
  71, "El elemento de seguridad principal de las y los ciclistas es el casco.", "en caso de atropello.")
P("cap5", "¿A qué edad comienzan las niñas y niños a actuar con seguridad en el tránsito?",
  ["Entre los 9 y 12 años", "Entre los 3 y 5 años", "A partir de los 15 años", "Desde que aprenden a caminar"], 0,
  70, "Comienzan a actuar con seguridad en el tránsito entre los 9 y 12 años de edad.")
P("cap5", "¿Hasta qué edad se desarrolla completamente la vista de las niñas y niños?",
  ["Hasta los 15 años", "Hasta los 5 años", "Hasta los 21 años", "Desde el nacimiento está desarrollada"], 0,
  70, "No tienen la vista completamente desarrollada: la vista no se desarrolla completamente hasta los 15 años de edad.")
P("cap5", "Una persona mayor puede necesitar, respecto de una persona joven, para cruzar una calle de 16 metros:",
  ["4 segundos más", "1 segundo más", "10 segundos más", "El mismo tiempo"], 0,
  69, "Una persona mayor puede necesitar 4 segundos más que una persona joven para cruzar una calle de 16 metros de ancho.")
P("cap5", "¿Puede un vehículo motorizado circular, detenerse o estacionar en una ciclovía?",
  ["No, está prohibido", "Sí, si va a baja velocidad", "Sí, sólo de noche", "Sí, si no hay ciclistas a la vista"], 0,
  72, "Recuerda que como persona conductora de un vehículo motorizado, no puedes circular, detenerte ni estacionar en las ciclovías.")
P("cap5", "¿Desde qué edad y estatura es obligatorio el Sistema de Retención Infantil según la Ley de Tránsito?",
  ["Hasta 8 años inclusive, o estatura menor o igual a 135 cm y 33 kg de peso",
   "Hasta los 3 años solamente",
   "Hasta los 15 años sin excepción",
   "Sólo para menores de 1 año"], 0,
  73, "Asimismo, desde marzo de 2017 la Ley de Tránsito obliga", "en Sistemas de Retención Infantil.")
P("cap5", "¿Cómo se sanciona no utilizar el Sistema de Retención Infantil cuando corresponde?",
  ["Como falta gravísima, con multa de 1,5 a 3 UTM y suspensión de licencia de 5 a 45 días",
   "Con una amonestación verbal",
   "Con multa de 0,1 UTM",
   "No tiene sanción"], 0,
  73, "El incumplimiento de estas medidas es sancionado como una falta gravísima", "de 5 a 45 días.")
P("cap5", "¿Dónde deben ser transportados los menores de 12 años?",
  ["En el asiento trasero, excepto en vehículos de cabina simple",
   "En el asiento delantero con cinturón",
   "En cualquier asiento indistintamente",
   "En el maletero si el vehículo es pequeño"], 0,
  73, "Se estableció la prohibición del traslado de menores de 12 años en los asientos delanteros",
  "(excepto en vehículos de cabina simple)")
P("cap5", "¿Hasta qué momento se recomienda instalar el Sistema de Retención Infantil a contramarcha?",
  ["Hasta alcanzar los límites de peso y altura del fabricante, mínimo hasta los dos años",
   "Sólo durante el primer mes de vida",
   "Hasta los 10 años",
   "No se recomienda a contramarcha"], 0,
  74, "Se recomienda que el SRI sea instalado a contramarcha", "(mínimo hasta los dos años).")

# --- Capítulo 6 -------------------------------------------------------------
P("cap6", "Si enfrentas al mismo tiempo la indicación de un carabinero y la de un semáforo, ¿cuál prevalece?",
  ["Las indicaciones de Carabineros de Chile", "La del semáforo", "La demarcación de la calzada", "La señal vertical más cercana"], 0,
  77, "En tal caso, las indicaciones dadas por Carabineros de Chile prevalecen sobre las demás.")
P("cap6", "Un carabinero visto de frente o de espalda indica:",
  ["Detención", "Autorización para avanzar", "Advertencia", "Viraje obligatorio"], 0,
  77, "Carabineros vistos de frente o de espalda: indican detención.")
P("cap6", "Aun teniendo luz verde, no debes avanzar si pasado el cruce no tienes a lo menos:",
  ["10 metros expeditos en tu pista de circulación", "3 metros expeditos", "50 metros expeditos", "1 metro expedito"], 0,
  78, "Aún teniendo luz verde, no avances si pasado el cruce no tienes a lo menos 10 metros expeditos en tu pista de circulación.")
P("cap6", "¿Qué indica la luz roja intermitente de un semáforo?",
  ["Ceda el paso", "Detención definitiva", "Prevención", "Paso libre"], 0,
  78, "Luz roja intermitente: Indica ceda el paso.", "que hagan riesgoso el cruzar.")
P("cap6", "¿Qué indica la luz amarilla intermitente?",
  ["Advierte peligro y obliga a aproximarse a velocidad reducida",
   "Indica detención obligatoria",
   "Indica paso preferente",
   "Indica que el semáforo está apagado"], 0,
  78, "Luz amarilla intermitente: Advierte peligro.", "y continuar con la debida precaución.")
P("cap6", "No respetar la indicación de la luz roja de un semáforo es una infracción:",
  ["Gravísima", "Leve", "Menos grave", "Sin clasificación"], 0,
  78, "No respetar la indicación de la luz roja de un semáforo, es una infracción gravísima a la Ley de Tránsito.")
P("cap6", "En los cruces ferroviarios, la luz blanca de las señales luminosas indica que:",
  ["No se acerca un tren, lo que no significa que se pueda pasar sin peligro",
   "Se aproxima un tren",
   "El cruce está definitivamente cerrado",
   "Se puede cruzar sin verificar nada"], 0,
  79, "en tanto que la blanca indica que no se acerca alguno", "el sistema de seguridad podría fallar.")
P("cap6", "¿Qué forma tienen por lo general las señales reglamentarias?",
  ["Forma circular o rectangular, con símbolos dentro de un círculo u orla roja",
   "Forma de rombo con fondo amarillo",
   "Forma cuadrada de color naranja",
   "Forma triangular con fondo verde"], 0,
  80, "Por lo general, estas señales tienen forma circular o rectangular", "dentro de un círculo u orla roja.")
P("cap6", "¿Qué forma y colores tienen las señales de advertencia de peligro?",
  ["Forma de rombo, fondo amarillo y símbolo negro",
   "Forma circular, fondo blanco y orla roja",
   "Forma cuadrada, fondo azul y símbolo blanco",
   "Forma octogonal, fondo rojo"], 0,
  81, "Estas tienen forma de rombo, su color de fondo es amarillo y su símbolo es negro.")
P("cap6", "Las señales transitorias, que responden a trabajos en la vía, son de color:",
  ["Naranja, salvo la primera señal que advierte los trabajos, que es amarilla",
   "Verde en todos los casos",
   "Azul en todos los casos",
   "Rojo en todos los casos"], 0,
  81, "Son de color naranja, con la excepción de la primera señal que advierte sobre los trabajos, la que es de color amarillo.")
P("cap6", "Una línea longitudinal continua indica que:",
  ["No existen condiciones de seguridad para que pueda ser traspasada",
   "Se puede traspasar libremente",
   "Sólo la pueden traspasar los buses",
   "Marca una zona de estacionamiento"], 0,
  82, "Las líneas longitudinales continuas", "para que pueda ser traspasada.")
P("cap6", "Cuando la línea longitudinal es mixta (segmentada y continua), sólo puede ser traspasada por:",
  ["Los vehículos que circulan por el lado en que esta es segmentada",
   "Todos los vehículos",
   "Los vehículos que circulan por el lado continuo",
   "Ningún vehículo"], 0,
  82, "En estos casos, sólo puede ser traspasada por los vehículos que circulan por el lado en que esta es segmentada.")
P("cap6", "¿Qué señala una franja amarilla continua pintada al borde de la calzada o en la solera en áreas urbanas?",
  ["La prohibición de estacionar a lo largo de esta",
   "Una zona de carga y descarga",
   "El inicio de una ciclovía",
   "Una zona de tránsito calmado"], 0,
  82, "en áreas urbanas suele demarcarse al borde de la calzada", "la prohibición de estacionar a lo largo de esta")
P("cap6", "Si la línea de detención no está pintada en un paso de cebra o cruce semaforizado, se ubica imaginariamente:",
  ["A no menos de un metro antes de éstos", "Justo sobre el paso peatonal", "A cinco metros antes", "No existe línea de detención"], 0,
  83, "Aunque esta no esté pintada, imaginariamente se ubica a no menos de un metro antes de éstos.")
P("cap6", "Cuando te aproximas a un cruce sin semáforo ni señales PARE o Ceda el Paso, debes dar preferencia a:",
  ["Los vehículos que se aproximan por la otra vía desde tu derecha",
   "Los vehículos que vienen desde tu izquierda",
   "Los vehículos de mayor tamaño",
   "Nadie, tienes preferencia siempre"], 0,
  84, "siempre tienes que dar preferencia a los vehículos que se aproximan al cruce por la otra vía desde tu derecha.")
P("cap6", "Al momento de virar, la persona conductora:",
  ["Carece de toda preferencia", "Tiene preferencia sobre los peatones", "Tiene preferencia sobre los ciclistas", "Mantiene su preferencia habitual"], 0,
  84, "Al momento de virar no tienes preferencia", "en los cruces o pasos reglamentarios.")
P("cap6", "Al enfrentar una señal PARE debes:",
  ["Detener tu vehículo y permitir el paso de quienes circulan por la otra vía",
   "Reducir la velocidad sin detenerte",
   "Tocar la bocina y avanzar",
   "Avanzar si no ves vehículos a lo lejos"], 0,
  84, "Al enfrentar la señal PARE debes detener tu vehículo", "cuando no exista posibilidad alguna de siniestro.")
P("cap6", "Al incorporarte a una rotonda o minirrotonda debes:",
  ["Ceder el paso a los vehículos que circulan por ella",
   "Ingresar sin detenerte porque tienes preferencia",
   "Detenerte siempre por 10 segundos",
   "Ingresar por la pista izquierda"], 0,
  84, "Al incorporarte a una zona de tránsito en rotación", "debes ceder el paso a los vehículos que circulan por ella.")
P("cap6", "Ceder el paso significa que quien tiene la preferencia:",
  ["No debe verse en la obligación de modificar su trayectoria ni su velocidad",
   "Debe reducir su velocidad para facilitar el cruce",
   "Debe detenerse completamente",
   "Debe encender sus luces intermitentes"], 0,
  85, "ceder el paso significa que quien tiene la preferencia en el uso de la vía no debe verse en la obligación de modificar su trayectoria ni su velocidad")
P("cap6", "Ante la aproximación de un vehículo de emergencia con señales luminosas y/o acústicas debes:",
  ["Cederles el derecho a vía, desplazándote hacia un lado y deteniéndote si es necesario",
   "Acelerar para no entorpecer",
   "Mantener tu velocidad y trayectoria",
   "Tocar la bocina para advertir a otros"], 0,
  85, "Vehículos de emergencia: Ante la aproximación de un vehículo de emergencia", "si se trata de un cruce.")
P("cap6", "Cuál es la secuencia correcta para efectuar un cambio de pista:",
  ["Espejo - señalización - maniobra", "Señalización - maniobra - espejo", "Maniobra - espejo - señalización", "Bocina - maniobra - espejo"], 0,
  86, "Recuerda siempre la secuencia espejo - señalización - maniobra.")
P("cap6", "El brazo izquierdo extendido horizontalmente indica:",
  ["Viraje a la izquierda", "Viraje a la derecha", "Disminución de velocidad", "Detención de emergencia"], 0,
  86, "Brazo extendido horizontalmente indica viraje a la izquierda.")
P("cap6", "El brazo izquierdo en ángulo recto hacia arriba indica:",
  ["Viraje a la derecha", "Viraje a la izquierda", "Detención", "Adelantamiento"], 0,
  86, "Brazo en ángulo recto hacia arriba indica viraje a la derecha.")
P("cap6", "El brazo extendido hacia abajo indica:",
  ["Disminución de velocidad o detención", "Viraje a la izquierda", "Viraje a la derecha", "Autorización para adelantar"], 0,
  86, "Brazo extendido hacia abajo indica disminución de velocidad o detención.")
P("cap6", "¿Dónde nunca debes utilizar la bocina?",
  ["En un túnel, ni a la entrada o salida de este", "En una avenida", "En una rotonda", "En un estacionamiento"], 0,
  87, "Nunca la utilices en un túnel, ni a la entrada o salida de este.")
P("cap6", "En carretera, la regla general de distancia con el vehículo de adelante indica mantener:",
  ["Una distancia en metros equivalente a lo que el velocímetro indica en kilómetros",
   "Siempre 10 metros",
   "El doble de la longitud del vehículo",
   "Un cuarto de la velocidad en metros"], 0,
  87, "Una regla aplicable siempre en carreteras dice que se debe mantener una distancia medida en metros equivalente a lo que el velocímetro te indica en kilómetros.")
P("cap6", "En el tránsito urbano, la distancia con el vehículo de adelante puede reducirse a:",
  ["La mitad", "Un cuarto", "El doble", "Cero"], 0,
  87, "En el tránsito urbano, dicha distancia puede reducirse a la mitad.")
P("cap6", "¿En qué consiste la Regla de los Tres Segundos?",
  ["Fijar un punto y comprobar que pasas por él después de contar mil uno, mil dos, mil tres",
   "Esperar tres segundos antes de arrancar",
   "Detenerse tres segundos en cada señal PARE",
   "Mantener tres metros de distancia"], 0,
  88, "Para usarla, fija tu mirada en un punto", "Disminuye la presión sobre el acelerador.")
P("cap6", "Con cuánta anticipación mínima debes señalizar tu intención de virar:",
  ["A lo menos 30 metros antes", "A lo menos 3 metros antes", "A lo menos 100 metros antes", "No es necesario señalizar"], 0,
  91, "Debes señalizar tu intención de virar con una anticipación suficiente: a lo menos 30 metros antes.")
P("cap6", "¿Cuál es la velocidad máxima permitida en zonas urbanas?",
  ["50 km/h", "60 km/h", "40 km/h", "70 km/h"], 0,
  96, "En zonas urbanas, la velocidad máxima permitida es de 50 km/h.")
P("cap6", "En zonas no urbanas con una sola pista por sentido, la velocidad máxima para vehículos livianos es:",
  ["100 km/h", "120 km/h", "80 km/h", "140 km/h"], 0,
  96, "En zonas no urbanas, y cuando la calzada tiene sólo una pista por sentido", "es de 100 km/h.")
P("cap6", "En zonas no urbanas con 2 o más pistas en un mismo sentido, el límite para vehículos livianos aumenta a:",
  ["120 km/h", "100 km/h", "140 km/h", "90 km/h"], 0,
  96, "Cuando hay 2 o más pistas en un mismo sentido, este límite aumenta a 120 km/h.")
P("cap6", "Los buses, camiones y vehículos de transporte escolar no deben circular a más de:",
  ["90 km/h", "100 km/h", "120 km/h", "80 km/h"], 0,
  96, "En todo caso, los buses, camiones y vehículos de transporte escolar no deben circular a más de 90 km/h")
P("cap6", "¿A qué velocidad máxima debes circular por las afueras de un colegio en horario de entrada y salida de clases?",
  ["No más de 30 km/h", "No más de 50 km/h", "No más de 20 km/h", "No hay límite especial"], 0,
  97, "Debes reducir tu velocidad a no más de 30 km/h cuando circules por las afueras de un colegio")
P("cap6", "A 50 km/h, con pavimento bueno y seco, ¿cuántos metros se necesitan para detenerse?",
  ["Unos 25 metros", "Unos 80 metros", "Unos 10 metros", "Unos 100 metros"], 0,
  96, "A 50 km/h se necesitan unos 25 metros para detenerse si el pavimento es bueno y está seco.")
P("cap6", "A 100 km/h, con buen pavimento seco, ¿cuántos metros se requieren para detenerse?",
  ["Unos 80 metros", "Unos 25 metros", "Unos 200 metros", "Unos 50 metros"], 0,
  96, "Si aumentas la velocidad a 100 km/h, requerirás unos 80 metros.")
P("cap6", "Si dos vehículos circulan en sentido contrario, ¿a qué velocidad se aproximan entre sí?",
  ["A una velocidad igual a la suma de las velocidades de cada uno",
   "A la velocidad del más rápido",
   "A la mitad de la suma de ambas",
   "A la velocidad del más lento"], 0,
  98, "Si dos vehículos circulan en sentido contrario, éstos se aproximan a una velocidad igual a la suma de las velocidades de cada uno.")
P("cap6", "Los adelantamientos deben efectuarse siempre:",
  ["Por la izquierda", "Por la derecha", "Por la berma", "Por donde haya más espacio"], 0,
  103, "Los adelantamientos deben efectuarse siempre por la izquierda.")
P("cap6", "No debes adelantar traspasando el eje de la calzada al aproximarte a un puente, viaducto, túnel o cruce ferroviario desde una distancia mínima de:",
  ["200 metros", "50 metros", "20 metros", "500 metros"], 0,
  103, "Circules por un puente, viaducto, túnel o cruce ferroviario o al aproximarte a cualquiera de estos lugares desde una distancia mínima de 200 metros.")
P("cap6", "¿En qué dos situaciones puedes adelantar a un vehículo por la derecha?",
  ["Cuando el vehículo alcanzado va a virar a la izquierda, y en vía urbana con tres o más pistas en un mismo sentido",
   "Siempre que la berma esté libre",
   "Cuando el vehículo de adelante circula lento",
   "Nunca se puede adelantar por la derecha"], 0,
  103, "Solo puedes adelantar a un vehículo por la derecha en las siguientes dos situaciones",
  "con tres o más pistas de circulación con un mismo sentido del tránsito.")
P("cap6", "¿Qué es una maniobra de sobrepaso?",
  ["Situarse adelante de otro vehículo sin invadir la pista del sentido contrario",
   "Adelantar traspasando el eje de la calzada",
   "Adelantar utilizando la berma",
   "Cambiar de pista en una intersección"], 0,
  103, "Así, se entiende que sobrepasas a otro vehículo cuando te sitúas adelante de él sin invadir la pista del sentido contrario.")
P("cap6", "Al estacionar en forma paralela a la cuneta, debes hacerlo a no más de:",
  ["30 centímetros de ella", "1 metro de ella", "10 centímetros de ella", "2 metros de ella"], 0,
  104, "debes hacerlo en forma paralela a la cuneta, a no más de 30 centímetros de ella")
P("cap6", "¿Qué distancia mínima debes dejar respecto de otros vehículos estacionados?",
  ["60 centímetros", "10 centímetros", "2 metros", "No hay distancia mínima"], 0,
  104, "dejando una distancia mínima de 60 centímetros respecto de otros vehículos estacionados.")
P("cap6", "¿A qué distancia mínima de un grifo para incendios no debes estacionar?",
  ["5 metros", "1 metro", "20 metros", "50 metros"], 0,
  105, "A menos de 5 metros de un grifo para incendios.")
P("cap6", "¿A qué distancia mínima de una señal PARE o Ceda el Paso no debes estacionar?",
  ["10 metros", "3 metros", "30 metros", "1 metro"], 0,
  105, "A menos de 10 metros de una señal PARE, Ceda el Paso y señales de advertencia de peligro")
P("cap6", "¿A qué distancia mínima de una esquina no debes estacionar?",
  ["10 metros", "5 metros", "20 metros", "2 metros"], 0,
  106, "A menos de 10 metros de una esquina.")
P("cap6", "¿A qué distancia mínima de una parada de locomoción colectiva no debes estacionar?",
  ["20 metros", "5 metros", "10 metros", "50 metros"], 0,
  106, "A menos de 20 metros de una señal que indique una parada de vehículos de locomoción colectiva.")
P("cap6", "¿A qué distancia mínima de un cruce ferroviario a nivel no debes estacionar?",
  ["20 metros", "5 metros", "100 metros", "2 metros"], 0,
  106, "A menos de 20 metros de un cruce ferroviario a nivel.")
P("cap6", "¿A qué distancia de las puertas de iglesias, establecimientos educacionales, hoteles y salas de espectáculos no debes estacionar durante las horas de afluencia de público?",
  ["A menos de 3 metros", "A menos de 10 metros", "A menos de 30 metros", "No hay restricción"], 0,
  105, "A menos de 3 metros de las puertas de iglesias, establecimientos educacionales")
P("cap6", "¿De qué color debe ser el chaleco de alta visibilidad y qué ancho mínimo deben tener sus bandas retrorreflectantes?",
  ["Amarillo, con bandas de ancho no inferior a 50 milímetros",
   "Naranja, con bandas de 10 milímetros",
   "Verde, con bandas de 100 milímetros",
   "Blanco, sin bandas"], 0,
  106, "Este debe ser de color amarillo y contar con bandas de material retrorreflectante de un ancho no inferior a 50 milímetros.")
P("cap6", "¿En qué casos puedes conducir marcha atrás?",
  ["Para mantener la libre circulación, incorporarte a la circulación y estacionar",
   "En cualquier momento que sea cómodo",
   "Sólo en autopistas",
   "Sólo de noche"], 0,
  106, "No debes conducir marcha atrás, a menos que ello sea indispensable", "Para estacionar.")
P("cap6", "Un tren que marcha a 100 km/h necesita para detenerse:",
  ["Entre 800 y 1.000 metros", "Entre 80 y 100 metros", "Menos de 200 metros", "Cerca de 5 kilómetros"], 0,
  107, "Un tren que marcha a 100 km/h necesitará entre 800 a 1.000 metros para detenerse.")
P("cap6", "Si ya has comenzado a cruzar una vía férrea y se activan las señales luminosas o acústicas, debes:",
  ["No detenerte", "Detenerte de inmediato", "Retroceder rápidamente", "Encender las luces intermitentes y esperar"], 0,
  107, "Si ya has comenzado a cruzar y se activan las señales luminosas o acústicas", "no te detengas.")
P("cap6", "Si tu vehículo se descompone en un cruce ferroviario, lo primero que debes hacer es:",
  ["Hacer salir a todas las personas del vehículo",
   "Intentar repararlo en el lugar",
   "Esperar dentro del vehículo",
   "Empujar el vehículo hacia la vía férrea"], 0,
  107, "Haz salir a todas las personas del vehículo.")
P("cap6", "¿Cuál es la distancia de seguridad adecuada al detenerte detrás de otro vehículo esperando la luz verde?",
  ["La que te permite ver los neumáticos traseros del vehículo de delante",
   "Un metro exacto",
   "La longitud de dos vehículos",
   "No es necesario mantener distancia"], 0,
  105, "Se estima que esta es adecuada si puedes ver los neumáticos traseros del vehículo de delante.")

# --- Capítulo 7 -------------------------------------------------------------
P("cap7", "¿Desde y hasta qué momento deben circular obligatoriamente los vehículos con sus luces encendidas?",
  ["Desde media hora después de la puesta de sol hasta media hora antes de su salida",
   "Sólo entre las 22 y las 6 horas",
   "Únicamente cuando llueve",
   "Sólo en carretera"], 0,
  110, "Para poder ver y ser visible, desde media hora después de la puesta de sol", "en los caminos y vías rurales.")
P("cap7", "¿Qué luces se deben usar en vías urbanas y cuáles en caminos y vías rurales?",
  ["Luces bajas en vías urbanas y luces altas en caminos y vías rurales",
   "Luces altas en vías urbanas y bajas en rurales",
   "Luces de estacionamiento en ambos casos",
   "Sólo luces neblineras"], 0,
  110, "los vehículos deben circular obligatoriamente con sus luces encendidas: luces bajas en las vías urbanas y luces altas en los caminos y vías rurales.")
P("cap7", "¿Se puede circular con las luces de estacionamiento encendidas?",
  ["No, en ningún caso", "Sí, en zonas urbanas", "Sí, cuando hay niebla", "Sí, durante el día"], 0,
  110, "En ningún caso podrás circular con las luces de estacionamiento encendidas.")
P("cap7", "¿Es necesario bajar las luces al cruzarse con peatones?",
  ["No es necesario", "Sí, siempre", "Sólo si van por la calzada", "Sólo de noche"], 0,
  111, "No es necesario que bajes las luces cuando te cruces con peatones.")
P("cap7", "¿De qué color son las luces de retroceso de un vehículo?",
  ["Blancas", "Rojas", "Amarillas", "Azules"], 0,
  113, "con excepción de las de retroceso, que son blancas")
P("cap7", "La Licencia de Conducir Clase B permite conducir un automóvil con un remolque ligero siempre que el peso total no supere:",
  ["3.500 kilogramos", "750 kilogramos", "10.000 kilogramos", "1.000 kilogramos"], 0,
  114, "La Licencia de Conducir Clase B te permite conducir tu automóvil con un remolque ligero", "no supere los 3.500 kilogramos.")
P("cap7", "¿Desde qué capacidad de carga deben poseer frenos los remolques?",
  ["Superior a 750 kilogramos", "Superior a 100 kilogramos", "Superior a 3.500 kilogramos", "Siempre, sin importar la carga"], 0,
  115, "Cuando los remolques tienen capacidad de carga superior a 750 kilogramos, deben poseer frenos")
P("cap7", "Al ingresar a una autopista por la pista de aceleración, la prioridad la tienen:",
  ["Los vehículos que circulan por la autopista", "Los vehículos que ingresan", "Los vehículos más lentos", "Los vehículos de carga"], 0,
  116, "Los vehículos que circulan por la autopista tienen la prioridad.")
P("cap7", "¿En qué casos puedes detenerte en una autopista?",
  ["Sólo si se produce una emergencia o lo solicita Carabineros",
   "Cuando necesites descansar",
   "Para recoger pasajeros",
   "Cuando quieras revisar el mapa"], 0,
  117, "No te detengas en una autopista, a menos que:", "Te lo solicite Carabineros.")
P("cap7", "Si tu vehículo se detiene en la berma de una autopista, debes salir:",
  ["Por la puerta derecha, asegurándote de que los pasajeros hagan lo mismo",
   "Por la puerta izquierda",
   "Sólo cuando llegue Carabineros",
   "Empujando el vehículo hacia la calzada"], 0,
  117, "Salir del vehículo por la puerta derecha asegurándote que tus pasajeros hagan lo mismo.")
P("cap7", "Si no puedes llegar con tu vehículo a la berma en una autopista, NO debes:",
  ["Colocar un triángulo u otro dispositivo reflectante en la calzada ni realizar reparaciones",
   "Encender las luces destellantes de advertencia",
   "Permanecer con el cinturón puesto",
   "Usar el chaleco reflectante si sales del vehículo"], 0,
  118, "No intentes colocar un triángulo u otro dispositivo reflectante en la calzada de la autopista, ni intentes realizar la más mínima reparación.")
P("cap7", "Al circular por un túnel, si se produce un atochamiento y el vehículo queda detenido, debes:",
  ["Encender las luces de emergencia y apagar el motor",
   "Mantener el motor encendido y acelerar",
   "Bajar del vehículo y caminar",
   "Tocar la bocina de forma continua"], 0,
  119, "Si se produce un atochamiento, enciende tus luces de emergencia inmediatamente", "recuerda apagar el motor de tu vehículo.")
P("cap7", "Al conducir con lluvia, la distancia de frenado será:",
  ["A lo menos el doble a la que sería en condiciones ideales",
   "La misma que en seco",
   "La mitad que en seco",
   "Diez veces mayor"], 0,
  121, "Tu distancia de frenado será a lo menos el doble a la que sería en condiciones ideales")
P("cap7", "¿Qué es el aquaplaning o hidroplaning?",
  ["Cuando una capa de agua se interpone entre la calzada y los neumáticos, que pierden adherencia y contacto",
   "El bloqueo de las ruedas al frenar",
   "El derrape en curvas cerradas",
   "La condensación en el parabrisas"], 0,
  121, "Cuando la lluvia es muy intensa, sobre la calzada se forma una película o capa de agua",
  "no obedeciéndole la dirección ni los frenos.")
P("cap7", "¿Cuál es el mejor consejo para evitar el aquaplaning?",
  ["Moderar la velocidad", "Frenar con fuerza", "Acelerar para atravesar el agua", "Usar luces altas"], 0,
  121, "Por esta razón, para evitar el \"aquaplaning\", el mejor consejo es moderar la velocidad")
P("cap7", "Si el vehículo comienza a patinar al frenar con lluvia y no tiene ABS, debes:",
  ["Soltar el freno completamente para recuperar la tracción de las ruedas",
   "Frenar aún con más fuerza",
   "Accionar el freno de mano",
   "Girar el volante bruscamente"], 0,
  121, "En caso de que el vehículo comience a patinar, suelta el freno completamente para recuperar la tracción de las ruedas.")
P("cap7", "Cuando la calzada está helada, la distancia de frenado puede aumentar hasta:",
  ["10 veces por encima de lo normal", "2 veces", "50 veces", "No aumenta"], 0,
  124, "cuando la calzada está helada, la distancia de frenado puede aumentar hasta 10 veces por encima de lo normal")
P("cap7", "Con niebla, ¿qué luces conviene mantener encendidas?",
  ["Las luces bajas", "Las luces altas", "Sólo las de estacionamiento", "Ninguna, para no deslumbrar"], 0,
  125, "Mantén encendidas tus luces bajas.", "se ven más y mejor.")
P("cap7", "¿Por qué no conviene usar luces altas con niebla?",
  ["Porque las gotas de agua reflejan la luz como un espejo",
   "Porque consumen más combustible",
   "Porque están prohibidas de noche",
   "Porque encandilan a los peatones únicamente"], 0,
  125, "No conviene utilizar luces altas, porque, al proyectarse paralelas sobre la calzada", "reflejan la luz como un espejo.")
P("cap7", "Ante viento fuerte lateral, ¿qué debes hacer con el volante?",
  ["Sujetarlo con firmeza y girarlo contra el viento",
   "Soltarlo para que el vehículo se estabilice solo",
   "Girarlo en el mismo sentido del viento",
   "Frenar bruscamente"], 0,
  125, "Corregir las desviaciones para corregir la trayectoria: Para ello, sujeta el volante con firmeza y gíralo contra el viento.")
P("cap7", "Al conducir con nieve, ¿qué marcha conviene usar?",
  ["La marcha más alta que razonablemente sea posible emplear",
   "Siempre la primera marcha",
   "Punto neutro en bajadas",
   "La marcha más baja disponible"], 0,
  123, "Usa la marcha más alta que razonablemente sea posible emplear", "Evita los cambios de marcha.")

# --- Capítulo 8 -------------------------------------------------------------
P("cap8", "Aplicar técnicas de Conducción Eficiente permite reducir el consumo de combustible entre:",
  ["Un 10 y un 15%", "Un 1 y un 2%", "Un 40 y un 60%", "No genera reducción"], 0,
  127, "han demostrado que aplicar técnicas en Conducción Eficiente permite reducir entre un 10 y un 15% el consumo de combustible.")
P("cap8", "Llevar un portaequipajes o bulto en el techo puede incrementar el consumo en carretera:",
  ["Por sobre un 20%", "En un 1%", "En un 50%", "No lo incrementa"], 0,
  129, "Si tienes un portaequipajes o bulto en el techo, el consumo se puede incrementar por sobre un 20% en carretera")
P("cap8", "Una reducción de 5 PSI del nivel óptimo de aire en los neumáticos puede incrementar el consumo en:",
  ["Un 3%", "Un 30%", "Un 0,1%", "No lo incrementa"], 0,
  129, "Se estima que una reducción en 5 PSI del nivel óptimo de aire en los neumáticos puede incrementar el consumo de combustible en un 3%")
P("cap8", "¿Cada cuánto se recomienda revisar la presión de los neumáticos como mínimo?",
  ["Al menos cada dos semanas", "Cada dos años", "Una vez al mes como máximo", "Sólo antes de un viaje largo"], 0,
  129, "en la frecuencia descrita por el fabricante en el manual del vehículo, o al menos cada dos semanas")
P("cap8", "¿A partir de qué tiempo de detención es más económico apagar el motor?",
  ["En cualquier detención mayor a un minuto", "Después de cinco minutos", "Después de media hora", "Nunca conviene apagarlo"], 0,
  133, "como regla general, en cualquier detención mayor a un minuto, es más económico apagar el motor")
P("cap8", "Un filtro de aire sucio puede llegar a perjudicar el rendimiento en:",
  ["Un 1,5%", "Un 15%", "Un 0,01%", "No lo afecta"], 0,
  130, "Un filtro de aire sucio puede llegar a perjudicar en un 1,5% el rendimiento")
P("cap8", "¿Se debe pisar el acelerador al encender el motor?",
  ["No, sólo provoca un incremento en el consumo",
   "Sí, siempre a fondo",
   "Sí, en vehículos modernos",
   "Sólo en invierno"], 0,
  130, "Cuando enciendas el motor, prefiere no pisar el acelerador, pues tal acción sólo provoca un incremento en el consumo.")

# --- Capítulo 9 -------------------------------------------------------------
P("cap9", "Toda persona que participe en un siniestro con personas lesionadas o muertas está obligada a:",
  ["Detener su marcha, prestar la ayuda posible y dar cuenta a la autoridad policial más cercana",
   "Retirarse del lugar para no entorpecer",
   "Esperar a su compañía de seguros antes de actuar",
   "Sólo dar aviso si tuvo la culpa"], 0,
  136, "Toda persona, con culpa o sin ella, que participe en un siniestro de tránsito", "dar cuenta a la autoridad policial más cercana.")
P("cap9", "¿Cuáles son los números de emergencia que debes llamar ante un siniestro?",
  ["SAMU/ambulancia 131, Bomberos 132 y Carabineros 133",
   "Ambulancia 130, Bomberos 134 y Carabineros 135",
   "Sólo el 133",
   "El 911 en todos los casos"], 0,
  136, "asegúrate de llamar al SAMU/ambulancia (131), Bomberos (132) y Carabineros (133) lo más pronto posible")
P("cap9", "Si la persona afectada es motociclista o ciclista con casco, debes:",
  ["No quitárselo nunca, porque podrías provocar una lesión en la columna cervical",
   "Quitárselo de inmediato para que respire",
   "Quitárselo sólo si está inconsciente",
   "Aflojarlo y luego retirarlo"], 0,
  137, "Si la persona afectada es motociclista o ciclista con casco, no debes quitárselo nunca", "en la columna cervical.")
P("cap9", "¿Qué significa la letra X de la secuencia XABCDE de primeros auxilios?",
  ["Control de hemorragias graves", "Examen de conciencia", "Extracción del lesionado", "Exposición de heridas"], 0,
  137, "X: Control de hemorragias graves")
P("cap9", "En la secuencia XABCDE, la letra D corresponde a:",
  ["Déficit de conciencia", "Detención cardíaca", "Descompresión", "Desplazamiento del lesionado"], 0,
  138, "D: Déficit de conciencia")
P("cap9", "¿Qué documentos debe portar un vehículo motorizado para circular?",
  ["Placa patente, permiso de circulación y certificado del Seguro Obligatorio de Accidentes Personales",
   "Sólo la placa patente",
   "Sólo la licencia de conducir",
   "Únicamente la revisión técnica"], 0,
  139, "Los vehículos motorizados no pueden circular sin su placa patente", "un Seguro Obligatorio de Accidentes Personales.")
P("cap9", "¿Qué cubre el Seguro Obligatorio de Accidentes Personales (SOAP)?",
  ["Los riesgos de muerte y lesiones corporales, independientemente de quién sea culpable",
   "Únicamente los daños materiales del vehículo",
   "Sólo a la persona conductora",
   "Sólo si la persona conductora no tuvo la culpa"], 0,
  139, "El seguro obligatorio cubre los riesgos de muerte y lesiones corporales", "ocasionado por un vehículo motorizado.")
P("cap9", "¿Qué prohíbe la Ley No Chat?",
  ["Conducir manipulando un dispositivo de telefonía móvil u otro artefacto electrónico no incorporado de fábrica",
   "Conversar con los pasajeros",
   "Escuchar radio mientras se conduce",
   "Usar el sistema de manos libres"], 0,
  141, "La Ley No Chat prohíbe la conducción de un vehículo (incluyendo a los ciclos) manipulando un dispositivo de telefonía móvil",
  "manipulación de un GPS, etc.")
P("cap9", "Según la Ley No Chat, ¿se puede manipular el celular detenido en una luz roja o en un taco?",
  ["No, tampoco en esos momentos", "Sí, si el vehículo está detenido", "Sí, sólo por menos de 5 segundos", "Sí, si es para contestar una llamada"], 0,
  141, "No se puede manipular, esto es, operar con una o ambas manos, un celular", "en una señal \"PARE\", etc.")
P("cap9", "¿Qué suspensión de licencia corresponde a la conducción bajo la influencia del alcohol?",
  ["3 meses", "2 años", "5 días", "6 meses"], 0,
  142, "3 meses", extra=0)
P("cap9", "Una persona de 17 años con Licencia Clase B debe conducir acompañada, en el asiento delantero, por alguien con licencia de:",
  ["No menos de 5 años de antigüedad", "No menos de 1 año de antigüedad", "Cualquier antigüedad", "No menos de 10 años de antigüedad"], 0,
  142, "Esta debe tener una Licencia de Conducir que la habilite", "de no menos de 5 años de antigüedad.")
P("cap9", "¿Por acumulación de cuántas infracciones gravísimas o graves en doce meses se suspende la licencia?",
  ["Dos", "Cinco", "Diez", "Una"], 0,
  143, "una licencia es suspendida por la acumulación de dos infracciones gravísimas o graves en un período de doce meses.")
P("cap9", "Exceder entre 20 y 60 kilómetros por hora el límite de velocidad máxima es una infracción:",
  ["Gravísima", "Grave", "Menos grave", "Leve"], 0,
  143, "Exceder entre 20 y 60 kilómetros por hora el límite de velocidad máxima.")
P("cap9", "Conducir sin usar el cinturón de seguridad, o sin que otros pasajeros lo usen debiendo hacerlo, es una infracción:",
  ["Grave", "Leve", "Gravísima", "Menos grave"], 0,
  143, "Conducir sin usar el cinturón de seguridad, o sin que otros pasajeros lo usen, debiendo hacerlo.")
P("cap9", "Exceder hasta en 10 kilómetros por hora el límite máximo de velocidad es una infracción:",
  ["Menos grave", "Gravísima", "Grave", "No es infracción"], 0,
  145, "Exceder hasta en 10 kilómetros por hora el límite máximo de velocidad.")
P("cap9", "En un vehículo CON frenos ABS, ante una frenada fuerte debes:",
  ["Pisar enérgicamente el pedal de freno manteniendo la máxima presión hasta el final",
   "Bombear el pedal de freno",
   "Reducir progresivamente la fuerza sobre el pedal",
   "Usar sólo el freno de mano"], 0,
  145, "Debes pisar enérgicamente el pedal de freno, manteniendo la máxima presión hasta el final.")
P("cap9", "En un vehículo SIN frenos ABS, ante una frenada fuerte debes:",
  ["Pisar enérgicamente el pedal reduciendo la fuerza de forma progresiva al disminuir la velocidad",
   "Mantener la máxima presión hasta el final",
   "Soltar el freno por completo",
   "Girar el volante para perder velocidad"], 0,
  145, "Debes pisar enérgicamente el pedal de freno, reduciendo la fuerza de forma progresiva a medida que va disminuyendo la velocidad.")
P("cap9", "Ante una falla total de frenos, ¿cuál es una de las maniobras recomendadas?",
  ["Soltar el acelerador y reducir a cambios más bajos para que el motor frene el vehículo",
   "Apagar el motor y soltar el volante",
   "Acelerar para buscar una subida",
   "Abrir las puertas para saltar"], 0,
  146, "Suelta el acelerador y reduce a cambios más bajos tan pronto te sea posible", "el motor frenará a tu vehículo.")
P("cap9", "Si tu vehículo emite humo muy negro por el tubo de escape, es probable que:",
  ["El filtro de aire esté sucio", "Falte líquido de frenos", "La batería esté descargada", "Los neumáticos estén desinflados"], 0,
  147, "Debes saber que si tu vehículo está emitiendo humo muy negro por el tubo de escape, es probable que el filtro de aire esté sucio.")
P("cap9", "¿Qué contaminante emitido por los vehículos provoca lesiones en el sistema nervioso central?",
  ["El plomo", "El dióxido de carbono", "El vapor de agua", "El oxígeno"], 0,
  147, "Plomo: Es un metal pesado que provoca lesiones en el sistema nervioso central.")

# --- Anexo 2 · Glosario -----------------------------------------------------
P("anexo2", "Según la Ley de Tránsito, ¿qué es la berma?",
  ["Faja lateral, pavimentada o no, adyacente a la calzada de un camino",
   "La parte de la vía destinada al uso de peatones",
   "La línea que separa dos sentidos de circulación",
   "El área común de dos calzadas que se cruzan"], 0,
  162, "Berma: Faja lateral, pavimentada o no, adyacente a la calzada de un camino.")
P("anexo2", "¿Qué es la calzada?",
  ["Parte de una vía destinada al uso de vehículos y animales",
   "Parte de una vía destinada al uso de peatones",
   "La franja de seguridad lateral de un camino",
   "El espacio exclusivo para ciclos"], 0,
  162, "Calzada: Parte de una vía destinada al uso de vehículos y animales.")
P("anexo2", "¿Qué es la acera?",
  ["Parte de una vía destinada al uso de peatones",
   "Parte de una vía destinada al uso de vehículos",
   "La zona de estacionamiento",
   "El eje de la calzada"], 0,
  162, "Acera: Parte de una vía destinada al uso de peatones.")
P("anexo2", "Un ciclo con motor auxiliar eléctrico se considera vehículo no motorizado si su potencia nominal continua máxima es de:",
  ["250 watts, con alimentación reducida o interrumpida a los 25 km/h",
   "500 watts, sin límite de velocidad",
   "1.000 watts, con corte a los 45 km/h",
   "100 watts, con corte a los 10 km/h"], 0,
  162, "de una potencia nominal continua máxima de 250 watts", "para los efectos de la ley como vehículos no motorizados.")
P("anexo2", "¿Qué es un cruce regulado?",
  ["Cruce donde existe un semáforo funcionando normalmente, excluyendo la intermitencia, o donde está Carabineros dirigiendo el tránsito",
   "Cualquier cruce con señal PARE",
   "Un cruce con demarcación de paso de cebra",
   "Un cruce ferroviario con barreras"], 0,
  162, "Cruce regulado: Cruce en que existe un semáforo funcionando normalmente", "o donde está Carabineros dirigiendo el tránsito.")
P("anexo2", "¿Qué es la luz baja según el glosario?",
  ["Luz cuya potencia permite visualizar obstáculos a una distancia no inferior a 50 metros",
   "Luz que permite ver a no menos de 150 metros",
   "Luz intermitente de advertencia",
   "Luz que identifica un vehículo estacionado"], 0,
  163, "Luz baja: Luz proyectada por los focos delanteros del vehículo", "a una distancia no inferior a 50 metros.")
P("anexo2", "¿Qué es la luz alta según el glosario?",
  ["Luz cuya potencia permite visualizar obstáculos a una distancia no inferior a 150 metros",
   "Luz que permite ver a no menos de 50 metros",
   "Luz de niebla delantera",
   "Luz de retroceso"], 0,
  163, "Luz alta: Luz proyectada por los focos delanteros del vehículo en forma paralela a la calzada", "a una distancia no inferior a 150 metros.")
P("anexo2", "¿Qué es una Zona de Tránsito Calmado?",
  ["Vías urbanas con velocidades máximas de 40, 30 o 20 km/h",
   "Vías rurales sin señalización",
   "Autopistas con peaje electrónico",
   "Zonas exclusivas para buses"], 0,
  165, "Zona de Tránsito Calmado: Vía o conjunto de vías emplazadas en zonas urbanas", "pudiendo estas ser de 40 km/h, 30 km/h o 20 km/h.")
P("anexo2", "¿Qué es un vehículo de emergencia?",
  ["El perteneciente a Carabineros de Chile e Investigaciones, al Cuerpo de Bomberos y las ambulancias autorizadas",
   "Cualquier vehículo con luces intermitentes",
   "Los vehículos de transporte escolar",
   "Los vehículos de servicios municipales"], 0,
  164, "Vehículo de emergencia: El perteneciente a Carabineros de Chile e Investigaciones", "permiso otorgado por la autoridad competente.")
P("anexo2", "¿Qué capacidad de carga máxima puede tener un triciclo motorizado de carga?",
  ["300 kilogramos", "750 kilogramos", "1.000 kilogramos", "100 kilogramos"], 0,
  164, "La capacidad de carga de estos vehículos no podrá superar los 300 kilogramos de peso.")

# --- Anexo 3 · Proceso de licencia -----------------------------------------
P("anexo3", "¿Dónde debe obtenerse la Licencia de Conducir?",
  ["En la comuna donde resides", "En cualquier municipalidad del país", "Sólo en la capital regional", "En el Registro Civil"], 0,
  168, "Recuerda que la Licencia de Conducir debe ser obtenida en la comuna donde resides.")
P("anexo3", "¿Cuántas oportunidades entrega el proceso por cada examen teórico y práctico?",
  ["Dos", "Una", "Tres", "Ilimitadas"], 0,
  169, "El proceso de obtención de licencia da la opción de tener dos oportunidades por cada examen teórico y práctico.")
P("anexo3", "¿En qué plazo se pueden repetir los exámenes teóricos reprobados?",
  ["En un plazo no superior a 25 días hábiles desde la primera reprobación",
   "En un plazo de 6 meses",
   "Al día siguiente",
   "En un plazo de 90 días corridos"], 0,
  169, "Exámenes teóricos, en un plazo no superior a 25 días hábiles desde la primera reprobación.")
P("anexo3", "Tras la primera denegación de la licencia, ¿cuánto hay que esperar para iniciar un segundo proceso?",
  ["30 días hábiles", "6 meses", "1 año", "No hay espera"], 0,
  169, "Sin embargo, una vez que se produzca la primera denegación, deberás esperar 30 días hábiles para poder iniciar un segundo proceso.")
P("anexo3", "¿Qué plazo tiene la Municipalidad para informar la emisión de la licencia al Registro Civil?",
  ["5 días hábiles", "30 días corridos", "24 horas", "6 meses"], 0,
  169, "la Municipalidad tiene un plazo de 5 días hábiles para informar al Servicio de Registro Civil e Identificación")
