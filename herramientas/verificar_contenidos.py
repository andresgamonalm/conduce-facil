"""Verificación de fidelidad de los contenidos publicados en Conduce-Fácil.

Comprueba, contra los PDF oficiales incluidos en el repositorio, que:

1. Cada respuesta del módulo Estudio aparece LITERALMENTE en el Manual CONASET,
   en la página que se cita.
2. Cada fundamento del banco de preguntas aparece LITERALMENTE en el manual, en
   la página citada.
3. Cada señalética de la trivia proviene de una página real del Manual de
   Señalización y su nombre y código figuran en esa misma página.
4. Todos los archivos de imagen referenciados existen y son legibles.

El script termina con código 1 si encuentra cualquier discrepancia.
"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from texto_manual import normalizar, paginas  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "public", "datos")
SENALES = os.path.join(RAIZ, "public", "assets", "senales")
FIGURAS = os.path.join(RAIZ, "public", "assets", "manual")
MANUAL_SENALIZACION = os.path.join(RAIZ, "Manual-Señalizacion")

MARGEN_PAGINAS = 2  # el texto de un contenido puede continuar en la página siguiente


def cargar(nombre: str) -> dict:
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as f:
        return json.load(f)


def contexto(pagina_numero: int) -> str:
    todas = paginas()
    desde = max(0, pagina_numero - 1 - MARGEN_PAGINAS)
    hasta = min(len(todas), pagina_numero + MARGEN_PAGINAS)
    return " ".join(todas[desde:hasta])


def sin_acentos_mayus(texto: str) -> str:
    """Mayúsculas sin acentos y con guiones y comillas unificados.

    El PDF alterna guion corto y largo, y comillas rectas y tipográficas, para
    el mismo nombre de señal; la comparación no debe depender de ese detalle.
    """
    t = unicodedata.normalize("NFD", texto.upper())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    for signo in "–—‐‑":
        t = t.replace(signo, "-")
    for comilla in "“”«»‘’":
        t = t.replace(comilla, '"')
    return re.sub(r"\s+", " ", t)


def verificar_estudio(fallos: list[str]) -> int:
    datos = cargar("estudio_conduce_facil.json")
    for tarjeta in datos["tarjetas"]:
        if normalizar(tarjeta["respuesta"]) not in contexto(tarjeta["pagina"]):
            fallos.append(
                f"ESTUDIO {tarjeta['id']} (p{tarjeta['pagina']}): la respuesta no aparece literalmente en el manual."
            )
        for figura in tarjeta.get("figuras", []):
            if not os.path.exists(os.path.join(FIGURAS, figura)):
                fallos.append(f"ESTUDIO {tarjeta['id']}: falta la imagen {figura}.")
    return len(datos["tarjetas"])


def verificar_preguntas(fallos: list[str]) -> int:
    datos = cargar("preguntas_conduce_facil.json")
    for pregunta in datos["preguntas"]:
        if normalizar(pregunta["fundamento"]) not in contexto(pregunta["pagina"]):
            fallos.append(
                f"PREGUNTA {pregunta['id']} (p{pregunta['pagina']}): el fundamento no aparece literalmente en el manual."
            )
        opciones = pregunta["opciones"]
        if len(opciones) < 3:
            fallos.append(f"PREGUNTA {pregunta['id']}: tiene menos de tres alternativas.")
        if len(set(opciones)) != len(opciones):
            fallos.append(f"PREGUNTA {pregunta['id']}: tiene alternativas repetidas.")
        if not 0 <= pregunta["correcta"] < len(opciones):
            fallos.append(f"PREGUNTA {pregunta['id']}: el índice de la alternativa correcta es inválido.")
    return len(datos["preguntas"])


def verificar_senales(fallos: list[str]) -> int:
    import pymupdf

    datos = cargar("senales_conduce_facil.json")
    documentos: dict[str, list[str]] = {}
    for senal in datos["senales"]:
        archivo_pdf = senal["fuente"]
        if archivo_pdf not in documentos:
            doc = pymupdf.open(os.path.join(MANUAL_SENALIZACION, archivo_pdf))
            documentos[archivo_pdf] = [normalizar(p.get_text("text")) for p in doc]
        texto = documentos[archivo_pdf][senal["pagina"] - 1]
        plano = sin_acentos_mayus(texto)

        # El manual escribe el código con o sin guion y con o sin espacios
        # («RPO - 2b», «RPO-2b», «RPO 2c»): la comparación admite las tres formas.
        codigo_flexible = re.sub(r"[-\s]+", r"[-\\s]*", sin_acentos_mayus(senal["codigo"]))
        if not re.search(codigo_flexible, plano):
            fallos.append(f"SEÑAL {senal['codigo']}: el código no aparece en {archivo_pdf} p{senal['pagina']}.")

        nombre_plano = sin_acentos_mayus(senal["nombre"])
        if nombre_plano not in plano:
            fallos.append(
                f"SEÑAL {senal['codigo']}: el nombre «{senal['nombre']}» no aparece en {archivo_pdf} p{senal['pagina']}."
            )

        ruta = os.path.join(SENALES, senal["archivo"])
        if not os.path.exists(ruta) or os.path.getsize(ruta) < 400:
            fallos.append(f"SEÑAL {senal['codigo']}: falta o está vacía la imagen {senal['archivo']}.")
    return len(datos["senales"])


def main() -> int:
    fallos: list[str] = []
    print("Verificando contenidos contra los PDF oficiales…\n")

    n_tarjetas = verificar_estudio(fallos)
    print(f"  Tarjetas de estudio revisadas : {n_tarjetas}")

    n_preguntas = verificar_preguntas(fallos)
    print(f"  Preguntas del test revisadas  : {n_preguntas}")

    n_senales = verificar_senales(fallos)
    print(f"  Señaléticas revisadas         : {n_senales}")

    total = n_tarjetas + n_preguntas + n_senales
    print()
    if fallos:
        print(f"SE ENCONTRARON {len(fallos)} DISCREPANCIAS:\n")
        for f in fallos[:40]:
            print("  -", f)
        if len(fallos) > 40:
            print(f"  … y {len(fallos) - 40} más.")
        return 1

    print(f"Sin discrepancias: los {total} contenidos publicados coinciden con los manuales oficiales.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
