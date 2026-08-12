"""Utilidades de lectura literal del Manual CONASET Clase B.

Este módulo es la única fuente de texto para los contenidos de estudio del
aplicativo: extrae el texto tal como está en el PDF oficial y lo normaliza sin
alterar palabras, cifras ni signos. Todo contenido publicado en Conduce-Fácil
debe provenir de aquí.
"""

from __future__ import annotations

import functools
import os
import re
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_CONASET = os.path.join(RAIZ, "Manual-Conaset", "Manual-Conducción-Clase-B.pdf")

# Los guiones de corte de línea del PDF se eliminan; los saltos de línea pasan a
# ser espacios. No se sustituye ninguna palabra.
_GUION_CORTE = re.compile(r"([a-záéíóúñü])[-‐‑]\n([a-záéíóúñü])", re.IGNORECASE)
_ESPACIOS = re.compile(r"[ \t   ]+")


def normalizar(texto: str) -> str:
    """Une los cortes de línea del PDF y unifica espacios y comillas."""
    t = unicodedata.normalize("NFC", texto)
    t = t.replace("­", "")
    t = _GUION_CORTE.sub(r"\1\2", t)
    t = t.replace("\n", " ")
    t = t.replace("“", '"').replace("”", '"')
    t = t.replace("‘", "'").replace("’", "'")
    t = t.replace("–", "-").replace("—", "-")
    t = _ESPACIOS.sub(" ", t)
    return t.strip()


@functools.lru_cache(maxsize=1)
def paginas() -> list[str]:
    """Texto normalizado de cada página del manual (índice 0 = página 1)."""
    import pymupdf  # import diferido: sólo se necesita al generar contenidos

    doc = pymupdf.open(PDF_CONASET)
    return [normalizar(p.get_text("text")) for p in doc]


def pagina(numero: int) -> str:
    return paginas()[numero - 1]


def rango(desde: int, hasta: int) -> str:
    return " ".join(paginas()[desde - 1 : hasta])


class TextoNoEncontrado(Exception):
    pass


def literal(numero_pagina: int, desde: str, hasta: str | None = None, paginas_extra: int = 1) -> str:
    """Devuelve el fragmento literal del manual entre dos anclas.

    ``desde`` y ``hasta`` son textos que deben existir tal cual en el manual.
    El resultado incluye ambas anclas. Si alguna no aparece, se levanta
    ``TextoNoEncontrado`` para impedir que se publique contenido inventado.
    """
    base = rango(numero_pagina, min(numero_pagina + paginas_extra, len(paginas())))
    d = normalizar(desde)
    i = base.find(d)
    if i < 0:
        raise TextoNoEncontrado(f"p{numero_pagina}: no se encontró el inicio {desde!r}")
    if hasta is None:
        return d
    h = normalizar(hasta)
    j = base.find(h, i + len(d))
    if j < 0:
        raise TextoNoEncontrado(f"p{numero_pagina}: no se encontró el fin {hasta!r}")
    return base[i : j + len(h)].strip()


def contiene(texto: str, numero_pagina: int, margen: int = 2) -> bool:
    """Comprueba que ``texto`` aparezca literalmente en el manual."""
    desde = max(1, numero_pagina - margen)
    hasta = min(len(paginas()), numero_pagina + margen)
    return normalizar(texto) in rango(desde, hasta)
