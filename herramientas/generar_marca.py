"""Genera la identidad visual del aplicativo Conduce-Fácil.

Produce el símbolo, el logotipo horizontal y los archivos derivados (SVG, PNG
transparente, ICO multirresolución, favicon y PNG de 1000 × 1000 para uso
audiovisual). El concepto: una placa de señal vertical en azul Gamonal con una
vía que se resuelve en un visto bueno; el trazo corto en turquesa y el largo en
blanco, con la línea segmentada del eje de calzada.
"""

from __future__ import annotations

import io
import os

import cairosvg
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = os.path.join(RAIZ, "public", "assets", "marca")
FUENTE_VAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Roboto-var.ttf")

AZUL = "#040764"
AZUL_OSCURO = "#04065A"
TURQUESA = "#20B6B6"
BLANCO = "#FFFFFF"

SIMBOLO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128" role="img" aria-label="Conduce-Fácil">
  <rect x="4" y="4" width="120" height="120" rx="24" fill="{azul}"/>
  <path d="M33 69 L55 91" fill="none" stroke="{turquesa}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M55 91 L97 33" fill="none" stroke="{blanco}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M63 82 L89 46" fill="none" stroke="{azul}" stroke-width="3.4" stroke-linecap="butt" stroke-dasharray="6 8"/>
</svg>""".format(azul=AZUL, turquesa=TURQUESA, blanco=BLANCO)

LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 128" width="520" height="128" role="img" aria-label="Conduce-Fácil">
  <rect x="4" y="4" width="120" height="120" rx="24" fill="{azul}"/>
  <path d="M33 69 L55 91" fill="none" stroke="{turquesa}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M55 91 L97 33" fill="none" stroke="{blanco}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M63 82 L89 46" fill="none" stroke="{azul}" stroke-width="3.4" stroke-linecap="butt" stroke-dasharray="6 8"/>
  <text x="150" y="82" font-family="Roboto, 'Helvetica Neue', Arial, sans-serif" font-size="54" font-weight="600" fill="{azul}">Conduce<tspan fill="{turquesa}">-Fácil</tspan></text>
</svg>""".format(azul=AZUL, turquesa=TURQUESA, blanco=BLANCO)


SIMBOLO_NEGATIVO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128" role="img" aria-label="Conduce-Fácil">
  <rect x="4" y="4" width="120" height="120" rx="24" fill="{blanco}"/>
  <path d="M33 69 L55 91" fill="none" stroke="{turquesa}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M55 91 L97 33" fill="none" stroke="{azul}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M63 82 L89 46" fill="none" stroke="{blanco}" stroke-width="3.4" stroke-linecap="butt" stroke-dasharray="6 8"/>
</svg>""".format(azul=AZUL, turquesa=TURQUESA, blanco=BLANCO)

LOGO_NEGATIVO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 128" width="520" height="128" role="img" aria-label="Conduce-Fácil">
  <rect x="4" y="4" width="120" height="120" rx="24" fill="{blanco}"/>
  <path d="M33 69 L55 91" fill="none" stroke="{turquesa}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M55 91 L97 33" fill="none" stroke="{azul}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M63 82 L89 46" fill="none" stroke="{blanco}" stroke-width="3.4" stroke-linecap="butt" stroke-dasharray="6 8"/>
  <text x="150" y="82" font-family="Roboto, 'Helvetica Neue', Arial, sans-serif" font-size="54" font-weight="600" fill="{blanco}">Conduce<tspan fill="{turquesa}">-Fácil</tspan></text>
</svg>""".format(azul=AZUL, turquesa=TURQUESA, blanco=BLANCO)


def escribir(nombre: str, contenido: str) -> None:
    with open(os.path.join(MARCA, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)


def rasterizar(svg: str, ancho: int) -> Image.Image:
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=ancho)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def fuente(tam: int, peso: int = 600) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(FUENTE_VAR, tam)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def logo_horizontal(alto_simbolo: int, negativo: bool = False) -> Image.Image:
    """Compone símbolo + palabra con la tipografía oficial en peso 600."""
    simbolo = rasterizar(SIMBOLO_NEGATIVO if negativo else SIMBOLO, alto_simbolo)
    color_palabra = BLANCO if negativo else AZUL
    tam = round(alto_simbolo * 0.46)
    f = fuente(tam, 600)
    texto_a, texto_b = "Conduce", "-Fácil"
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    ancho_a = round(tmp.textlength(texto_a, font=f))
    ancho_b = round(tmp.textlength(texto_b, font=f))
    sep = round(alto_simbolo * 0.20)
    margen = round(alto_simbolo * 0.06)
    ancho = alto_simbolo + sep + ancho_a + ancho_b + margen
    img = Image.new("RGBA", (ancho, alto_simbolo), (0, 0, 0, 0))
    img.paste(simbolo, (0, 0), simbolo)
    d = ImageDraw.Draw(img)
    x = alto_simbolo + sep
    y = alto_simbolo // 2
    d.text((x, y), texto_a, font=f, fill=color_palabra, anchor="lm")
    d.text((x + ancho_a, y), texto_b, font=f, fill=TURQUESA, anchor="lm")
    return img


def main() -> None:
    os.makedirs(MARCA, exist_ok=True)

    escribir("logo_conduce_facil.svg", LOGO)
    escribir("icono_conduce_facil.svg", SIMBOLO)
    escribir("logo_conduce_facil_negativo.svg", LOGO_NEGATIVO)
    escribir("icono_conduce_facil_negativo.svg", SIMBOLO_NEGATIVO)

    logo_horizontal(360).save(os.path.join(MARCA, "logo_conduce_facil.png"), optimize=True)
    logo_horizontal(360, negativo=True).save(
        os.path.join(MARCA, "logo_conduce_facil_negativo.png"), optimize=True)

    icono = rasterizar(SIMBOLO, 1000)
    icono.save(os.path.join(MARCA, "icono_conduce_facil_1000x1000.png"), optimize=True)

    # ICO multirresolución para acceso directo, instalador e ícono del sistema.
    tamanos = [16, 24, 32, 48, 64, 128, 256]
    base = rasterizar(SIMBOLO, 256)
    base.save(
        os.path.join(MARCA, "icono_conduce_facil.ico"),
        format="ICO",
        sizes=[(t, t) for t in tamanos],
    )
    rasterizar(SIMBOLO, 180).save(os.path.join(MARCA, "favicon_conduce_facil.png"), optimize=True)
    base.save(
        os.path.join(MARCA, "favicon_conduce_facil.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )

    for nombre in sorted(os.listdir(MARCA)):
        ruta = os.path.join(MARCA, nombre)
        detalle = ""
        if nombre.lower().endswith((".png", ".ico")):
            with Image.open(ruta) as im:
                detalle = f" {im.size[0]}x{im.size[1]} {im.mode}"
        print(f"  {nombre:38s} {os.path.getsize(ruta):>8,} bytes{detalle}")


if __name__ == "__main__":
    main()
