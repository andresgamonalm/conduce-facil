"""Genera los archivos de datos que consume el aplicativo Conduce-Fácil.

Escribe en ``public/datos`` tres archivos JSON:

* ``estudio_conduce_facil.json``   tarjetas de estudio del Manual CONASET
* ``preguntas_conduce_facil.json`` banco de preguntas del Test de prueba
* ``senales_conduce_facil.json``   catálogo de señaléticas del Manual de Señalización

Todo el contenido proviene de los PDF oficiales incluidos en el repositorio.
"""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import contenido_estudio as ce  # noqa: E402
import contenido_preguntas as cp  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "public", "datos")
FIGURAS = os.path.join(RAIZ, "public", "assets", "manual")
SENALES = os.path.join(RAIZ, "public", "assets", "senales")
MANIFIESTO_SENALES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "manifiesto_senales.json"
)
MANIFIESTO_FIGURAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "manifiesto_figuras.json"
)

GRUPOS = [
    ("Reglamentarias", ("RPI", "RPO", "RR", "RO", "RA"),
     "Notifican prioridades, prohibiciones, restricciones, obligaciones y autorizaciones. Su transgresión constituye infracción."),
    ("Advertencia de peligro", ("PG", "PF", "PI", "PO", "PE"),
     "Advierten la existencia y naturaleza de riesgos o situaciones imprevistas en la vía o en sus zonas adyacentes."),
    ("Informativas", ("IP", "ID", "IV", "IE", "IS", "IT", "IO", "II"),
     "Orientan y guían a las personas usuarias para llegar a destino de la forma más segura, simple y directa."),
    ("Señalización transitoria", ("PT", "PTF", "ITD", "ITP", "ITO"),
     "Advierten peligros o entregan información cuando se realizan trabajos en la vía. Se caracterizan por ser de color naranja."),
    ("Mensajería variable", ("PMV",),
     "Señales de mensaje variable que informan condiciones cambiantes de la vía."),
]


def grupo_de(codigo: str) -> tuple[str, str]:
    prefijo = re.match(r"^([A-Z]+)-", codigo).group(1)
    for nombre, prefijos, descripcion in GRUPOS:
        if prefijo in prefijos:
            return nombre, descripcion
    return "Otras señales", ""


def cargar(ruta: str) -> list[dict]:
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    os.makedirs(DATOS, exist_ok=True)

    if ce.ERRORES or cp.ERRORES:
        for e in ce.ERRORES + cp.ERRORES:
            print("ERROR:", e)
        return 1

    # --- figuras del Manual CONASET agrupadas por página ---------------------
    figuras_por_pagina: dict[str, list[str]] = {}
    for fig in cargar(MANIFIESTO_FIGURAS):
        if not os.path.exists(os.path.join(FIGURAS, fig["archivo"])):
            continue
        figuras_por_pagina.setdefault(str(fig["pagina"]), [])
        if fig["archivo"] not in figuras_por_pagina[str(fig["pagina"])]:
            figuras_por_pagina[str(fig["pagina"])].append(fig["archivo"])

    tarjetas = []
    for t in ce.TARJETAS:
        tarjetas.append({**t, "figuras": figuras_por_pagina.get(str(t["pagina"]), [])[:4]})

    estudio = {
        "fuente": "Libro para la Conducción en Chile - Licencia Clase B, CONASET, julio 2024",
        "capitulos": ce.CAPITULOS,
        "tarjetas": tarjetas,
    }
    with open(os.path.join(DATOS, "estudio_conduce_facil.json"), "w", encoding="utf-8") as f:
        json.dump(estudio, f, ensure_ascii=False, separators=(",", ":"))

    preguntas = {
        "fuente": "Libro para la Conducción en Chile - Licencia Clase B, CONASET, julio 2024",
        "preguntas": cp.PREGUNTAS,
    }
    with open(os.path.join(DATOS, "preguntas_conduce_facil.json"), "w", encoding="utf-8") as f:
        json.dump(preguntas, f, ensure_ascii=False, separators=(",", ":"))

    # --- señaléticas ---------------------------------------------------------
    senales = []
    faltantes = []
    for s in cargar(MANIFIESTO_SENALES):
        if not os.path.exists(os.path.join(SENALES, s["archivo"])):
            faltantes.append(s["archivo"])
            continue
        grupo, descripcion = grupo_de(s["code"])
        senales.append(
            {
                "codigo": s["code"],
                "nombre": s["nombre"],
                "archivo": s["archivo"],
                "grupo": grupo,
                "fuente": s["fuente"],
                "pagina": s["pagina"],
            }
        )
    if faltantes:
        print("ERROR: faltan imágenes de señales:", faltantes[:10])
        return 1

    catalogo = {
        "fuente": "Manual de Señalización de Tránsito, Ministerio de Transportes y Telecomunicaciones",
        "grupos": [{"nombre": n, "descripcion": d} for n, _, d in GRUPOS],
        "senales": senales,
    }
    with open(os.path.join(DATOS, "senales_conduce_facil.json"), "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(",", ":"))

    con_fig = sum(1 for t in tarjetas if t["figuras"])
    print(f"Tarjetas de estudio : {len(tarjetas)} ({con_fig} con figuras del manual)")
    print(f"Preguntas del test  : {len(cp.PREGUNTAS)}")
    print(f"Señaléticas         : {len(senales)}")
    for nombre, _, _ in GRUPOS:
        print(f"   - {nombre}: {sum(1 for s in senales if s['grupo'] == nombre)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
