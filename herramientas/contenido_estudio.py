"""Definición de las tarjetas de estudio de Conduce-Fácil.

Cada tarjeta se compone de una pregunta (la división didáctica del contenido) y
de una respuesta que se recorta LITERALMENTE del Manual CONASET mediante anclas
de texto. Si un ancla no existe en el PDF, la generación falla: así es imposible
publicar contenido inventado o alterado.
"""

from __future__ import annotations

from texto_manual import TextoNoEncontrado, literal

TARJETAS: list[dict] = []
ERRORES: list[str] = []

CAPITULOS = [
    {"id": "cap1", "numero": 1, "titulo": "Los siniestros de tránsito", "paginas": "6-9"},
    {"id": "cap2", "numero": 2, "titulo": "Los principios de la conducción", "paginas": "11-31"},
    {"id": "cap3", "numero": 3, "titulo": "Convivencia Vial", "paginas": "33-35"},
    {"id": "cap4", "numero": 4, "titulo": "La persona en el tránsito", "paginas": "37-66"},
    {"id": "cap5", "numero": 5, "titulo": "Las y los usuarios vulnerables", "paginas": "68-75"},
    {"id": "cap6", "numero": 6, "titulo": "Normas de circulación", "paginas": "77-107"},
    {"id": "cap7", "numero": 7, "titulo": "Conducción en circunstancias especiales", "paginas": "109-125"},
    {"id": "cap8", "numero": 8, "titulo": "Conducción eficiente", "paginas": "127-134"},
    {"id": "cap9", "numero": 9, "titulo": "Informaciones importantes", "paginas": "136-148"},
    {"id": "anexo2", "numero": 10, "titulo": "Glosario de la Ley de Tránsito", "paginas": "162-165"},
    {"id": "anexo3", "numero": 11, "titulo": "Proceso de obtención de la Licencia de Conducir", "paginas": "168-169"},
]


def T(cap: str, seccion: str, pregunta: str, pagina: int, desde: str, hasta: str | None = None, extra: int = 1) -> None:
    try:
        respuesta = literal(pagina, desde, hasta, paginas_extra=extra)
    except TextoNoEncontrado as e:
        ERRORES.append(f"[{cap} p{pagina}] {pregunta[:60]} :: {e}")
        return
    TARJETAS.append(
        {
            "id": f"{cap}-{len(TARJETAS) + 1:03d}",
            "capitulo": cap,
            "seccion": seccion,
            "pregunta": pregunta,
            "respuesta": respuesta,
            "pagina": pagina,
        }
    )


# ---------------------------------------------------------------------------
# Capítulo 1 · Los siniestros de tránsito
# ---------------------------------------------------------------------------
S = "Los siniestros de tránsito"
T("cap1", S, "¿Por qué CONASET dejó de hablar de «accidentes» de tránsito y usa el concepto de «siniestros»?",
  6, "Antes de comenzar, debemos saber", "de cada persona usuaria de las vías.")
T("cap1", S, "¿Qué demuestra que los siniestros de tránsito no son azarosos ni impredecibles?",
  6, "Los siniestros de tránsito tienen poco de azarosos", "disminuir sus consecuencias perjudiciales.")
T("cap1", S, "¿Por qué conducir implica una responsabilidad colectiva y no sólo personal?",
  6, "La conducción de un vehículo implica responsabilidad colectiva", "o indirectamente su decisión.")
T("cap1", S, "¿Cuántas personas fallecen cada día en el mundo por siniestros de tránsito y cómo califica la OMS esta situación?",
  6, "¿Sabías que más de 3.000 personas fallecen", "de salud pública en todo el mundo.")
T("cap1", S, "En Chile, ¿qué lugar ocupan los siniestros de tránsito como causa de muerte según el grupo de edad?",
  6, "En Chile, al igual que en el resto del mundo", "la segunda causa de muerte después de los suicidios.")
T("cap1", S, "¿Se pueden evitar las muertes por siniestros de tránsito?",
  6, "La mayoría de las muertes producidas", "detallados a lo largo de este libro.")
T("cap1", S, "¿Cuánto sufrimiento provoca en el entorno cercano cada persona fallecida en un siniestro?",
  7, "Por otro lado, no se valora el sufrimiento", "sufren dolor (familiares, amigos, etc.).")
T("cap1", S, "¿Qué impacto económico tienen los siniestros de tránsito en Chile?",
  7, "Además de las pérdidas de vidas humanas", "el 2% del PIB según las cifras de la OMS.")
T("cap1", S, "¿Cuánto paga en promedio cada persona al año por los costos de los siniestros de tránsito?",
  7, "Si este dinero fuera invertido", "los siniestros de tránsito posibles de valorizar.")

S = "Estadísticas de siniestros en Chile"
T("cap1", S, "¿Cuántos siniestros y cuántas personas fallecidas se registran anualmente en Chile?",
  8, "Anualmente en Chile se registran más de 82.000 siniestros", "En promedio 450 de ellas son atropelladas.")
T("cap1", S, "¿Dónde se produce la mayor cantidad de personas fallecidas en siniestros de tránsito?",
  8, "La mayor parte de las personas fallecidas", "en vías interurbanas o no urbanas.")
T("cap1", S, "¿Qué porcentaje de los siniestros ocurre en vías urbanas y dónde se concentra?",
  8, "Si bien la mayor cantidad de personas fallecidas en siniestros", "se produce en zonas no urbanas (rural).")
T("cap1", S, "¿Dónde se produce la mayor cantidad de lesionados y de qué gravedad?",
  8, "También en vías urbanas se produce la mayor cantidad", "que los lesionados en carreteras.")
T("cap1", S, "¿Cuántas personas resultan lesionadas graves en promedio cada año?",
  8, "Como promedio de los últimos 5 años, aproximadamente 7.700", "en los más de 82.000 siniestros de tránsito.")
T("cap1", S, "¿Cómo cambia la probabilidad de que un peatón muera atropellado según la velocidad del vehículo?",
  8, "La probabilidad de que un peatón muera atropellado", "lo más probable es que un peatón atropellado muera.")
T("cap1", S, "¿En qué condiciones hay mayor siniestralidad?",
  8, "Existen condiciones que cuentan con mayor siniestralidad", "situaciones de escaso flujo vehicular.")
T("cap1", S, "¿Qué porcentaje de los siniestros de tránsito involucra falla humana y a qué grupo etario afecta más?",
  8, "Además, las estadísticas indican que la falla humana", "en siniestros de tránsito en los últimos años.")
T("cap1", S, "¿Qué porcentaje de las personas conductoras fallecidas en siniestros son varones?",
  8, "Finalmente, se debe agregar que cerca del 79%", "de tránsito son varones.")
T("cap1", S, "¿Cuáles son los factores de mayor incidencia en la ocurrencia de siniestros?",
  8, "La imprudencia de quien conduce", "en la ocurrencia de siniestros.")

S = "Sistema Seguro"
T("cap1", S, "¿Qué establece como principio ético el enfoque de Sistema Seguro?",
  9, "Es por esto que desde el año 2017", "conocido mundialmente como la Visión Cero.")
T("cap1", S, "¿Qué cambio de paradigma supone el enfoque Sistema Seguro?",
  9, "Esto supone un cambio de paradigma", "y guíe el comportamiento humano.")
T("cap1", S, "¿Cómo se gestiona el enfoque Sistema Seguro?",
  9, "El enfoque Sistema Seguro se gestiona", "lesiones graves o la muerte.")
T("cap1", S, "¿Cuáles son los cuatro principios fundamentales y no transables del Sistema Seguro?",
  9, "Los seres humanos cometemos errores", "antes de que el daño ocurra.")

# ---------------------------------------------------------------------------
# Capítulo 2 · Los principios de la conducción
# ---------------------------------------------------------------------------
S = "Funcionamiento del automóvil"
T("cap2", S, "¿Por qué es necesario conocer cómo está construido el automóvil y para qué sirve el panel de instrumentos?",
  11, "Para poder conducir de manera segura", "sobre el estado de los principales sistemas del vehículo:")
T("cap2", S, "¿Qué es el motor y qué combustibles puede utilizar?",
  11, "El motor es la parte del vehículo", "la cantidad de revoluciones del motor en todo momento (ver imagen superior).")
T("cap2", S, "¿Qué indican el tacómetro, el velocímetro y el odómetro?",
  11, "Tacómetro: Velocidad del motor en revoluciones por minuto.", "Indica la distancia total o parcial recorrida por el vehículo.")
T("cap2", S, "¿Qué significan los testigos verdes, rojos y amarillos del panel de instrumentos?",
  11, "Testigos color verde:", "Advierten sobre un posible problema a revisar.")
T("cap2", S, "¿Qué función cumple el sistema de lubricación y qué se debe hacer si se enciende la luz de presión de aceite?",
  12, "Se trata del sistema encargado de distribuir aceite", "ya que le puedes causar averías graves.")
T("cap2", S, "¿Qué recomendaciones existen sobre el aceite del motor?",
  12, "Te recomendamos controlar el nivel de aceite", "no olvides controlar el sellos de los envases.")
T("cap2", S, "¿Qué es el sistema eléctrico y cómo se produce y almacena su energía?",
  12, "Es aquel que se encarga de proporcionar la energía eléctrica", "la correspondiente aguja en el panel de instrumentos.")
T("cap2", S, "¿Qué ocurre cuando la batería está mal cargada o descargada?",
  12, "Una batería mal cargada hace que el vehículo", "la batería se encuentre descargada o desconectada.")
T("cap2", S, "¿Qué se debe revisar primero si una unidad eléctrica deja de funcionar?",
  12, "Por otro lado, debes saber que para tu seguridad", "es probable que una ampolleta se haya quemado.")
T("cap2", S, "¿Qué debes controlar en el sistema eléctrico y qué precaución exige la batería?",
  12, "El nivel de líquido en la batería.", "cuidado con tu ropa y piel.")
T("cap2", S, "¿Qué debes hacer si al conducir sientes un fuerte olor a gasolina?",
  13, "Este sistema es el encargado de suministrar combustible", "el riesgo de incendio en tu vehículo.")
T("cap2", S, "¿Qué debes recordar al cargar gasolina?",
  13, "Apagar el motor del vehículo.", "según las indicaciones del fabricante.")
T("cap2", S, "¿Qué recomendaciones reducen la contaminación asociada al combustible?",
  13, "Evita la apertura de la tapa", "ya que causan alto consumo de combustible.")
T("cap2", S, "¿Qué significan las letras E, F, C y H en los indicadores del tablero?",
  13, "En el indicador de combustible, la letra E significa vacío", "y la letra H, caliente, del inglés \"Hot\".")
T("cap2", S, "¿Cuál es la misión del sistema de refrigeración y qué líquido utiliza?",
  13, "Este sistema tiene la misión de enfriar el motor", "y pasa desde ahí al radiador.")
T("cap2", S, "¿Qué provoca que se eleve la temperatura del motor y qué se debe hacer?",
  13, "Cuando hay una obstrucción del sistema de refrigeración", "detener la marcha y reparar la avería.")
T("cap2", S, "¿Por qué el líquido refrigerante debe contener anticongelante?",
  13, "También es importante destacar que a temperaturas bajo cero", "el tipo de líquido adecuado para tus necesidades.")
T("cap2", S, "¿Qué es el sistema de escape y qué riesgo implica el monóxido de carbono?",
  14, "Se trata del conjunto de elementos y conductos", "sal del vehículo y respira aire fresco.")
T("cap2", S, "¿Qué indica un ruido anormalmente alto del tubo de escape?",
  14, "Un ruido anormalmente alto del tubo de escape", "de orificios en el silenciador.")
T("cap2", S, "¿Qué es la transmisión y cómo llega la energía a las ruedas?",
  14, "Es el sistema encargado de transferir la potencia", "el cambio de marchas y la velocidad del automóvil.")
T("cap2", S, "¿Qué ocurre si se conduce presionando el embrague más tiempo del necesario?",
  14, "Debes saber que al conducir presionando el embrague", "se reduce el control sobre el vehículo.")
T("cap2", S, "¿Qué tipos de caja de cambios existen y para qué sirve?",
  15, "Existen diversos tipos de caja de cambios", "lo que permite optimizar el uso de combustible.")
T("cap2", S, "¿Qué hace el sistema de dirección y qué es la servodirección?",
  15, "El sistema de dirección se encarga de transmitir", "existe un mecanismo auxiliar llamado servodirección.")
T("cap2", S, "¿Qué desalinea la dirección y qué consecuencias tiene?",
  15, "Debes saber que la dirección se desalinea", "y aumente el desgaste de los neumáticos.")
T("cap2", S, "¿Qué señales indican un defecto en la dirección o poca presión en los neumáticos delanteros?",
  15, "Algunas de las señales que te indicarán", "el vehículo tiende a irse hacia un lado.")
T("cap2", S, "¿Para qué sirven la suspensión y la amortiguación?",
  15, "Estos sistemas son los encargados de mantener", "para absorber las irregularidades del asfalto.")
T("cap2", S, "¿Cuáles son los síntomas de amortiguadores en mal estado?",
  15, "Al frenar, el vehículo se inclina hacia adelante", "las luces oscilan de forma llamativa.")
T("cap2", S, "¿Qué consecuencias peligrosas puede tener un amortiguador en malas condiciones?",
  16, "Vehículo con pérdida de estabilidad", "La fatiga aparece con mayor facilidad en quien conduce.")
T("cap2", S, "¿Cuáles son los dos sistemas de frenos que tienen todos los vehículos?",
  16, "1. El freno de servicio (pedal de freno)", "si el motor se detiene en una bajada.")
T("cap2", S, "¿Cuándo conviene hacer pruebas de frenado a baja velocidad?",
  16, "Es importante saber que a temperaturas bajo cero", "si el vehículo ha estado estacionado.")
T("cap2", S, "¿Cuál es el mayor riesgo de una frenada brusca?",
  16, "Ante una situación de emergencia", "no se pueda evitar el obstáculo.")
T("cap2", S, "¿Cómo funciona el sistema de frenado antibloqueo (ABS)?",
  17, "El ABS (sistema de frenado antibloqueo) detecta", "los frenos seguirán funcionando.")
T("cap2", S, "¿Puede aumentar la distancia de frenado en un vehículo con ABS?",
  17, "Se debe tener en cuenta que si un vehículo tiene incorporado", "podría aumentar con respecto a la distancia sin ABS.")
T("cap2", S, "¿Qué debes controlar del sistema de frenos?",
  17, "El nivel del líquido de frenos periódicamente", "el vehículo ha estado guardado por un largo tiempo.")
T("cap2", S, "¿Por qué los neumáticos son un elemento crítico de seguridad?",
  17, "Los neumáticos son el único punto de apoyo", "incluso en situaciones difíciles.")
T("cap2", S, "¿Cuál es la profundidad mínima aconsejable del dibujo de los neumáticos?",
  18, "Para que los neumáticos cumplan bien sus funciones", "que esta es inferior a 1,6 mm.")
T("cap2", S, "¿Qué consecuencias tiene una presión de aire demasiado baja o demasiado alta?",
  18, "Presión de aire demasiado baja Presión de aire demasiado alta En una o en las dos ruedas traseras.", "hace que el vehículo tienda a torcer hacia ese lado.")
T("cap2", S, "¿Qué debes recordar sobre el cuidado de los neumáticos?",
  19, "Controlar la presión de los neumáticos cuando estos estén fríos", "no exceder la velocidad máxima indicada por el fabricante.")
T("cap2", S, "¿Qué debes hacer si se revienta un neumático mientras conduces?",
  19, "Si al ir conduciendo se revienta un neumático trasero", "debes detenerte lentamente al costado de la vía.")
T("cap2", S, "¿Qué indica un desgaste irregular de los neumáticos?",
  19, "Un desgaste irregular puede deberse a problemas", "con menor presión de aire que la recomendada.")
T("cap2", S, "¿Qué focos y luces exteriores deben poseer los vehículos motorizados de cuatro o más ruedas?",
  20, "Parte delantera: Dos focos que proyecten luces altas", "y una luz que ilumine la placa patente del vehículo.")
T("cap2", S, "¿Dónde debe ubicarse la tercera luz de freno?",
  20, "Adicionalmente, debe contar con una tercera luz de freno", "y vehículos de transporte de escolares.")
T("cap2", S, "¿Cómo puedes controlar que tus luces bajas no encandilen a otras personas?",
  20, "Puedes controlar tus luces bajas", "de tu vehículo respecto del nivel del suelo.")
T("cap2", S, "¿Cuándo deben utilizarse las luces intermitentes de advertencia de peligro?",
  20, "Luces de advertencia de peligro:", "para un estacionamiento peligroso o ilegal.", 2)
T("cap2", S, "¿Cuándo pueden usarse las luces neblineras?",
  21, "Luces neblineras: Algunos vehículos", "deben apagarse tan pronto mejore la visibilidad.")
T("cap2", S, "¿Qué son los puntos ciegos o ángulos muertos?",
  21, "Ten presente que aun cuando tus espejos", "denominados puntos ciegos o ángulos muertos")
T("cap2", S, "¿Por qué las imágenes de los espejos laterales se ven más lejanas?",
  21, "Los espejos permiten a la persona conductora ver el tráfico", "más lejanas de lo que están en la realidad.")
T("cap2", S, "¿Qué debes controlar antes de conducir?",
  22, "Cinturones de seguridad Limpiaparabrisas", "Bocina", 0)
T("cap2", S, "¿De qué debes asegurarte siempre antes de poner el vehículo en movimiento?",
  22, "Que al tomar el volante, tus brazos queden ligeramente flexionados.", "para tener siempre una buena visibilidad.")

S = "La energía y las leyes físicas"
T("cap2", S, "¿Cómo afectan las leyes físicas del movimiento a un vehículo que toma una curva?",
  23, "Tienes que tener en cuenta que las personas", "para mantener al vehículo en la carretera.")
T("cap2", S, "¿Cuánto aumenta la energía del movimiento al duplicar la velocidad?",
  23, "Al aumentar la velocidad al doble", "ya que costará más mantener la dirección.")
T("cap2", S, "¿De qué depende la fuerza centrífuga en una curva?",
  23, "La magnitud de la fuerza centrífuga", "y de lo cerrada que sea la curva.")
T("cap2", S, "¿Cómo debes enfrentar una curva?",
  23, "Al enfrentarte a una curva, reduce la velocidad", "y acelera suavemente a la salida de la misma.")
T("cap2", S, "¿Qué es la distancia de reacción y cuánto dura un tiempo normal de reacción?",
  23, "La distancia de reacción es la distancia que recorre el vehículo", "20 metros si lo hace a 72 km/h, etc.")
T("cap2", S, "¿Cómo se compone la distancia de detención?",
  23, "La distancia de detención (S) es la suma", "y la distancia de frenado (F).")
T("cap2", S, "¿Cómo se estima aproximadamente la distancia de reacción?",
  24, "Puedes estimar aproximadamente la distancia de reacción", "debes considerar los 2 primeros dígitos")
T("cap2", S, "¿Qué es la distancia de frenado y de qué depende?",
  24, "La distancia de frenado es la distancia que recorre el vehículo", "y de la forma de frenar.")
T("cap2", S, "¿Cómo crece la distancia de frenado al aumentar la velocidad?",
  24, "La distancia de frenado crece al cuadrado", "la distancia de frenado aumenta 9 veces, etc.")
T("cap2", S, "¿Cómo se debe frenar en situaciones inesperadas si el vehículo no cuenta con ABS?",
  24, "En situaciones inesperadas es necesario saber frenar", "la presión sobre el pedal de freno soltándolo.")
T("cap2", S, "¿Qué precaución exige la fuerza de gravedad en pendientes pronunciadas?",
  25, "Si has andado en bicicleta y has tratado de frenar", "nunca desenganchar el motor ya que pierdes el control del vehículo.")
T("cap2", S, "¿Qué riesgos implica el desplazamiento del centro de gravedad del vehículo?",
  25, "Es importante saber los riesgos que implica", "con la parte trasera hacia delante.")
T("cap2", S, "¿Qué ocurre si un vehículo con tracción delantera acelera más de lo que permite la fricción?",
  25, "Respecto a la tracción de las ruedas", "deja de acelerar y retoma tu trayectoria.")
T("cap2", S, "¿Qué hacer si un vehículo con tracción trasera pierde fricción?",
  25, "Por otro lado, si tienes un vehículo con tracción trasera", "continúa acelerando y gira la dirección hacia la trayectoria.")

S = "Elementos de seguridad"
T("cap2", S, "¿Cuál es la diferencia entre elementos de seguridad activa y pasiva?",
  26, "Son los sistemas que sirven para prevenir", "el cinturón de seguridad y el airbag.")
T("cap2", S, "¿Cuál es la función del cinturón de seguridad?",
  26, "Los cinturones de seguridad tienen la función de salvar vidas", "sujetas con un mismo cinturón.")
T("cap2", S, "¿Desde qué año de fabricación es obligatorio el cinturón en los asientos traseros?",
  26, "El uso de este elemento en los asientos traseros", "de fabricación 2002 o posterior.")
T("cap2", S, "¿A qué equivale chocar a 50, 70 y 90 km/h sin cinturón de seguridad?",
  26, "Un choque a 50 km/h sin llevar puesto el cinturón", "una caída desde el piso 11.")
T("cap2", S, "¿Qué hacer con el cinturón después de sufrir un siniestro?",
  26, "Después de sufrir un siniestro, el cinturón podría estar dañado", "Revísalo después de alguna eventualidad.")
T("cap2", S, "¿Cómo debe colocarse correctamente la banda torácica del cinturón?",
  27, "La banda toráxica debe pasar sobre la clavícula", "y reducir al mínimo su eficacia.")
T("cap2", S, "¿Cómo debe colocarse la banda abdominal del cinturón?",
  27, "La banda abdominal debe colocarse sobre los huesos", "provocar graves lesiones internas durante el siniestro.")
T("cap2", S, "¿Qué se debe verificar una vez abrochado el cinturón?",
  27, "Una vez abrochado el cinturón, debes estirarlo", "puede provocarte lesiones durante el siniestro.")
T("cap2", S, "¿Qué es el efecto submarino y cómo se evita?",
  28, "El uso adecuado del cinturón de seguridad evita el llamado efecto submarino", "se desliza por debajo de la banda abdominal.")
T("cap2", S, "¿Qué postura y tensión del cinturón evitan el efecto submarino?",
  28, "Siempre debes conducir en una postura adecuada", "evita conducir con ropa de mucho volumen.")
T("cap2", S, "¿Qué elementos favorecen el deslizamiento de la persona y anulan las características del asiento?",
  28, "No pongas toallas o almohadones", "es más probable que te deslices por debajo de ella.")
T("cap2", S, "¿Por qué las consecuencias de no usar cinturón no son individuales?",
  28, "Las consecuencias del no uso del cinturón", "o a quien viaje en el asiento delantero.")
T("cap2", S, "¿Qué demuestran los estudios sobre la probabilidad de fallecer sin cinturón de seguridad?",
  28, "El estudio de miles de siniestros demuestra", "tienen el doble de probabilidad de fallecer en ellos.")
T("cap2", S, "¿Qué ocurre si una persona sale eyectada del vehículo por no usar cinturón?",
  28, "Si una persona sufre un siniestro y por no tener puesto", "es mucho más seguro quedar dentro del vehículo.")
T("cap2", S, "¿Es cierto que el cinturón no es necesario en vías urbanas por la baja velocidad?",
  29, "Cerca del 80% de los siniestros con víctimas", "lo que suele ocurrir con frecuencia.")
T("cap2", S, "¿Debe usarse el cinturón durante el embarazo?",
  29, "Las personas embarazadas también deben ponerse el cinturón", "si ella golpea el vientre contra el volante).")
T("cap2", S, "¿Por qué el airbag no reemplaza al cinturón de seguridad?",
  29, "Ningún dispositivo de seguridad del vehículo es capaz de sustituir", "cuando se infle la bolsa de aire.")
T("cap2", S, "¿Qué es el airbag y de cuántos tipos existe?",
  30, "El airbag es una bolsa de aire que se infla", "para que estos se activen ante un impacto.")
T("cap2", S, "¿De qué formas protege el airbag a las personas ocupantes del vehículo?",
  30, "1. Frena suavemente el movimiento", "por ejemplo, del parabrisas.")
T("cap2", S, "¿A qué velocidad se infla el airbag y qué riesgo implica sin cinturón?",
  30, "Al producirse un siniestro, la bolsa de aire se infla", "por la enorme fuerza del golpe.")
T("cap2", S, "¿En qué se basa la eficacia del airbag frontal?",
  30, "La eficacia del airbag frontal se basa", "reducir un 20% la probabilidad de sufrir lesiones mortales.")
T("cap2", S, "¿Dónde nunca debe instalarse un Sistema de Retención Infantil?",
  30, "Nunca debes poner un Sistema de Retención Infantil", "en el asiento delantero.")
T("cap2", S, "¿Qué es el efecto latigazo y cómo se previene?",
  31, "Cuando un vehículo sufre un impacto por atrás", "es usando los apoya cabezas.")
T("cap2", S, "¿Qué consecuencias puede tener no usar correctamente el apoya cabezas?",
  31, "No utilizarlo correctamente podría desencadenar", "podrían prolongarse algunos meses.")
T("cap2", S, "¿Cuál es la posición correcta del apoya cabezas?",
  31, "La posición exacta es detrás de la cabeza.", "y nunca superior a 4 cm.")

# ---------------------------------------------------------------------------
# Capítulo 3 · Convivencia Vial
# ---------------------------------------------------------------------------
S = "Convivencia Vial"
T("cap3", S, "¿Qué es una buena Convivencia Vial?",
  33, "Una buena Convivencia Vial es aquella", "gocen de un nivel adecuado de Educación Vial.")
T("cap3", S, "¿Qué es la Educación Vial?",
  33, "La Educación Vial es la adquisición de valores", "con el fin de contribuir a la Seguridad Vial.")
T("cap3", S, "¿Cuál es la meta de la Seguridad Vial?",
  33, "La meta de la Seguridad Vial es la eliminación total", "que el riesgo percibido sea prácticamente nulo.")
T("cap3", S, "¿Cuál es el mayor riesgo a la hora de conducir?",
  33, "Debes saber que mientras conduces un automóvil corres riesgos", "son el mayor riesgo a la hora de conducir.")
T("cap3", S, "¿Qué porcentaje de los siniestros con víctimas se debe a fallas humanas?",
  33, "Cerca del 90% de los siniestros de tránsito con víctimas", "con una equivocada percepción del riesgo.")
T("cap3", S, "¿Cuál es el primer paso para combatir el crecimiento de la siniestralidad vial?",
  33, "El parque automotriz del país ha crecido", "solo le ocurren a los demás\".")
T("cap3", S, "¿Cuáles son los principales factores de riesgo?",
  34, "Alcohol y drogas, que disminuyen las facultades para conducir.", "pueden generar la pérdida de control del vehículo.")
T("cap3", S, "¿Qué es el Entorno Vial y en qué principio se apoya?",
  34, "Las vías por donde circulan los vehículos conforman el Entorno Vial", "en una serie de principios como el de la confianza.")
T("cap3", S, "¿Qué se espera de las demás personas al circular, según el principio de confianza?",
  34, "Sin este principio no se podría salir a la calle", "que cedan en paso cuando se tiene la prioridad, etc.")
T("cap3", S, "¿Cuál es el principio fundamental en la conducción de un vehículo?",
  35, "La precaución es el principio fundamental", "preventiva para garantizar tu seguridad.")
T("cap3", S, "¿Cuál es la mejor virtud que se puede tener al conducir?",
  35, "En el Entorno Vial, la solidaridad es la mejor virtud", "en pos de una buena Convivencia Vial.")
T("cap3", S, "¿Cuáles son las claves para la convivencia vial?",
  35, "Recuerda siempre ver y ser visible.", "ambientales y del pavimento.")

# ---------------------------------------------------------------------------
# Capítulo 4 · La persona en el tránsito
# ---------------------------------------------------------------------------
S = "La persona en el tránsito"
T("cap4", S, "¿Qué es decisivo cuando las reglas del tránsito no ofrecen claridad?",
  37, "Es necesario practicar la conducción y obtener seguridad", "a través de la experiencia en la conducción, traducida en horas al volante.")
T("cap4", S, "¿Con qué frecuencia sufren siniestros las personas conductoras principiantes?",
  37, "Estadísticas internacionales señalan que las personas conductoras principiantes", "que aquellas con más experiencia en la conducción.")
T("cap4", S, "¿Cuáles son los efectos visuales que influyen en la conducción?",
  37, "Densidad de pauta: sucede cuando hay mayor densidad", "parece hallarse más cerca del ojo.")
T("cap4", S, "¿Cuándo surgen las interpretaciones erróneas del entorno?",
  39, "Estas interpretaciones erróneas del entorno", "y forma son insuficientes o poco claros.")
T("cap4", S, "¿Hasta qué distancia funciona bien la percepción estereoscópica de distancias?",
  39, "Una especie de imagen estereoscópica aparece", "más importancia a la hora de juzgar distancias.")
T("cap4", S, "¿Qué buena regla se recomienda frente a las propias percepciones?",
  39, "¿Por qué es importante saber esto?", "y no conducir cuando exista cansancio.")
T("cap4", S, "¿Por qué es riesgoso hacer dos cosas al mismo tiempo mientras se conduce?",
  39, "Hacer dos cosas al mismo tiempo puede resultar muy riesgoso", "para enfrentar una situación difícil.")
T("cap4", S, "¿Qué influye negativamente en la seguridad del tránsito respecto de la concentración?",
  39, "Además de llevar las dos manos sobre el volante", "influyen negativamente en la seguridad del tránsito.")
T("cap4", S, "¿Por qué las distracciones al conducir provocan siniestros?",
  39, "Las distracciones al conducir son causa de muchos siniestros.", "¡Conducir requiere toda tu atención!")
T("cap4", S, "Entre quien tiene menor tiempo de reacción y quien conduce a baja velocidad, ¿quién detiene antes el vehículo?",
  40, "El tiempo de reacción de las personas conductoras", "es este último quien logrará detener el vehículo primero.")
T("cap4", S, "¿Es cierto que las personas conductoras jóvenes reaccionan más rápido en cualquier situación?",
  40, "Con frecuencia se piensa que las y los conductores jóvenes", "el tiempo de reacción va siendo mayor.")
T("cap4", S, "¿Qué efectos de ceguera se presentan al conducir en la oscuridad?",
  40, "Al conducir en la oscuridad es frecuente", "empeorando por corto tiempo la visión.")
T("cap4", S, "¿Cuál es la distancia de visibilidad al cruzarse con otro vehículo con luces bajas?",
  40, "Pero la verdad es que la distancia de visibilidad", "las demarcaciones de la calzada hasta unos 70 metros.")
T("cap4", S, "¿Cuál es la distancia de visibilidad durante una ceguera temporal?",
  40, "Cuando se produce un efecto de ceguera temporal", "la distancia de visibilidad es de 0 metros.")
T("cap4", S, "¿Qué es la percepción selectiva?",
  41, "Al ir conduciendo, se está expuesto a una gran cantidad", "por el estado de vigilancia.")
T("cap4", S, "¿Qué riesgo genera la percepción selectiva?",
  41, "A causa de la percepción selectiva se corre el riesgo", "circunstancias importantes en el tránsito.")
T("cap4", S, "¿Cuánta luz reflejan la ropa oscura, la ropa blanca y los materiales reflectantes?",
  41, "La utilización de vestimenta favorable para la visibilidad", "y los materiales reflectantes entre un 90 y 98%.")
T("cap4", S, "¿Cómo funciona el ojo humano y qué es la mácula ciega?",
  42, "La pupila regula la entrada de luz", "en él no puede ser percibido.")
T("cap4", S, "¿Cuál es la agudeza visual en la visión periférica y cuál es su función?",
  43, "En las partes externas de la visión periférica", "mueves la cabeza y los ojos y lo reconoces.")
T("cap4", S, "¿Cuál es el campo visual normal de una persona?",
  43, "Aunque no se vea con gran nitidez", "en la capacidad de orientación.")
T("cap4", S, "¿Por qué las personas conductoras con experiencia aprovechan mejor su visión periférica?",
  43, "Las personas conductoras con experiencia, aprovechan", "y concentran su mirada en objetos fijos.")
T("cap4", S, "¿Por qué se subestima la velocidad a la que se conduce?",
  43, "Entre otras causas, tal subestimación se produce", "en lo que a las impresiones de la vista se refiere.")
T("cap4", S, "¿Qué es la visión de túnel?",
  44, "Como ejemplo se puede mencionar el fenómeno denominado visión de túnel", "se encuentra en estado de estrés.")
T("cap4", S, "¿Qué error se comete al estimar el punto de encuentro entre dos vehículos?",
  44, "Otro fenómeno relacionado al procesamiento limitado", "circulan exactamente a la misma velocidad, lo que rara vez coincide con la realidad.")

S = "La conducción segura requiere equilibrio emocional"
T("cap4", S, "¿Por qué la edad mínima para optar a una Licencia de Conducir es 18 años?",
  45, "Para optar a una Licencia de Conducir es necesario haber cumplido 18 años", "sus impulsos que van en contra de su propia decisión.")
T("cap4", S, "¿Qué características de las personas jóvenes aumentan su vulnerabilidad en el tránsito?",
  45, "Excesiva necesidad de autoafirmación", "especialmente por aquella que incita al riesgo.")
T("cap4", S, "¿Cuáles son los factores que influyen en la evaluación y aceptación del peligro?",
  45, "1. Actitud frente al tránsito.", "por lo que su comportamiento será más arriesgado.", 2)
T("cap4", S, "¿Qué conocimientos y destrezas exige ser una buena persona conductora?",
  46, "Ser una buena persona conductora exige muchos conocimientos", "y algo muy importante: hay que ser una persona precavida.")
T("cap4", S, "¿Qué significa tener capacidad de adaptarse a la realidad en el tránsito?",
  46, "Por otro lado, para ser una persona conductora responsable", "que rigen en el contexto del tránsito.")
T("cap4", S, "¿Qué implica poseer una identidad para una persona conductora?",
  46, "Poseer una identidad implica tener una idea clara", "podrían ser la causa de una conducta errada.")
T("cap4", S, "¿Por qué es importante el autocontrol al conducir?",
  46, "El saber controlarse en situaciones que afectan", "es primordial para tomar buenas decisiones.")
T("cap4", S, "¿Qué provoca la agresividad al conducir?",
  47, "La agresividad provoca que se perciba", "lleva a tomar decisiones impulsivas.")
T("cap4", S, "¿Por qué es fundamental la empatía para conducir?",
  47, "Para conducir, es fundamental el desarrollo de la empatía", "es decir, ciclistas, motociclistas y peatones.")
T("cap4", S, "¿Cómo influye la presión del grupo en la conducción?",
  47, "La influencia del grupo puede ser altamente negativa", "para con las demás personas usuarias de las vías.")

S = "Conductas que implican riesgos"
T("cap4", S, "¿Qué es la impulsividad y por qué es negativa al conducir?",
  48, "La impulsividad, que significa que se actúa sin pensar", "con el consiguiente riesgo de siniestros.")
T("cap4", S, "¿Qué consecuencias tiene no asumir la culpa?",
  48, "Ciertas personas tienen una gran propensión a culpar", "al no existir aprendizaje de las experiencias.")
T("cap4", S, "¿Qué es la represión como conducta de riesgo?",
  49, "En diferentes situaciones de la vida las personas tratan de reprimir", "puede resultar decisivo cuando se conduce un vehículo.")
T("cap4", S, "¿Qué provoca reprimir los riesgos con frecuencia?",
  49, "En tu conciencia sabes que los riesgos aumentan.", "la probabilidad de sufrir un siniestro.")
T("cap4", S, "¿Qué es la formación de reacción?",
  49, "Muchos siniestros de tránsito son consecuencia del mecanismo denominado formación de reacción.", "lo que podría desencadenar riesgos en su conducción.")
T("cap4", S, "¿Qué es la validación como conducta de riesgo?",
  49, "Quizás alguien desea mostrar a sus acompañantes", "aumentan los riesgos de sufrir o provocar un siniestro.")

S = "Sobre el alcohol en la conducción"
T("cap4", S, "¿Qué estableció la Ley Tolerancia Cero del año 2012?",
  50, "En el año 2012 fue promulgada la modificación a la Ley de Tránsito", "también las sanciones asociadas a la conducción con alcohol.")
T("cap4", S, "¿Cuánto aumenta el riesgo de siniestro con alcoholemia entre 0,3 y 0,8 g/l?",
  50, "Con una alcoholemia entre 0,3 y 0,5 g/l", "el riesgo es cinco veces más que si no hubiera bebido.")
T("cap4", S, "¿Qué se entiende por conducción bajo la influencia del alcohol y en estado de ebriedad, y qué sanciones tienen?",
  50, "0,31 - 0,79 gramos por mil de alcohol en la sangre. 0,8 o más gramos", "cancelación de licencia y presidio (cárcel).")
T("cap4", S, "¿Cuándo aumentan significativamente las sanciones por conducir con alcohol?",
  50, "Las sanciones aumentan significativamente en caso de reincidencia", "personas fallecidas y/o con lesiones.")
T("cap4", S, "¿Qué sanciona la Ley Emilia y qué se considera delito calificado?",
  51, "Una modificación legal en el año 2014, conocida como Ley Emilia", "en el ejercicio de sus funciones.")
T("cap4", S, "¿Qué ocurre si la persona conductora se niega a realizarse las pruebas de detección de alcohol?",
  51, "Por otro lado, si la persona conductora que participa", "dependiendo de las consecuencias del siniestro.")
T("cap4", S, "¿Cómo afecta el alcohol al organismo y a partir de qué concentración?",
  51, "El cerebro es afectado por el alcohol", "acrecentar estas sensaciones bebiendo más.")
T("cap4", S, "¿Cómo perturba el alcohol el tiempo de reacción y la coordinación?",
  51, "El alcohol perturba el estado de ánimo", "y coordinación de una persona conductora ante un imprevisto.")
T("cap4", S, "¿Cómo afecta el alcohol a la visión periférica y a la visión doble?",
  51, "Asimismo, la mayoría de las personas no nota una reducción", "lo que dificulta enfocar la mirada.")
T("cap4", S, "¿Cuál es la única tasa de alcohol segura para conducir?",
  51, "La única tasa de alcohol segura para conducir es \"0\".", "busca otra alternativa para transportarte.")
T("cap4", S, "¿Qué funciones se ven afectadas antes de que la persona note su estado?",
  51, "La visión periférica, la atención, el tiempo de reacción", "de que empieces a darte cuenta del estado en que te encuentras.")
T("cap4", S, "¿Cómo se conoce la tasa de alcohol en la sangre de una persona?",
  52, "Para conocer la tasa de alcohol que tiene una persona", "usados por Carabineros de Chile.")
T("cap4", S, "¿Cómo influyen la masa corporal y el sexo en la tasa de alcoholemia?",
  52, "La masa corporal: A menor peso corporal", "ni experimentan los mismos efectos.")
T("cap4", S, "¿Cómo influye el tiempo que dura la ingesta de alcohol?",
  52, "El tiempo que dura la ingesta.", "el cuerpo eliminará algo de alcohol antes de recibir más.")
T("cap4", S, "¿En cuánto tiempo se detecta el alcohol en la sangre y cuándo alcanza su nivel máximo?",
  52, "El alcohol se detecta en la sangre 5 minutos", "en promedio, a la hora después de haber bebido.")
T("cap4", S, "¿A qué ritmo elimina el cuerpo el alcohol y se puede acelerar?",
  52, "El cuerpo se libera del alcohol mediante la metabolización", "una ducha fría o ejercicios físicos.")
T("cap4", S, "¿Cómo influyen el alimento ingerido y la edad en la concentración de alcohol?",
  53, "El alimento ingerido: La concentración de alcohol", "porque no han tenido la práctica necesaria.")

S = "Las drogas y estupefacientes"
T("cap4", S, "¿Cuál es el mayor riesgo de conducir bajo el efecto de drogas?",
  53, "El mayor riesgo de conducir bajo el efecto de drogas", "el historial de la persona consumidora, entre otros factores.")
T("cap4", S, "¿Cuáles son las principales consecuencias del consumo de marihuana para la conducción?",
  53, "Se clasifica como depresor, alucinógeno.", "Produce fuertes somnolencias.")
T("cap4", S, "¿Cuáles son los principales efectos de la cocaína en la conducción?",
  53, "Es un estimulante cuyos principales efectos son:", "pudiendo sufrir distracciones fácilmente.", 2)
T("cap4", S, "¿Cuáles son las cuatro etapas del consumo de pasta base?",
  54, "1. Etapa de euforia:", "visuales, auditivas, olfativas o cutáneas.")
T("cap4", S, "¿Qué efectos físicos destacan del consumo de pasta base?",
  54, "En todas sus etapas los riesgos para la conducción", "temblores, náuseas y/o vómitos.")
T("cap4", S, "¿Qué manifestaciones puede generar el consumo de éxtasis?",
  54, "Períodos de mayor sensibilidad a la luz", "períodos de agotamiento físico y mental.")
T("cap4", S, "¿Qué se debe hacer si se ha consumido cualquier droga?",
  55, "Si has consumido cualquier droga, no conduzcas.", "para volver a conducir de forma segura.")

S = "Enfermedades y medicamentos"
T("cap4", S, "¿Qué enfermedades tienen mayor riesgo de ocurrencia de siniestros?",
  56, "No todas las enfermedades implican los mismos riesgos", "y algunos problemas de visión.")
T("cap4", S, "¿Qué evaluación médica se realiza al iniciar el proceso de licencia?",
  56, "Ten presente que al iniciar un proceso de otorgamiento", "poder aprobar o rechazar el examen médico.")
T("cap4", S, "¿Qué acciones disminuyen el riesgo si se tiene una enfermedad crónica?",
  56, "Conocer bien tu enfermedad.", "Consultar con un médico los riesgos de tu patología para una conducción segura.")
T("cap4", S, "¿Cuánto recorre un vehículo a 90 km/h durante un estornudo de un segundo?",
  58, "Es importante saber que esta enfermedad puede afectar", "sin que se pueda prestar atención a las condiciones de la vía.")
T("cap4", S, "¿Qué consejos existen para personas conductoras alérgicas?",
  58, "Intentar no abrir las ventanas durante la conducción", "pueden no recomendar el medicamento más adecuado.")
T("cap4", S, "¿Qué es el estrés y qué consecuencias tiene si se mantiene mucho tiempo?",
  58, "El estrés es un mecanismo de defensa del organismo", "problemas digestivos e incluso infartos.")
T("cap4", S, "¿Cómo influye un grado demasiado alto de estrés en la persona conductora?",
  59, "La influencia negativa de un grado demasiado alto de estrés", "cierta rigidez cerebral y muscular.")
T("cap4", S, "¿Cómo influye la depresión sobre las capacidades para conducir?",
  59, "Los cambios de estado de ánimo provocan", "puede inducir a la persona a provocar un siniestro de tránsito.")
T("cap4", S, "¿A qué riesgo equivale conducir bajo los efectos de algunos antihistamínicos?",
  60, "Se ha comprobado que el riesgo de conducir", "esto es, conducir bajo la influencia del alcohol.")
T("cap4", S, "¿Qué son los psicofármacos y qué tipos existen?",
  60, "Son aquellos medicamentos usados para el tratamiento", "una efímera y fuerte sensación de autoconfianza.")

S = "Cansancio, sueño y fatiga"
T("cap4", S, "¿Qué porcentaje de los siniestros de tránsito se asocia al factor sueño?",
  62, "Datos a nivel internacional revelan que entre el 15 y el 30%", "y muchos de ellos tienen consecuencias graves.")
T("cap4", S, "¿Cuáles son los efectos del cansancio y del sueño en la conducción?",
  62, "Aumenta el tiempo de reacción.", "cuando otro vehículo lleva luces altas cuando se tiene sueño.")
T("cap4", S, "¿Qué son los microsueños?",
  62, "Pueden presentarse microsueños, que son períodos", "Numerosos siniestros se producen a consecuencia de estos.")
T("cap4", S, "¿Cuáles son las diferentes fases del cansancio?",
  63, "La primera señal de cansancio se manifiesta", "ni con el máximo esfuerzo de voluntad.")
T("cap4", S, "¿Qué factores favorecen la aparición del sueño?",
  63, "El momento del día. La madrugada", "en pocos días experimentarás una gran somnolencia.")
T("cap4", S, "¿Cómo influyen el tránsito monótono y las sustancias sedantes o estimulantes en la somnolencia?",
  64, "El tránsito monótono. Conducir de noche", "la que influye muy negativamente en la Seguridad Vial.")
T("cap4", S, "¿Cuáles son los efectos de la fatiga más riesgosos para la conducción?",
  64, "La capacidad de mantener la atención en el entorno", "El tiempo de reacción se incrementará.", 2)
T("cap4", S, "¿Qué circunstancias favorecen la aparición de la fatiga al volante?",
  65, "Circular por una vía con mucho tráfico", "que hagan incómoda y difícil la conducción.", 2)
T("cap4", S, "¿Qué consejos se recomiendan en caso de fatiga o cansancio en la conducción?",
  66, "Si sientes cansancio o sueño al ir conduciendo", "y la de las demás personas.")
T("cap4", S, "¿Cada cuánto se debe descansar en viajes largos?",
  66, "En viajes largos, descansa al menos 20 a 30 minutos", "de conducción, como máximo.")

# ---------------------------------------------------------------------------
# Capítulo 5 · Las y los usuarios vulnerables
# ---------------------------------------------------------------------------
S = "Las y los usuarios vulnerables"
T("cap5", S, "¿Quiénes son las y los usuarios vulnerables de las vías?",
  68, "Si bien todas las personas usuarias de las vías públicas", "personas ciclistas, motociclistas, entre otras.")
T("cap5", S, "¿Qué proporción de las víctimas mortales del tránsito representan peatones, ciclistas y motociclistas?",
  68, "Peatones, ciclistas y motociclistas, junto con sus pasajeros", "por causa del tránsito en el mundo.")
T("cap5", S, "¿Qué porcentaje de los siniestros son atropellos y qué porcentaje de fallecidos representan?",
  68, "En Chile, los atropellos representan aproximadamente el 15%", "aproximadamente al 28% del total de fallecidas.")
T("cap5", S, "¿Qué es la zona de incertidumbre y qué infracciones cometen con frecuencia los peatones?",
  68, "La alta siniestralidad de estas personas usuarias", "pasarelas o no respetar los semáforos.")
T("cap5", S, "¿Cómo influyen los teléfonos y audífonos en el comportamiento de los peatones?",
  68, "Sumado a este comportamiento, hay que considerar el uso de teléfonos", "Ten mucha precaución.")
T("cap5", S, "¿Qué debes hacer como persona conductora frente a los peatones?",
  68, "Estar siempre alerta y anticiparte", "Estos probablemente no te han visto.")
T("cap5", S, "¿Cuáles son los principales problemas que enfrentan las personas mayores en la vía pública?",
  69, "Exceso de ruido en el ambiente", "descender inesperadamente a la calzada.")
T("cap5", S, "¿Cuántos segundos más puede necesitar una persona mayor para cruzar una calle de 16 metros?",
  69, "Las calles pueden resultar demasiado anchas para cruzar", "de 16 metros de ancho.")
T("cap5", S, "¿Cómo debes comportarte ante peatones, personas ebrias o con impedimentos?",
  69, "Demuestra consideración hacia las y los peatones.", "pueden tener dificultades auditivas.")
T("cap5", S, "¿Cómo afecta la edad avanzada a las capacidades de conducción?",
  70, "El deterioro de las capacidades psicomotoras", "hay que darles tiempo suficiente y no presionarlos a actuar.")
T("cap5", S, "¿Qué características tienen las niñas y niños en el tránsito?",
  70, "Tienen una estatura pequeña", "Comienzan a actuar con seguridad en el tránsito entre los 9 y 12 años de edad.")
T("cap5", S, "¿En qué situaciones debes estar preparado para detener el vehículo por la presencia de niñas y niños?",
  70, "En áreas residenciales donde las niñas y niños juegan", "se interesan más en éstos que en el tránsito.")
T("cap5", S, "¿Cómo debes actuar ante vehículos a tracción animal o personas a caballo?",
  70, "Presta atención cuando en un camino o una carretera", "Mantén una distancia lateral prudente.", 2)
T("cap5", S, "¿Por qué no se deben hacer señales luminosas o acústicas cerca de animales?",
  71, "No hagas señales luminosas o acústicas", "y provocar una situación de riesgo.")
T("cap5", S, "¿Por qué los siniestros en motocicleta resultan fácilmente fatales?",
  71, "Pese a sus ventajas, la falta de carrocería produce", "que en uno cerrado y de mayor tamaño.")
T("cap5", S, "¿Por qué hay que tener especial cuidado con motociclistas en los cruces?",
  71, "Son frecuentes las colisiones que se producen en intersecciones", "no cuentan con carrocería para proteger a quien los conduce.")
T("cap5", S, "¿Qué se entiende por persona ciclista y cuál es su principal elemento de seguridad?",
  71, "Se entiende como persona ciclista a toda aquella", "las cuales son las de mayor importancia en caso de atropello.")
T("cap5", S, "¿Qué espacio lateral debes dejar al pasar cerca de una persona ciclista?",
  71, "Al pasar con tu vehículo cerca de una persona ciclista", "del mayor esfuerzo desarrollado al pedalear.")
T("cap5", S, "¿Qué precauciones debes tomar ante la presencia de ciclistas?",
  72, "Cuando circules detrás de una persona ciclista", "No siempre circulan con luces que permitan verles oportunamente.")
T("cap5", S, "¿Puede un vehículo motorizado circular, detenerse o estacionar en una ciclovía?",
  72, "Recuerda que como persona conductora de un vehículo motorizado", "antes de abrir la puerta.")
T("cap5", S, "¿Qué señales de brazo deben utilizar las personas ciclistas para comunicar sus maniobras?",
  72, "Viraje a la derecha Brazo izquierdo en ángulo recto", "Brazo izquierdo extendido hacia abajo.")

S = "Niñas y niños en el automóvil"
T("cap5", S, "¿Qué debes hacer cuando llevas niñas y niños en tu vehículo?",
  73, "Cuando lleves niñas y/o niños en tu vehículo enfrentarás", "abiertas desde el interior del vehículo.")
T("cap5", S, "¿Qué es un Sistema de Retención Infantil y quién está obligado a usarlo?",
  73, "Ten en cuenta que eres un ejemplo a seguir", "al momento de transportar a niñas y niños en un automóvil.")
T("cap5", S, "¿Qué cifras existen sobre niñas, niños y adolescentes fallecidos en Chile?",
  73, "Los siniestros de tránsito son una de las principales causas de", "y 36.221 resultaron con lesiones.")
T("cap5", S, "¿Qué prohibición se estableció desde marzo de 2016 respecto de menores de 12 años?",
  73, "Se estableció la prohibición del traslado de menores de 12 años", "si este ya les queda bien posicionado (ver esquema inferior).")
T("cap5", S, "¿Hasta qué edad, estatura y peso es obligatorio el Sistema de Retención Infantil?",
  73, "Asimismo, desde marzo de 2017 la Ley de Tránsito obliga", "escolar y vehículos de similares características.")
T("cap5", S, "¿Cómo se sanciona el incumplimiento del uso del Sistema de Retención Infantil?",
  73, "El incumplimiento de estas medidas es sancionado", "de la Licencia de Conducir de 5 a 45 días.")
T("cap5", S, "¿Cómo se usa correctamente el cinturón de seguridad en niñas y niños?",
  74, "El niño o niña abordo debe sentarse apoyando", "Los pies deben apoyarse completamente en el piso del vehículo.")
T("cap5", S, "¿Por qué no basta con utilizar un Sistema de Retención Infantil?",
  74, "Se debe tener en cuenta que no basta solo con utilizar", "a través del arnés o el cinturón de seguridad.")
T("cap5", S, "¿Desde cuándo y hasta cuándo deben utilizarse los Sistemas de Retención Infantil?",
  74, "Estos dispositivos deben utilizarse desde el primer viaje", "hasta que puedan usar el cinturón de seguridad directamente.")
T("cap5", S, "¿Qué lesiones genera el uso incorrecto del cinturón de seguridad en menores?",
  74, "El uso incorrecto del cinturón de seguridad, genera lesiones importantes", "que pueden comprometer seriamente la vida.")
T("cap5", S, "¿Qué aspectos se deben considerar al elegir un Sistema de Retención Infantil?",
  74, "Peso, altura y nivel de desarrollo de la niña y/o niño", "indicados por el fabricante (mínimo hasta los dos años).")
T("cap5", S, "¿Qué tipos de anclaje puede tener un Sistema de Retención Infantil?",
  75, "Que se puede instalar correcta y fácilmente", "a menos que lo indique el fabricante del SRI.")
T("cap5", S, "¿Cómo es la etiqueta que deben llevar las sillas infantiles certificadas?",
  75, "La etiqueta debe ir pegada a la silla", "y mide 9,5 cm de alto y 7,5 cm de ancho.")

# ---------------------------------------------------------------------------
# Capítulo 6 · Normas de circulación
# ---------------------------------------------------------------------------
S = "El lenguaje del tránsito"
T("cap6", S, "¿De cuántas maneras se expresa el lenguaje asociado al tránsito?",
  77, "Lograr una buena Convivencia Vial requiere cumplir", "Las reglas del tránsito.")
T("cap6", S, "¿Qué significan las señales de Carabineros según su posición?",
  77, "Carabineros vistos de frente o de espalda", "y quienes tengan vía libre deben detenerse.")
T("cap6", S, "¿Qué indicación prevalece si hay más de una instrucción en el tránsito?",
  77, "Puede que en alguna ocasión, enfrentes más de una instrucción", "prevalecen sobre las demás.")
T("cap6", S, "¿Por qué los cruces con semáforo pueden convertirse en zonas de riesgo?",
  78, "En los cruces con altos flujos vehiculares se instalan semáforos", "para la generación de siniestros de tránsito.")
T("cap6", S, "¿Qué significa la luz verde del semáforo y qué precaución exige?",
  78, "Luz verde: Indica paso.", "Si vas a virar, debes cederles el paso.")
T("cap6", S, "¿Qué significan la luz roja y la luz roja intermitente?",
  78, "Luz roja: Indica detención.", "que hagan riesgoso el cruzar.")
T("cap6", S, "¿Qué significan la luz amarilla y la luz amarilla intermitente?",
  78, "Luz amarilla: Indica prevención.", "y continuar con la debida precaución.")
T("cap6", S, "¿Qué tipo de infracción es no respetar la luz roja del semáforo?",
  78, "No respetar la indicación de la luz roja", "es una infracción gravísima a la Ley de Tránsito.")
T("cap6", S, "¿Qué es un semáforo con cabezal para ciclistas?",
  79, "Semáforo con cabezal para ciclistas:", "recuerda que tienen la preferencia.")
T("cap6", S, "¿Qué señales luminosas existen en los cruces ferroviarios y qué significan sus colores?",
  79, "Semáforos con cruces ferroviarios:", "el sistema de seguridad podría fallar.")
T("cap6", S, "¿Qué significa la combinación de luz roja y flecha verde?",
  79, "Luz roja y flecha verde:", "y continuar con la debida precaución.")
T("cap6", S, "¿Cómo funcionan los semáforos para el transporte público?",
  80, "Semáforo para el transporte público:", "el color verde puede ser reemplazado por blanco.")
T("cap6", S, "¿Qué indican la equis y la flecha de las señales de mensaje variable sobre la calzada?",
  80, "Una pista puede encontrarse temporalmente cerrada al tránsito.", "La flecha muestra que la vía está abierta al tránsito.")

S = "Señales de tránsito"
T("cap6", S, "¿Para qué se emplean las señales verticales?",
  80, "Estas señales se emplean para indicar a las personas conductoras", "y otras entregan información importante.")
T("cap6", S, "¿Qué finalidad tienen las señales reglamentarias y qué forma poseen?",
  80, "Señales reglamentarias: tienen por finalidad notificar", "Sólo Bicicletas, entre otras.")
T("cap6", S, "¿Qué indica la señal FIN RESTRICCIÓN?",
  80, "Es importante destacar que la señal FIN RESTRICCIÓN", "corresponde a \"No adelantar\".")
T("cap6", S, "¿Qué propósito y forma tienen las señales de advertencia de peligro?",
  81, "Señales de advertencia de peligro: tienen como propósito advertir", "con una tonalidad levemente verde.")
T("cap6", S, "¿Qué debes hacer al pasar una señal de advertencia de peligro?",
  81, "Dado que todas estas señales advierten un peligro", "para tu seguridad y la de las demás personas.")
T("cap6", S, "¿Qué propósito tienen las señales informativas y de qué colores son?",
  81, "Señales informativas: tienen como propósito orientar y guiar", "atractivos turísticos también pueden ser de color café.")
T("cap6", S, "¿Qué son las señales transitorias y de qué color son?",
  81, "Señales transitorias: Estas pueden corresponder al tipo preventivo", "la que es de color amarillo.")
T("cap6", S, "¿Qué precauciones exige circular por zonas con trabajos en la vía?",
  81, "Recuerda moderar tu velocidad en zonas con trabajos", "incluso maquinaria, pueden ser un riesgo.")
T("cap6", S, "¿Para qué sirven las demarcaciones o marcas viales?",
  82, "Las demarcaciones (marcas viales) aclaran y fortalecen las normas.", "flechas, símbolos, leyendas y otros.")
T("cap6", S, "¿Qué indican las líneas longitudinales discontinuas?",
  82, "Las líneas longitudinales discontinuas", "no imponga riesgos a las demás personas.")
T("cap6", S, "¿Qué indican las líneas longitudinales continuas?",
  82, "Las líneas longitudinales continuas", "de una curva o ante un cambio de rasante.")
T("cap6", S, "¿Qué ocurre con las líneas longitudinales mixtas?",
  82, "En ocasiones, las líneas longitudinales pueden presentarse en forma mixta", "por el lado en que esta es segmentada.")
T("cap6", S, "¿Qué es la línea de borde de calzada o berma y se puede circular por ella?",
  82, "Otro caso de importancia, es el de la línea longitudinal que indica el borde", "podrás traspasar esta línea para permanecer en la berma.")
T("cap6", S, "¿Cuándo la línea de borde de calzada puede ser segmentada?",
  82, "La línea de borde de calzada también puede ser segmentada", "además, en general más anchas (ver imagen en la página 118).")
T("cap6", S, "¿Qué significan las demarcaciones amarillas en caminos de montaña y en áreas urbanas?",
  82, "Además, debes saber que en caminos de montaña", "la prohibición de estacionar a lo largo de esta")
T("cap6", S, "¿Qué demarcaciones son importantes en los cruces?",
  83, "Demarcaciones en los cruces: En un cruce regulado con semáforo", "así como a pasos peatonales y cruce de ciclovías.")
T("cap6", S, "¿Cómo se demarca un paso de cebra y dónde se ubica la línea de detención?",
  83, "Demarcación paso de cebra:", "imaginariamente se ubica a no menos de un metro antes de éstos.")
T("cap6", S, "¿Qué indica la demarcación de no bloquear cruce?",
  83, "Demarcación de no bloquear cruce:", "espacio suficiente para no quedar detenido en él.")
T("cap6", S, "¿Qué son las demarcaciones de símbolos y leyendas?",
  83, "Demarcación de símbolos y leyendas:", "y la leyenda LENTO")
T("cap6", S, "¿Se puede circular o estacionar sobre las áreas achuradas?",
  83, "Otras demarcaciones: Entre estas se encuentran", "abandona la pista tan pronto puedas hacerlo de manera segura.")
T("cap6", S, "¿Qué prioridad tienen las y los peatones en un paso de cebra?",
  83, "¡No lo olvides! En un paso de cebra", "las y los peatones tienen prioridad.")

S = "Las reglas del tránsito"
T("cap6", S, "¿A quién debes dar preferencia en un cruce sin semáforo ni señales PARE o Ceda el Paso?",
  84, "Cuando te aproximes a un cruce sin semáforo", "por la otra vía desde tu derecha.")
T("cap6", S, "¿Qué preferencia tienes al momento de virar?",
  84, "Al momento de virar no tienes preferencia", "las y los peatones en los cruces o pasos reglamentarios.")
T("cap6", S, "¿Qué debes hacer al incorporarte a una rotonda o minirrotonda?",
  84, "Al incorporarte a una zona de tránsito en rotación", "debes ceder el paso a los vehículos que circulan por ella.")
T("cap6", S, "¿Qué debes hacer al enfrentar la señal PARE?",
  84, "Al enfrentar la señal PARE debes detener tu vehículo", "cuando no exista posibilidad alguna de siniestro.")
T("cap6", S, "¿Qué debes hacer al enfrentar la señal CEDA EL PASO?",
  84, "Al enfrentar una señal CEDA EL PASO", "cuya proximidad constituya riesgo de siniestro.")
T("cap6", S, "¿Qué preferencia existe en áreas rurales entre una vía secundaria y una principal?",
  85, "En las áreas rurales, cuando te aproximes a una vía principal", "que circulen por la vía principal.")
T("cap6", S, "¿Qué significa exactamente ceder el paso?",
  85, "Ten presente también, que ceder el paso significa", "de quien no tiene la prioridad.")
T("cap6", S, "¿Cuáles son las otras obligaciones de ceder el paso?",
  85, "Al aproximarte a un paso de cebra en el que alguien", "carecerás de todo derecho preferente de paso respecto de peatones y vehículos en tránsito.")
T("cap6", S, "¿Qué ocurre cuando la pista por la que circulas se ve sorpresivamente obstaculizada?",
  85, "Cuando la pista por la que circulas se ve sorpresivamente obstaculizada", "para poder cambiarte de pista.")
T("cap6", S, "¿Cómo se debe actuar ante la aproximación de un vehículo de emergencia?",
  85, "Vehículos de emergencia: Ante la aproximación", "abandónala tan pronto puedas hacerlo de manera segura.")
T("cap6", S, "¿Qué obligación tienes respecto de las señales que haces a quien te sigue?",
  85, "Como persona conductora, tienes la obligación de hacer saber", "e intenta interpretar sus intenciones.")
T("cap6", S, "¿Cuándo debes señalizar tus maniobras?",
  86, "Señaliza cuando vayas a ponerte en movimiento", "Señaliza cuando vayas a virar.")
T("cap6", S, "¿Cómo debe darse la señal antes de una maniobra?",
  86, "La señal debe darse con tiempo suficiente", "hacia las demás personas usuarias de las vías.")
T("cap6", S, "¿Cuál es la secuencia correcta antes de un cambio de pista?",
  86, "Ante un cambio de pista, no comiences a señalizar", "la secuencia espejo - señalización - maniobra.")
T("cap6", S, "¿Qué señales con el brazo indican viraje y detención?",
  86, "Brazo extendido horizontalmente indica viraje a la izquierda.", "indica disminución de velocidad o detención.")
T("cap6", S, "¿Cuándo puedes usar la bocina y cuándo nunca debes usarla?",
  87, "Sólo para prevenir un siniestro y siempre que su uso", "Ni al adelantar o sobrepasar a animales.")
T("cap6", S, "¿Qué debes saber sobre las luces de freno y las intermitentes de emergencia?",
  87, "Las luces de freno se encienden automáticamente", "haya una situación de riesgo.")
T("cap6", S, "¿Cómo se divide la calzada cuando el eje no está demarcado?",
  87, "En ocasiones, el eje de calzada puede no estar demarcado.", "y siempre debes circular por la derecha.")
T("cap6", S, "¿Qué regla se aplica para la distancia con el vehículo que va adelante en carretera?",
  87, "Saber cuál es la distancia correcta con respecto al vehículo", "dicha distancia puede reducirse a la mitad.")
T("cap6", S, "¿Qué riesgos genera mantener una distancia muy corta?",
  87, "Mantener una distancia muy corta aumenta los riesgos de siniestro", "La conducción se hace irregular y poco económica.")
T("cap6", S, "¿En qué consiste la «Regla de los Tres Segundos»?",
  88, "Otra regla aplicable en carreteras que te permite saber", "Disminuye la presión sobre el acelerador.")
T("cap6", S, "¿Cuántos metros recorres antes de empezar a frenar según la velocidad?",
  88, "Cuando descubras que un vehículo que va adelante tuyo", "25 metros si vas a 90 km/h.")
T("cap6", S, "¿A qué se deben por lo general los choques en serie?",
  88, "Por lo general, los choques en serie se deben", "lo que no les permite frenar a tiempo.")
T("cap6", S, "¿Qué hacer para reducir los riesgos de colisión?",
  88, "Varía la distancia que mantienes respecto del vehículo", "o de la carretera son adversas.")
T("cap6", S, "¿Qué distancia exige la ley entre vehículos que circulan en un mismo sentido?",
  89, "Sobre esta materia, la ley señala que cuando dos o más vehículos", "que marchan en caravana en un cortejo fúnebre.")
T("cap6", S, "¿Por qué aumentar la distancia detrás de un vehículo con patente extranjera?",
  89, "Aumenta tu distancia si en la ciudad vas circulando", "una señal o virar inesperadamente.")
T("cap6", S, "¿Cuándo es mayor el riesgo en los cruces y adelantamientos?",
  89, "Los cruces con vehículos y los adelantamientos implican siempre riesgos.", "por posibles adelantamientos y cruces con otros.")
T("cap6", S, "¿Qué espacio debes dejar al pasar cerca de vehículos estacionados?",
  89, "Deja un espacio suficiente, equivalente al ancho de una puerta", "entre los vehículos con la intención de cruzar.")
T("cap6", S, "¿Por qué mitad de la calzada debes circular y cuándo puedes usar la pista izquierda?",
  90, "Sitúate completamente dentro de una pista", "la que reserva pista para el tránsito de alta o baja velocidad.")
T("cap6", S, "¿Qué reglas rigen los cambios de pista de circulación?",
  90, "Como se señaló anteriormente, en ciertos casos podrás ubicar", "para ingresar de forma inmediata a una tercera.")
T("cap6", S, "¿Qué debes hacer al cambiarte de pista?",
  91, "Verificar a través del espejo retrovisor", "Mirar a larga distancia hacia adelante y hacia atrás.")
T("cap6", S, "¿Cuáles son los pasos para realizar un viraje a la derecha?",
  91, "1. Ubícate tan cerca como sea posible del borde derecho", "elige la ubicación más conveniente para continuar.")
T("cap6", S, "¿Con cuánta anticipación debes señalizar la intención de virar?",
  91, "Debes señalizar tu intención de virar con una anticipación suficiente", "Debes apagar el señalizador una vez finalizado el viraje.")
T("cap6", S, "¿Cómo se ejecuta correctamente un viraje a la izquierda desde una vía de doble tránsito?",
  92, "Para virar desde una vía de doble tránsito", "si la vía fuese de un único sentido de tránsito.")
T("cap6", S, "¿Por qué no debes situarte en forma oblicua al esperar para virar a la izquierda?",
  92, "Si te chocaran por atrás", "lo que podría dar origen a una colisión frontal.")
T("cap6", S, "¿En qué debes concentrarte antes de efectuar un viraje a la izquierda?",
  92, "Antes de efectuar un viraje a la izquierda es especialmente importante", "no obstaculizar innecesariamente a los vehículos que se acercan por detrás tuyo.")
T("cap6", S, "¿Cuándo conviene renunciar a efectuar un viraje a la izquierda?",
  93, "Hay ocasiones en las que debes renunciar a efectuar un viraje", "que pueda aparecer sorpresivamente.")
T("cap6", S, "¿Qué tipo de siniestros se producen con frecuencia al virar a la izquierda?",
  93, "Una gran cantidad de los siniestros que se producen", "corresponden a choques por atrás.")
T("cap6", S, "¿Qué es un viraje en «U» y dónde puede realizarse?",
  94, "Se denomina viraje en \"U\" a aquella maniobra", "siempre que ello no esté expresamente prohibido.")
T("cap6", S, "¿Dónde no debes virar en «U»?",
  94, "En las intersecciones de calles y caminos.", "Donde la señalización o demarcación lo prohíba.")
T("cap6", S, "¿Cómo elegir la pista correcta cuando hay varias pistas en la misma dirección?",
  94, "Cuando existan varias pistas en una misma dirección", "cuando vas a continuar derecho.")
T("cap6", S, "¿Cómo debes actuar al acercarte y circular por una rotonda?",
  94, "Al acercarte a una rotonda, decide lo antes posible", "pasado la salida inmediatamente anterior a la que utilizarás.")
T("cap6", S, "¿Qué son las pistas reservadas para el transporte público y cuándo puedes ingresar?",
  95, "En algunas ciudades y sectores de ellas suele privilegiarse", "y sea estrictamente necesario para poder virar.")
T("cap6", S, "¿Pueden otros vehículos utilizar las ciclovías?",
  95, "En algunos lugares pueden existir ciclovías.", "delimitadas sólo con demarcación al borde de la calzada.")
T("cap6", S, "¿Qué son las pistas o vías con tránsito reversible?",
  95, "Estas pistas o vías, son utilizadas a lo largo del día", "circular por ellas sólo de sur a norte.")
T("cap6", S, "¿Qué son las vías de uso exclusivo y las pistas de emergencia?",
  95, "Con el propósito de favorecer al transporte público", "derivadas de la falla del sistema de frenos de un vehículo.")

S = "La velocidad"
T("cap6", S, "¿Por qué es fácil dejarse cegar por la velocidad?",
  96, "Es fácil acostumbrarse a las velocidades altas", "dejarse engañar y cegarse por la velocidad.")
T("cap6", S, "¿Qué distancia se necesita para detenerse a 50 y a 100 km/h con buen pavimento seco?",
  96, "Cuando vas a detenerte es cuando notas la velocidad.", "cuando aumentes la velocidad.")
T("cap6", S, "¿Cómo debe ser siempre la velocidad razonable y prudente?",
  96, "Si todas las personas respetaran los límites de velocidad", "ante cualquier obstáculo o imprevisto.")
T("cap6", S, "¿Cuáles son las velocidades máximas permitidas en Chile?",
  96, "Las velocidades máximas permitidas varían", "ni los buses interurbanos a más de 100 km/h.")
T("cap6", S, "¿Puede la autoridad modificar los límites de velocidad?",
  96, "No obstante, la autoridad puede modificar los límites", "instalando las señales correspondientes.")
T("cap6", S, "¿En qué situaciones se debe reducir obligatoriamente la velocidad?",
  96, "En zonas densamente pobladas.", "Cuando el pavimento esté resbaladizo.")
T("cap6", S, "¿Qué otras situaciones obligan a reducir la velocidad?",
  97, "Cuando te acerques a un vehículo de locomoción colectiva", "mientras estés en una Zona de Tránsito Calmado.")
T("cap6", S, "¿A qué velocidad debes circular por las afueras de un colegio en horario de entrada y salida?",
  97, "Debes reducir tu velocidad a no más de 30 km/h", "durante las horas de entrada y salida de clases.")
T("cap6", S, "¿Qué significa la conducción a la defensiva?",
  97, "Conduces con precaución.", "Miras primero y conduces después.")
T("cap6", S, "¿Qué significa una velocidad adecuada en situaciones arriesgadas?",
  97, "Una velocidad adecuada significa que, en situaciones arriesgadas", "aunque las normas no te lo exijan.")
T("cap6", S, "¿A qué condiciones debes adaptar tu velocidad?",
  97, "Y no olvides que debes adaptar tu velocidad", "así como el cálculo de distancias.")
T("cap6", S, "¿Qué son los peligros ocultos?",
  97, "Tienes que poder detenerte ante cualquier obstáculo imaginable.", "Esta es una capacidad que hay que entrenar.")
T("cap6", S, "¿Cómo influye el estado de la carretera en la distancia de frenado?",
  98, "Tienes que adaptar tu velocidad a las condiciones y aspecto", "Conduce con máxima atención para lograr visualizar los peligros.")
T("cap6", S, "¿Cómo se debe tomar una curva?",
  98, "Disminuye tu velocidad antes de llegar a una curva.", "para retomar la velocidad al salir de la curva.")

S = "Encuentros y adelantamientos"
T("cap6", S, "¿A qué velocidad se aproximan dos vehículos que circulan en sentido contrario?",
  98, "Si dos vehículos circulan en sentido contrario", "de las velocidades de cada uno.")
T("cap6", S, "¿Qué error se comete al estimar dónde se producirá el cruce con otro vehículo?",
  98, "Con frecuencia, erróneamente se estima que el cruce", "cuando los dos vehículos circulen a igual velocidad")
T("cap6", S, "¿Qué peligros existen en los encuentros con vehículos que vienen en sentido contrario?",
  99, "Un vehículo que viene en una fila en sentido contrario", "No frenes bruscamente dejándote llevar por el pánico.")
T("cap6", S, "¿Qué sugerencias existen para los encuentros con otros vehículos?",
  99, "Los vehículos que vienen en sentido contrario constituyen siempre un peligro.", "Reduce los riesgos de siniestro conduciendo a velocidad más baja.")
T("cap6", S, "¿Quién debe ceder el paso cuando hay obstáculos fijos en la calzada?",
  100, "Como regla general en estos casos", "como ejemplo, la presencia de un banderero.")
T("cap6", S, "¿Qué preguntas debes hacerte antes de adelantar a otro vehículo?",
  100, "¿Qué gano con adelantar?", "¿A qué velocidad puedo hacer el adelantamiento?", 2)
T("cap6", S, "¿Qué debes suponer siempre del vehículo que viene en sentido contrario al adelantar?",
  101, "Siempre que un vehículo venga en sentido contrario", "este puede aumentar su velocidad.")
T("cap6", S, "¿Qué ocurre al adelantar a 90 km/h con un vehículo a 350 metros que viene a 90 km/h?",
  101, "Analicemos el caso de la siguiente imagen", "El siniestro es un hecho.")
T("cap6", S, "¿Qué debes hacer cuando vayas a adelantar?",
  101, "Mira lejos hacia adelante y prepárate.", "un vehículo puede aparecer por una vía lateral.")
T("cap6", S, "¿Qué precaución exige adelantar a un vehículo de gran tamaño?",
  101, "Cuando vayas a adelantar a un vehículo de gran tamaño", "adelantar un vehículo largo es más arriesgado.")
T("cap6", S, "¿Qué debes hacer durante el adelantamiento?",
  102, "Trata de adelantar rápidamente sin sobrepasar el límite", "Señaliza tu intención de regresar a la pista de la derecha.")
T("cap6", S, "¿Qué debes hacer al finalizar el adelantamiento?",
  102, "Vuelve hacia tu derecha una vez que veas", "Vuelve a la velocidad normal.")
T("cap6", S, "¿Cómo debes actuar cuando te adelantan?",
  102, "Facilita el adelantamiento manteniéndote lo más a la derecha posible.", "desplázate lo más que puedas a la derecha.")
T("cap6", S, "¿En qué casos no debes adelantar traspasando el eje o línea central de la calzada?",
  103, "No dispongas de un espacio libre hacia delante", "Un vehículo que marcha detrás tuyo haya iniciado un adelantamiento.")
T("cap6", S, "¿En qué dos situaciones puedes adelantar por la derecha?",
  103, "Solo puedes adelantar a un vehículo por la derecha", "con tres o más pistas de circulación con un mismo sentido del tránsito.")
T("cap6", S, "¿Qué es una maniobra de sobrepaso y en qué se diferencia del adelantamiento?",
  103, "Las normas vigentes distinguen estos adelantamientos", "No debes efectuar esta maniobra de sobrepaso fuera de la calzada.")
T("cap6", S, "¿En qué condición pueden ciclos, motocicletas y motonetas sobrepasar en la misma pista?",
  103, "Es importante mencionar que las personas conductoras de ciclos", "siempre que los vehículos sobrepasados se encuentren detenidos.")

S = "Estacionamiento y detención"
T("cap6", S, "¿Dónde debes estacionar cuando no hay lugares habilitados fuera de la vía pública?",
  104, "No debes estacionar ni detener tu vehículo donde pueda constituirse", "podrás estacionar al lado izquierdo.")
T("cap6", S, "¿A qué distancia de la cuneta y de otros vehículos debes estacionar?",
  104, "A menos que esté permitida otra forma de estacionamiento", "de 60 centímetros respecto de otros vehículos estacionados.")
T("cap6", S, "¿Cómo se estaciona en caminos o vías rurales?",
  104, "En los caminos o vías rurales, estaciona de modo", "y lo más cerca de la cuneta que puedas.")
T("cap6", S, "¿Qué no debes olvidar al estacionar?",
  104, "En las vías con cierta inclinación", "ni animales dentro del vehículo.")
T("cap6", S, "¿En qué lugares está prohibido estacionar y detenerse?",
  104, "Donde las señales oficiales lo prohíban.", "En las calzadas o bermas de caminos públicos de 2 o más pistas de circulación en un mismo sentido.")
T("cap6", S, "¿En qué lugares no debes estacionar?",
  105, "Donde exista línea amarilla continua pintada a lo largo de la solera.", "posta de primeros auxilios y hospitales.")
T("cap6", S, "¿A qué distancia de una esquina, recintos militares, paradas y cruces ferroviarios no debes estacionar?",
  106, "A menos de 10 metros de una esquina.", "A menos de 20 metros de un cruce ferroviario a nivel.")
T("cap6", S, "¿Puedes estacionar en un lugar reservado a otro vehículo?",
  106, "Podrás estacionar en un lugar reservado a otro vehículo", "sólo por el tiempo mínimo para tomar o dejar pasajeros.")
T("cap6", S, "¿Qué debes hacer al estacionar de noche o con escasa visibilidad?",
  106, "Cuando siendo de noche estaciones en una vía sin alumbrado público", "manteniendo siempre encendidas tus luces de estacionamiento.")
T("cap6", S, "¿Qué medidas debes adoptar en un estacionamiento por emergencia?",
  106, "Cuando accidentalmente por averías, fallas mecánicas", "mantén activadas tus luces de advertencia de peligro.")
T("cap6", S, "¿Qué características debe tener el chaleco de alta visibilidad?",
  106, "Si desciendes del vehículo, siempre debes utilizar un chaleco", "de un ancho no inferior a 50 milímetros.")
T("cap6", S, "¿En qué casos se puede conducir marcha atrás?",
  106, "No debes conducir marcha atrás, a menos que ello sea indispensable", "Para estacionar.")
T("cap6", S, "¿Puedes retroceder dentro de un cruce?",
  107, "Sin embargo, no debes retroceder en un cruce", "a menos que recibas una indicación expresa de Carabineros.")
T("cap6", S, "¿Qué debes verificar antes de retroceder?",
  107, "Antes de retroceder verifica que no haya peatones", "No te confíes de los espejos para juzgar la distancia que tienes detrás.")
T("cap6", S, "¿Qué distancia de seguridad debes mantener al detenerte detrás de otro vehículo esperando luz verde?",
  105, "Cuando te detengas detrás de un vehículo esperando la luz verde", "si puedes ver los neumáticos traseros del vehículo de delante.")

S = "Cruces ferroviarios"
T("cap6", S, "¿Cómo debes cruzar un cruce ferroviario?",
  107, "Respeta la señalización de los cruces ferroviarios", "apaga la radio de tu vehículo en caso de llevarla encendida.")
T("cap6", S, "¿Cuánta distancia necesita un tren que marcha a 100 km/h para detenerse?",
  107, "Recuerda que los trenes no pueden detenerse fácilmente.", "necesitará entre 800 a 1.000 metros para detenerse.")
T("cap6", S, "¿Quién tiene siempre la preferencia en un cruce ferroviario?",
  107, "El tren tiene siempre la preferencia", "como persona conductora de un vehículo.")
T("cap6", S, "¿Qué hacer si ya comenzaste a cruzar y se activan las señales del cruce ferroviario?",
  107, "Si ya has comenzado a cruzar y se activan las señales", "no te detengas.")
T("cap6", S, "¿A qué distancia de un cruce ferroviario no debes estacionar ni adelantar?",
  107, "Nunca pases un cruce ferroviario si no dispones de espacio", "ni a menos de 200 metros de él.")
T("cap6", S, "¿Qué hacer si tu vehículo se descompone en un cruce ferroviario?",
  107, "Haz salir a todas las personas del vehículo.", "En caso contrario, sal del cruce.")

# ---------------------------------------------------------------------------
# Capítulo 7 · Conducción en circunstancias especiales
# ---------------------------------------------------------------------------
S = "Conducción en la oscuridad"
T("cap7", S, "¿Por qué es mayor el riesgo de siniestro durante la noche?",
  109, "El riesgo de siniestro es mayor durante la noche", "reduce la velocidad o detén el vehículo de ser necesario.")
T("cap7", S, "¿Cómo afecta la oscuridad al cálculo de distancias?",
  109, "Nuestra capacidad de calcular distancias depende", "cuando desees adelantar a otro vehículo.")
T("cap7", S, "¿De qué depende descubrir un obstáculo al conducir en la oscuridad?",
  109, "La potencia y ajuste de tus luces.", "La potencia de las luces del vehículo que viene en sentido contrario.")
T("cap7", S, "¿Qué debes hacer para prevenir siniestros al conducir de noche?",
  109, "Para prevenir siniestros, aumenta la distancia", "y los que te anteceden.")
T("cap7", S, "¿En qué horario y con qué luces deben circular obligatoriamente los vehículos?",
  110, "Para poder ver y ser visible, desde media hora después", "oportunamente percibidos por las y los peatones y demás personas conductoras.")
T("cap7", S, "¿Con qué luces se debe circular siempre en vías interurbanas?",
  110, "En vías interurbanas, aun cuando no esté oscuro", "debes circular siempre con tus luces encendidas.")
T("cap7", S, "¿Se puede circular con las luces de estacionamiento encendidas?",
  110, "En ningún caso podrás circular con las luces de estacionamiento encendidas.")
T("cap7", S, "¿Cuál es la distancia de visibilidad según la ropa y el tipo de luces?",
  110, "ropas oscuras ropas claras ropas con reflectante", "con luces altas")
T("cap7", S, "¿Cómo debes manejar las luces al encontrarte con otro vehículo en la oscuridad?",
  111, "Al encontrarse en la oscuridad y en una vía no urbana", "Dirige tu mirada a lo lejos hacia el borde derecho de la calzada.")
T("cap7", S, "¿Es necesario bajar las luces al cruzarse con peatones?",
  111, "No es necesario que bajes las luces cuando te cruces con peatones.")
T("cap7", S, "¿Con cuánta anticipación debes bajar las luces en un encuentro?",
  111, "Baja tus luces con anticipación suficiente", "todo el espacio entre los dos vehículos debe encontrarse iluminado.")
T("cap7", S, "¿Cuándo debes volver a las luces altas en un encuentro?",
  111, "También es importante que cambies a luces altas", "ya que tu visibilidad se encuentra limitada.")
T("cap7", S, "¿Por qué debes anticipar más el cambio de luces al cruzarte con un bus o camión?",
  111, "Si la carretera es ancha, puedes esperar más antes de cambiar", "que las que conducen automóviles o motocicletas.")
T("cap7", S, "¿Cómo debes manejar las luces en un adelantamiento nocturno?",
  111, "Cuando alcances a un vehículo que va delante", "que no alcanzarías a descubrir si va con luces bajas.")
T("cap7", S, "¿Cómo debes ayudar cuando otro vehículo te adelanta de noche?",
  112, "Cuando te adelanten, ayuda a quien lo está haciendo", "deben iluminar la vía a ambos durante el adelantamiento.")
T("cap7", S, "¿Qué luces debes encender al estacionar en una vía pública sin alumbrado?",
  112, "Cuando estaciones en una vía pública sin alumbrado", "enciende también las luces intermitentes.")
T("cap7", S, "¿Qué luces llevan los vehículos de carga y de locomoción colectiva?",
  112, "Los vehículos de carga y de locomoción colectiva llevan", "en los extremos de su parte superior trasera.")
T("cap7", S, "¿Qué luces llevan motocicletas, motonetas, triciclos y bicicletas?",
  112, "Parte delantera: un foco que proyecta luces altas y bajas.", "Parte trasera: luz roja fija.")
T("cap7", S, "¿De qué color son las luces que los vehículos proyectan hacia adelante y hacia atrás?",
  113, "Ten presente que todas las luces que los vehículos proyectan", "que pueden ser rojas o amarillas (ámbar).")
T("cap7", S, "¿Qué son las huinchas retrorreflectantes y dónde se ubican?",
  113, "Otro elemento que, aunque no son luces", "ruedas, parte trasera y horquillas delanteras y traseras.")
T("cap7", S, "¿Se pueden usar luces altas al conducir de noche en zona urbana con alumbrado público?",
  113, "Al conducir por una zona urbana que posea alumbrado público", "no siempre son lo suficientemente visibles.")

S = "Conducción con carga"
T("cap7", S, "¿Cómo modifica una carga pesada la maniobrabilidad del vehículo?",
  113, "Una carga pesada puede modificar la maniobrabilidad", "y necesitarás más espacio para adelantar.")
T("cap7", S, "¿Qué ocurre con una carga pesada en la parte posterior o delantera del automóvil?",
  113, "Con una carga pesada en la parte posterior de tu automóvil", "una distribución más uniforme de la carga.")
T("cap7", S, "¿Qué precauciones exige poner carga en el interior del vehículo?",
  114, "Al poner carga en el interior de tu vehículo no obstruyas", "pueden se pueden mover hacia adelante, transformarse en proyectiles.")
T("cap7", S, "¿Qué importancia tienen los neumáticos al llevar carga extra?",
  114, "Al llevar carga extra, la presión y tamaño adecuado", "Consulta para ello el manual del vehículo o a quien te lo vendió.")
T("cap7", S, "¿Qué no debes olvidar al transportar carga?",
  114, "Controlar las sujeciones de la parrilla.", "Ten en consideración la estabilidad del vehículo y la resistencia del techo.")
T("cap7", S, "¿Qué remolque permite conducir la Licencia Clase B?",
  114, "La Licencia de Conducir Clase B te permite conducir tu automóvil con un remolque", "el peso total no supere los 3.500 kilogramos.")
T("cap7", S, "¿Qué precaución exigen los espejos al conducir con remolque?",
  114, "Por lo general, los remolques son más anchos que los autos.", "Mientras arrastres el remolque, mira siempre tus espejos retrovisores.")
T("cap7", S, "¿Desde qué capacidad de carga deben poseer frenos los remolques?",
  115, "Cuando los remolques tienen capacidad de carga superior a 750 kilogramos", "un vehículo de arrastre con enchufe para frenos eléctricos.")
T("cap7", S, "¿Qué freno adicional deben tener los remolques con frenos?",
  115, "Además, los remolques con frenos deben poseer uno para casos de emergencia", "al romperse el dispositivo de arrastre.")
T("cap7", S, "¿Qué ocurre si la presión sobre la bola de arrastre es baja o excesiva?",
  115, "Cuando la presión sobre la esfera es baja o nula", "cegar a las personas conductoras que vienen en sentido contrario.")
T("cap7", S, "¿Qué debes controlar antes de comenzar a conducir con remolque?",
  115, "La carga en el remolque esté bien distribuida", "El sistema de frenos funcione.")
T("cap7", S, "¿Qué hacer si el remolque comienza a zigzaguear?",
  115, "Si el remolque comienza a zigzaguear suelta el acelerador", "hasta que recuperes la estabilidad y puedas seguir tu ruta.")

S = "Conducción en autopistas"
T("cap7", S, "¿Qué exige la conducción en autopistas y autovías?",
  116, "En las autopistas y autovías los vehículos circulan a velocidades más altas", "que en otras calles o caminos.")
T("cap7", S, "¿De qué debes asegurarte antes de circular por una autopista?",
  116, "Cuando vayas a circular por una autopista, asegúrate", "luces y focos estén limpios.")
T("cap7", S, "¿Qué es la pista de aceleración y quién tiene la prioridad al ingresar a la autopista?",
  116, "Para ingresar a las autopistas existe una pista especial", "detente hasta que esta se produzca.")
T("cap7", S, "¿Qué debes hacer una vez que abandonas la pista de aceleración?",
  116, "Usa tus espejos y, para asegurarte, corrobora volteando tu cabeza", "acostumbrarte a la velocidad del resto, antes de sobrepasar.")
T("cap7", S, "¿Cómo se paga el uso de algunas autopistas?",
  116, "En algunas autopistas, el peaje por utilizarlas es a través", "sin contar con un sistema de pago es sancionado.")
T("cap7", S, "¿Cómo debes conducir dentro de la autopista?",
  116, "Cuando tengas buena visibilidad y las condiciones de la vía sean buenas", "cuando se conduce a velocidades altas.")
T("cap7", S, "¿Cómo puedes facilitar el acceso de los vehículos que van a entrar a la autopista?",
  116, "Aligerando la presión sobre el acelerador y dejando pasar", "Cambiándote de pista.", 2)
T("cap7", S, "¿Por qué la conducción en autopista genera cansancio y ceguera por velocidad?",
  117, "Las carreteras buenas y rápidas no tienen sólo ventajas.", "constantemente controles tu velocidad mirando el velocímetro.")
T("cap7", S, "¿En qué casos puedes detenerte en una autopista?",
  117, "No te detengas en una autopista, a menos que:", "Te lo solicite Carabineros.")
T("cap7", S, "¿Puedes estacionar o recoger personas en una autopista?",
  117, "No te estaciones en una autopista, incluidas sus bermas", "a menos que se trate de una emergencia.")
T("cap7", S, "¿Qué debes hacer si tu vehículo presenta una falla mecánica en una autopista?",
  117, "Si tu vehículo presenta un problema sal de la autopista", "llamar a un Servicio de Emergencia o a Carabineros.")
T("cap7", S, "¿Qué hacer si no puedes llegar con tu vehículo a la berma?",
  118, "Enciende tus luces destellantes de advertencia de peligro.", "ni intentes realizar la más mínima reparación.")
T("cap7", S, "¿Cómo se sale correctamente de una autopista?",
  118, "A menos que las señales te indiquen que una pista", "y disminuye tu velocidad cuando sea necesario.")
T("cap7", S, "¿Cómo se distingue la pista de desaceleración y por qué hay que reducir la velocidad al salir?",
  118, "La pista de desaceleración para salir de la autopista se distingue", "es fundamental que reduzcas tu velocidad.")
T("cap7", S, "¿Qué precauciones exige la circulación por túneles?",
  118, "Cuando debas circular por un túnel, asegúrate de tener combustible", "recuerda apagar el motor de tu vehículo.", 2)
T("cap7", S, "¿Qué hacer si tu vehículo sufre un desperfecto dentro de un túnel?",
  119, "Enciende tus luces de emergencia.", "Sigue las instrucciones del personal del túnel.")
T("cap7", S, "¿Qué hacer en caso de incendio de tu vehículo dentro de un túnel?",
  119, "Si es posible, sal del túnel.", "solicita ayuda desde un teléfono de emergencia.")

S = "Conducción en distintas condiciones climáticas"
T("cap7", S, "¿Cuál es la primera regla de seguridad ante condiciones climáticas desfavorables?",
  120, "Cuando las condiciones climáticas son desfavorables", "asegúrate de que el vehículo se encuentra en perfecto estado.")
T("cap7", S, "¿Por qué es con las primeras gotas de lluvia cuando más precauciones hay que tomar?",
  120, "Sin embargo, es con las primeras gotas de lluvia", "ante las primeras señales de agua en el camino.")
T("cap7", S, "¿Cómo afecta la lluvia a la adherencia de los neumáticos?",
  120, "En estas circunstancias, se reduce la adherencia", "la lluvia provoca que se reduzca tu visibilidad.")
T("cap7", S, "¿Qué medidas mejoran la adherencia y previenen deslizamientos con lluvia?",
  121, "Comprueba frecuentemente si los frenos responden", "para paliar la disminución de adherencia de los neumáticos.")
T("cap7", S, "¿Qué es el aquaplaning o hidroplaning?",
  121, "Cuando la lluvia es muy intensa, sobre la calzada se forma", "no obedeciéndole la dirección ni los frenos.")
T("cap7", S, "¿Cómo se evita el aquaplaning?",
  121, "A mayor velocidad, mayor es la cantidad de agua", "no frenar ni acelerar innecesariamente.")
T("cap7", S, "¿Qué hacer cuando hay charcos de agua en la calzada?",
  121, "Evita pasar por ellos, ya sea dejándolos entre las ruedas", "no mojar a peatones ni a ciclistas.")
T("cap7", S, "¿Cómo circular cuando la calzada está anegada?",
  122, "Si no tienes alternativa y te ves en la obligación de pasar", "Si no funcionan bien, sécalos frenando suavemente.")
T("cap7", S, "¿Qué medidas mejoran la visibilidad con lluvia?",
  122, "Mantén limpio el parabrisas, la luneta trasera y todas tus luces.", "Recuerda mantener tus luces siempre encendidas.")
T("cap7", S, "¿Por qué la nieve recién caída es peligrosa?",
  122, "Cuando caen los primeros copos de nieve la conducción es tan peligrosa", "sus efectos son similares a los del hielo.")
T("cap7", S, "¿Qué medidas se deben adoptar para conducir con nieve?",
  123, "Como norma general, cuando haya nieve conduce lentamente", "está más dura y es posible que haya hielo.")
T("cap7", S, "¿Qué medidas mejoran la visibilidad con nieve?",
  123, "Acciona los limpiaparabrisas y, si el vehículo posee", "es indispensable agregar anticongelante al líquido lavador.")
T("cap7", S, "¿Se deben encender las luces altas cuando está nevando?",
  124, "Aunque sea de noche, no conviene encender las luces altas", "con posibilidad de provocar un deslumbramiento.")
T("cap7", S, "¿Dónde es más probable que la calzada esté helada?",
  124, "En los días fríos y húmedos, las sombras que proyectan", "tienden a congelarse mucho antes que el resto del camino.")
T("cap7", S, "¿Cómo puedes verificar que la calzada está con hielo?",
  124, "Si notas que la dirección del vehículo está excesivamente ligera", "frenando en forma suave mientras conduces lentamente.")
T("cap7", S, "¿Cuánto puede aumentar la distancia de frenado con la calzada helada?",
  124, "Hay que resaltar que cuando la calzada está helada", "y evitando frenar.")
T("cap7", S, "¿Existe algún elemento que permita conducir con seguridad sobre hielo o nieve?",
  124, "Como norma general, ten en cuenta que no existe ningún elemento", "o bien, circulando con cadenas.")
T("cap7", S, "¿Cómo afecta la niebla a la visibilidad y a la adherencia?",
  125, "Este fenómeno reduce la visibilidad.", "existe peligro de deslizamiento igual que cuando comienza a llover.")
T("cap7", S, "¿Qué luces se deben usar con niebla y cuáles no?",
  125, "Mantén encendidas tus luces bajas.", "úsalas sólo cuando la niebla es espesa, ya que podrías deslumbrar.")
T("cap7", S, "¿Qué otras medidas se deben adoptar con niebla?",
  125, "Aumenta tu distancia de seguridad en relación al vehículo de adelante.", "la falta de visibilidad puede provocar siniestros.")
T("cap7", S, "¿Qué riesgo implica el viento fuerte y qué medidas se deben adoptar?",
  125, "El viento fuerte, principalmente cuando en caminos de montaña", "debes mantener una distancia lateral segura.")

# ---------------------------------------------------------------------------
# Capítulo 8 · Conducción eficiente
# ---------------------------------------------------------------------------
S = "Conducción eficiente"
T("cap8", S, "¿Qué se entiende por Conducción Eficiente?",
  127, "Utilizamos el concepto de Conducción Eficiente", "un mayor rendimiento energético en tu vehículo.")
T("cap8", S, "¿Cuánto permite reducir el consumo de combustible aplicar técnicas de Conducción Eficiente?",
  127, "Diversos estudios realizados por la Agencia Chilena de Eficiencia Energética", "un 15% el consumo de combustible.")
T("cap8", S, "¿Cómo incide la Conducción Eficiente en el consumo y en el medio ambiente?",
  127, "Los beneficios de la Conducción Eficiente se manifiestan", "de la acumulación de gases en la atmósfera.")
T("cap8", S, "¿Por qué conviene planificar el recorrido antes de partir?",
  128, "Lo primero que se debes considerar para tener una conducción eficiente", "obtener un mejor rendimiento.")
T("cap8", S, "¿Qué significa que la eficiencia energética no es hacer menos?",
  128, "Te recomendamos preparar con antelación las cosas", "si en uno puedes hacer todos los trámites?")
T("cap8", S, "¿Cómo debe usarse el GPS de forma segura y eficiente?",
  128, "Si tienes un GPS o tu teléfono celular cuenta con uno", "escucha las indicaciones del GPS a través del audio de cada aplicación.")
T("cap8", S, "¿Cómo influye el peso del vehículo en el consumo de combustible?",
  128, "Para mover una carga más grande se necesita más fuerza", "donde no impliquen un gasto de energía.")
T("cap8", S, "¿Cuánto puede aumentar el consumo por llevar portaequipajes en el techo?",
  129, "Los equipos portaequipajes y bultos en el techo tienen otro efecto", "el consumo se puede incrementar por sobre un 20% en carretera")
T("cap8", S, "¿Con qué frecuencia se debe revisar la presión de los neumáticos y dónde se encuentra el valor correcto?",
  129, "Es necesario revisar la presión de tus neumáticos regularmente", "en las vacaciones u otras salidas fuera de la ciudad.")
T("cap8", S, "¿Cuánto puede aumentar el consumo una reducción de 5 PSI en los neumáticos?",
  129, "Se estima que una reducción en 5 PSI del nivel óptimo", "el consumo de combustible en un 3%")
T("cap8", S, "¿Cuáles son los beneficios de un buen mantenimiento?",
  130, "Permite conducir de forma segura.", "Mayor disponibilidad del vehículo.")
T("cap8", S, "¿Cuánto puede incrementar el consumo un filtro de combustible o de aire en mal estado?",
  130, "Además de los neumáticos, existen otros elementos clave", "parte del recurso energético no se aprovechará.")
T("cap8", S, "¿Se debe pisar el acelerador al encender el motor?",
  130, "Cuando enciendas el motor, prefiere no pisar el acelerador", "la partida e inyección de combustible hacia el motor.")
T("cap8", S, "¿Cómo se debe acelerar para una conducción eficiente?",
  131, "Evita acelerar a fondo.", "que una que lo hace de forma paulatina.")
T("cap8", S, "¿Cuánto se reduce el rendimiento de combustible a altas velocidades?",
  131, "Si bien en carreteras se permiten límites de velocidad", "¿Valdrá la pena incrementar tanto el consumo por unos cuantos minutos?")
T("cap8", S, "¿Qué marchas conviene usar para no exigir el motor?",
  131, "Un motor exigido a mayores revoluciones tendrá un mayor consumo", "donde se alcanza el mayor rendimiento.")
T("cap8", S, "¿Qué ocurre con la caja de cambios automática si se acelera a fondo?",
  131, "Este consejo sólo es aplicable si el vehículo que conduces", "lo que finalmente aumenta el consumo.")
T("cap8", S, "¿Por qué mantener una distancia prudente ahorra combustible?",
  131, "Para determinar la distancia necesaria respecto del vehículo", "es necesario mantener una distancia prudente.")
T("cap8", S, "¿Cómo se determina una distancia prudente?",
  132, "Entonces, ¿cuál sería una distancia prudente?", "del capítulo Normas de circulación (página 87).")
T("cap8", S, "¿Por qué conviene frenar con anticipación?",
  132, "A fin de reducir el consumo energético, se recomienda frenar", "disminuirá el tiempo que mantienes el pie en el acelerador sin necesidad.")
T("cap8", S, "¿Cómo se debe reducir la velocidad al ver un semáforo en rojo o una señal PARE?",
  132, "Si ves un semáforo en rojo o una señal PARE", "si lo adoptas como práctica.")
T("cap8", S, "¿Cuándo conviene apagar el motor del vehículo?",
  133, "Es común que durante el viaje se produzcan detenciones", "en este caso, no conviene apagar el motor.")
T("cap8", S, "¿Qué prima en adelantamientos y situaciones de emergencia?",
  133, "En estas situaciones debe primar la seguridad por sobre la economía", "no se ponga en riesgo la seguridad propia o de terceros.")
T("cap8", S, "¿Cuál es la base de la Conducción Eficiente?",
  134, "No es coincidencia que los principios de una conducción segura", "lo que implica una reducción en el consumo.")
T("cap8", S, "¿Qué principios fomentan a la vez la seguridad y la eficiencia?",
  134, "Atención a las condiciones que rodean a la persona conductora", "como la del resto de las personas usuarias de las vías.")

# ---------------------------------------------------------------------------
# Capítulo 9 · Informaciones importantes
# ---------------------------------------------------------------------------
S = "Cómo comportarse en caso de siniestro"
T("cap9", S, "¿Qué obligaciones tiene toda persona que participa en un siniestro con lesionados o fallecidos?",
  136, "Toda persona, con culpa o sin ella, que participe en un siniestro", "dar cuenta a la autoridad policial más cercana.")
T("cap9", S, "¿Cómo se sanciona el incumplimiento de detenerse y dar aviso?",
  136, "El incumplimiento de lo anterior será sancionado", "y penas de cárcel efectiva.")
T("cap9", S, "¿Qué sanción tiene darse a la fuga y no dar aviso a la autoridad?",
  136, "El darse a la fuga y no dar aviso a la autoridad policial", "penas de cárcel efectiva de al menos un año.")
T("cap9", S, "¿Qué precauciones debes tomar al detenerte a ayudar en un siniestro?",
  136, "Al detenerte para ayudar, debes saber que tanto las colisiones", "con un material aislante de color naranjo.")
T("cap9", S, "¿A qué números de emergencia debes llamar y qué información entregar?",
  136, "El pánico, que con frecuencia se presenta en casos de siniestros", "y la cantidad de vehículos y de víctimas.")
T("cap9", S, "¿Se puede mover a las personas lesionadas del lugar del siniestro?",
  137, "Independiente de cómo se vean las personas, evita moverlas", "puedan ser atropelladas en la calzada.")
T("cap9", S, "¿Qué se debe hacer si la persona afectada es motociclista o ciclista con casco?",
  137, "Si la persona afectada es motociclista o ciclista con casco", "podrías provocar una lesión en la columna cervical.")
T("cap9", S, "¿Qué medidas básicas ayudan a una persona en shock?",
  137, "Producto de la gravedad de las lesiones, la persona lesionada", "por ningún motivo le des algo de comer o beber.")
T("cap9", S, "¿Qué significa la sigla XABCDE de los primeros auxilios?",
  137, "X: Control de hemorragias graves", "a una frecuencia de 1 cada 6 segundos.")
T("cap9", S, "¿Qué comprenden las etapas C, D y E de los primeros auxilios?",
  138, "C: Circulación", "que pueda prestar atención de salud.")
T("cap9", S, "¿Cómo actuar ante un siniestro con un vehículo que transporta cargas peligrosas?",
  138, "Frente a un siniestro de tránsito en que se vea involucrado un camión", "antes de llamar a los servicios de emergencia.")

S = "Disposiciones aplicables a los vehículos"
T("cap9", S, "¿Qué documentos debe portar un vehículo motorizado para circular?",
  139, "Los vehículos motorizados no pueden circular sin su placa patente", "los que deben encontrarse siempre vigentes.")
T("cap9", S, "¿Quién otorga las Placas Patentes Únicas y qué registro se lleva?",
  139, "Las Placas Patentes Únicas (PPU) son otorgadas", "medidas precautorias que afecten a los vehículos.")
T("cap9", S, "¿Qué establece la Ley Patente Cero Días?",
  139, "La Ley Patente Cero Días, vigente desde febrero del año 2023", "con sus Placas Patentes Únicas instaladas.")
T("cap9", S, "¿Qué es el permiso de circulación y qué se requiere para obtenerlo?",
  139, "El permiso de circulación corresponde a un impuesto", "el Seguro Obligatorio de Accidentes Personales (SOAP).")
T("cap9", S, "¿Qué cubre el Seguro Obligatorio de Accidentes Personales (SOAP)?",
  139, "El seguro obligatorio cubre los riesgos de muerte", "que emite la compañía aseguradora.")
T("cap9", S, "¿Qué comprende la revisión técnica?",
  139, "La revisión técnica es como el examen médico de tu vehículo.", "frenos, luces, neumáticos y combustión interna.")
T("cap9", S, "¿Cómo se determina el mes de la revisión técnica?",
  140, "Considerando que, a menos que se trate de vehículos nuevos", "Siempre debes verificar esta información en www.prt.cl.")
T("cap9", S, "¿Qué es el Certificado de Homologación Individual?",
  140, "En caso de vehículos nuevos, estos deben contar con su Certificado de Homologación", "y seguridad vigentes en el país.")

S = "Responsabilidad de la persona conductora"
T("cap9", S, "¿A qué no se limita la responsabilidad de la persona conductora?",
  140, "La responsabilidad de la persona conductora no se limita", "son partes esenciales para la Convivencia Vial.")
T("cap9", S, "¿Qué documento debes portar siempre y qué lo reemplaza si fue retenido?",
  141, "Como persona conductora tienes la obligación de portar siempre", "o una boleta de citación al Juzgado.")
T("cap9", S, "¿Qué prohíbe la Ley No Chat?",
  141, "La Ley No Chat prohíbe la conducción de un vehículo", "manipulación de un GPS, etc.")
T("cap9", S, "¿Qué detalla la normativa de la Ley No Chat?",
  141, "No se puede manipular, esto es, operar con una o ambas manos", "Durante el trayecto puede recibir instrucciones vía audio.")
T("cap9", S, "¿Qué es un sistema de manos libres?",
  141, "El sistema de manos libres es aquel que te permite utilizar", "sin descuidar la conducción.")
T("cap9", S, "¿Qué equipos NO se consideran manos libres?",
  141, "El reglamento de la Ley No Chat establece que no son \"manos libres\"", "o utilizar aplicaciones en dichos dispositivos o artefactos.")
T("cap9", S, "¿Qué hacer si recibes una llamada y no cuentas con manos libres?",
  141, "¡Recuerda! Es tu deber conducir con toda tu atención", "debes buscar un lugar seguro para detenerte y atenderla.")
T("cap9", S, "¿En qué condiciones puede una persona de 17 años obtener Licencia Clase B?",
  142, "Excepcionalmente, una persona de 17 años puede obtener una Licencia Clase B", "de no menos de 5 años de antigüedad.")
T("cap9", S, "¿En qué aspectos puede restringirse una Licencia de Conducir?",
  142, "Debes saber que tu Licencia de Conducir puede ser restringida", "no puedes manejar sin ellos.")
T("cap9", S, "¿Qué infracciones producen suspensión de la Licencia de Conducir y por cuánto tiempo?",
  142, "3 meses* 2 años* Entre 5 y 45 días*", "Exceder en más de 60 km/h un límite de velocidad máxima.")
T("cap9", S, "¿Qué acumulación de infracciones produce la suspensión de la licencia?",
  143, "De igual modo, una licencia es suspendida por la acumulación", "en un período de doce meses.")
T("cap9", S, "¿Cuáles son las infracciones o contravenciones gravísimas?",
  143, "No detenerse ante la luz roja de las señales luminosas", "Exceder entre 20 y 60 kilómetros por hora el límite de velocidad máxima.", 2)
T("cap9", S, "¿Cuáles son algunas de las infracciones graves?",
  143, "Conducir un vehículo en condiciones físicas o psíquicas deficientes.", "en una cuesta o en una curva del camino.", 2)
T("cap9", S, "¿Qué otras infracciones graves existen relacionadas con el vehículo y la circulación?",
  144, "Estacionar o detenerse en la calzada o berma", "de forma permanente, en sus vidrios y espejos laterales.")
T("cap9", S, "¿Cuáles son ejemplos de infracciones menos graves?",
  144, "Estacionar o detener un vehículo en lugares prohibidos", "o impidan el control sobre el sistema de dirección, frenos y de seguridad.")
T("cap9", S, "¿Qué son las infracciones leves?",
  145, "Son infracciones o contravenciones leves todas las demás transgresiones", "graves o menos graves.")
T("cap9", S, "¿Qué delitos de la Ley de Tránsito pueden ser sancionados con cárcel?",
  145, "Además, es importante que sepas que la Ley de Tránsito contempla delitos", "bajo la influencia de sustancias estupefacientes o psicotrópicas, entre otras.")
T("cap9", S, "¿Cómo se debe frenar fuerte en un vehículo CON frenos ABS?",
  145, "Debes pisar enérgicamente el pedal de freno, manteniendo la máxima presión", "No debes asustarte al notarlo.")
T("cap9", S, "¿Cómo se debe frenar fuerte en un vehículo SIN frenos ABS?",
  145, "Debes pisar enérgicamente el pedal de freno, reduciendo la fuerza", "recuperes la adherencia de tus neumáticos al pavimento.")
T("cap9", S, "¿Qué es recomendable en ambos casos al frenar fuerte?",
  145, "En ambos casos es recomendable pisar el embrague", "cuando las revoluciones sean muy bajas.")
T("cap9", S, "¿Qué debes hacer ante una falla total de frenos?",
  146, "Presionar y soltar el pedal varias veces.", "sujetar el volante firmemente.")

S = "Tránsito y medio ambiente"
T("cap9", S, "¿Qué contaminantes emiten los vehículos motorizados y qué efectos tienen?",
  147, "Óxido de carbono: Influye en el sistema cardíaco y vascular.", "Contribuye a la acidificación.")
T("cap9", S, "¿Cómo influye la forma de conducir en las emisiones de gases?",
  147, "La forma de conducir tiene gran importancia en las emisiones de gases.", "provoca también emisiones innecesarias que deben evitarse.")
T("cap9", S, "¿Qué indica un humo muy negro por el tubo de escape?",
  147, "Debes saber que si tu vehículo está emitiendo humo muy negro", "es probable que el filtro de aire esté sucio.")
T("cap9", S, "¿Cómo se puede contribuir positivamente al medio ambiente al conducir?",
  147, "Acelerando suavemente.", "Optar por la conducción de vehículos híbridos o eléctricos.", 2)
T("cap9", S, "¿Qué debes considerar al conducir un vehículo eléctrico?",
  148, "Asegúrate de que tu vehículo cuente con la etiqueta", "del Vehículo Eléctrico (servicios de emergencia)\".")

# ---------------------------------------------------------------------------
# Anexo 2 · Glosario
# ---------------------------------------------------------------------------
S = "Glosario"
T("anexo2", S, "¿Qué es la acera?", 162, "Acera: Parte de una vía", "destinada al uso de peatones.")
T("anexo2", S, "¿Qué es el adelantamiento?", 162, "Adelantamiento: Maniobra efectuada", "se sitúa adelante de otro u otros que le antecedían.")
T("anexo2", S, "¿Qué es una berma?", 162, "Berma: Faja lateral", "adyacente a la calzada de un camino.")
T("anexo2", S, "¿Qué es la calzada?", 162, "Calzada: Parte de una vía", "destinada al uso de vehículos y animales.")
T("anexo2", S, "¿Qué es un camino?", 162, "Camino: Vía rural", "destinada al uso de peatones, vehículos y animales.")
T("anexo2", S, "¿Qué es un ciclo según la Ley de Tránsito?", 162, "Ciclo: Vehículo no motorizado", "para los efectos de la ley como vehículos no motorizados.")
T("anexo2", S, "¿Qué es una ciclovía?", 162, "Ciclovía: Espacio destinado al uso exclusivo de ciclos", "que puede estar segregado física o visualmente.")
T("anexo2", S, "¿Qué es una persona conductora?", 162, "Conductora/conductor: Toda persona que conduce", "de un animal de silla, de tiro o de arreo de animales.")
T("anexo2", S, "¿Qué es un cruce?", 162, "Cruce: La unión de una calle o camino con otros", "entre las líneas de edificación o deslindes en su caso.")
T("anexo2", S, "¿Qué es un cruce regulado?", 162, "Cruce regulado: Cruce en que existe un semáforo", "o donde está Carabineros dirigiendo el tránsito.")
T("anexo2", S, "¿Qué es la cuneta?", 162, "Cuneta: En calles, el ángulo formado", "el foso lateral de poca profundidad.")
T("anexo2", S, "¿Qué es una demarcación?", 163, "Demarcación: Símbolo, palabra o marca", "para guía del tránsito de vehículos y peatones.")
T("anexo2", S, "¿Qué es el derecho preferente de paso?", 163, "Derecho preferente de paso: Prerrogativa", "de un vehículo para proseguir su marcha.")
T("anexo2", S, "¿Qué es la detención según la Ley de Tránsito?", 163, "Detención: Paralización a que obligan", "pero sólo mientras dure esta maniobra.")
T("anexo2", S, "¿Qué es el eje de calzada?", 163, "Eje de calzada: La línea longitudinal a la calzada", "la división es en dos partes iguales.")
T("anexo2", S, "¿Qué significa estacionar?", 163, "Estacionar: Paralizar un vehículo en la vía pública", "por un período mayor que el necesario para dejar o recibir pasajeros.")
T("anexo2", S, "¿Qué es una intersección?", 163, "Intersección: Área común de calzadas", "que se cruzan o convergen.")
T("anexo2", S, "¿Qué es la línea de detención adelantada?", 163, "Línea de detención adelantada: Línea transversal", "zona de espera especial para personas conductoras de ciclos o motocicletas.")
T("anexo2", S, "¿Qué es la línea de detención de vehículos y dónde se entiende ubicada si no está demarcada?",
  163, "Línea de detención de vehículos: Línea transversal", "En otros cruces, justo antes de la intersección.")
T("anexo2", S, "¿Qué es la luz baja y a qué distancia permite visualizar obstáculos?",
  163, "Luz baja: Luz proyectada por los focos delanteros", "a una distancia no inferior a 50 metros.")
T("anexo2", S, "¿Qué es la luz alta y a qué distancia permite visualizar obstáculos?",
  163, "Luz alta: Luz proyectada por los focos delanteros", "a una distancia no inferior a 150 metros.")
T("anexo2", S, "¿Qué es un paso para peatones?", 164, "Paso para peatones: Senda de seguridad", "la prolongación imaginaria de las aceras.")
T("anexo2", S, "¿Qué es una pista de circulación?", 164, "Pista de circulación: Faja demarcada", "destinada al tránsito de una fila de vehículos.")
T("anexo2", S, "¿Qué es una pista de uso exclusivo?", 164, "Pista de uso exclusivo: Espacio de la calzada", "determinados por la autoridad correspondiente.")
T("anexo2", S, "¿Qué es un semáforo?", 164, "Semáforo: Dispositivo luminoso", "se regula la circulación de vehículos y peatones.")
T("anexo2", S, "¿Qué es una señal de tránsito?", 164, "Señal de tránsito: Dispositivos, signos y demarcaciones", "regular, advertir o encauzar el tránsito.")
T("anexo2", S, "¿Qué significa sobrepasar?", 164, "Sobrepasar: Maniobra mediante la cual un vehículo pasa a otro", "sin traspasar el eje de la calzada.")
T("anexo2", S, "¿Qué es un triciclo motorizado de carga?", 164, "Triciclo motorizado de carga:", "no podrá superar los 300 kilogramos de peso.")
T("anexo2", S, "¿Qué es un vehículo de emergencia?", 164, "Vehículo de emergencia: El perteneciente a Carabineros", "permiso otorgado por la autoridad competente.")
T("anexo2", S, "¿Qué es un vehículo de locomoción colectiva?", 164, "Vehículo de locomoción colectiva:", "exceptuados los taxis que no efectúen servicio colectivo.")
T("anexo2", S, "¿Qué es una zona de espera especial?", 165, "Zona de espera especial: Área señalizada", "en un cruce regulado con semáforo.")
T("anexo2", S, "¿Qué es una Zona de Tránsito Calmado y qué velocidades puede tener?",
  165, "Zona de Tránsito Calmado: Vía o conjunto de vías", "pudiendo estas ser de 40 km/h, 30 km/h o 20 km/h.")
T("anexo2", S, "¿Qué son la zona rural y la zona urbana?", 165, "Zona rural: Área geográfica que excluye las zonas urbanas.", "deben estar determinados y señalizados por las Municipalidades.")

# ---------------------------------------------------------------------------
# Anexo 3 · Proceso de obtención de la Licencia de Conducir
# ---------------------------------------------------------------------------
S = "Proceso de obtención de la Licencia de Conducir"
T("anexo3", S, "¿Qué se debe verificar antes de iniciar el proceso de obtención de la licencia?",
  168, "Si quieres obtener la Licencia de Conducir, lo primero que debes verificar", "debe ser obtenida en la comuna donde resides.")
T("anexo3", S, "¿Por qué conviene tomar el curso en la misma comuna donde se tramitará la licencia?",
  168, "Si realizas un curso en una Escuela de Conductores", "ellos te deben facilitar el vehículo para rendir el examen práctico de conducción.")
T("anexo3", S, "¿Qué exámenes y evaluaciones se realizan en la Municipalidad?",
  169, "En la Municipalidad te realizarán exámenes para determinar", "posteriormente, entregada a ti.")
T("anexo3", S, "¿Qué plazo tiene la Municipalidad para informar al Registro Civil?",
  169, "Luego de la emisión de la licencia, la Municipalidad tiene un plazo", "para incluir tu licencia al Registro de Conductores.")
T("anexo3", S, "¿Cuántas oportunidades hay por cada examen teórico y práctico?",
  169, "Se entiende que cada proceso comienza con la presentación", "dos oportunidades por cada examen teórico y práctico.")
T("anexo3", S, "¿Qué plazos existen para repetir los exámenes reprobados?",
  169, "En caso de reprobar alguno de los exámenes establecidos en la ley", "en un plazo no superior a 25 días hábiles desde la primera reprobación.")
T("anexo3", S, "¿Qué ocurre si no concurres dentro del plazo o vuelves a reprobar?",
  169, "Si trascurrido los plazos señalados no concurres", "se procede a la denegación de la concesión de la Licencia de Conducir.")
T("anexo3", S, "¿Cuánto hay que esperar tras una denegación para iniciar un nuevo proceso?",
  169, "Sin embargo, una vez que se produzca la primera denegación", "contado desde las respectivas denegaciones a la licencia.")
