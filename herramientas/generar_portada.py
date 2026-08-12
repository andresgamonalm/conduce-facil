"""Genera la portada de presentación de Conduce-Fácil en 1920 × 1080."""

from __future__ import annotations

import io
import os

import cairosvg
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = os.path.join(RAIZ, "public", "assets", "marca")
DESTINO = os.path.join(RAIZ, "documentacion", "portada_presentacion_conduce_facil.jpg")
FUENTE_VAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Roboto-var.ttf")

FONDO = "#F5F5F5"
AZUL = "#040764"
TURQUESA = "#20B6B6"
GRIS_MEDIO = "#545454"


def fuente(tam: int, peso: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(FUENTE_VAR, tam)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def main() -> None:
    lienzo = Image.new("RGB", (1920, 1080), FONDO)
    dibujo = ImageDraw.Draw(lienzo)

    icono_png = cairosvg.svg2png(
        url=os.path.join(MARCA, "icono_conduce_facil.svg"), output_width=300
    )
    icono = Image.open(io.BytesIO(icono_png)).convert("RGBA")
    lienzo.paste(icono, (810, 300), icono)

    f_titulo = fuente(104, 600)
    ancho_a = dibujo.textlength("Conduce", font=f_titulo)
    ancho_b = dibujo.textlength("-Fácil", font=f_titulo)
    x = (1920 - (ancho_a + ancho_b)) / 2
    dibujo.text((x, 660), "Conduce", font=f_titulo, fill=AZUL, anchor="lt")
    dibujo.text((x + ancho_a, 660), "-Fácil", font=f_titulo, fill=TURQUESA, anchor="lt")

    f_bajada = fuente(30, 400)
    dibujo.text(
        (960, 800),
        "Preparación del examen teórico de conducción Clase B en Chile",
        font=f_bajada, fill=GRIS_MEDIO, anchor="mt",
    )

    f_pie = fuente(23, 500)
    dibujo.text(
        (960, 985),
        "Contenidos oficiales CONASET · Manual de Señalización de Tránsito · Desarrollado por Gamonal",
        font=f_pie, fill=GRIS_MEDIO, anchor="mt",
    )

    lienzo.save(DESTINO, quality=94, optimize=True, progressive=True)
    print(f"{os.path.basename(DESTINO)} {lienzo.size} · {os.path.getsize(DESTINO) // 1024} KB")


if __name__ == "__main__":
    main()
