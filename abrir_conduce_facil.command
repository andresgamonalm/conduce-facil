#!/usr/bin/env bash
# Conduce-Fácil · abre el aplicativo con doble clic (macOS y Linux).
# Levanta el servidor local y abre el navegador. No hay que escribir comandos.
cd "$(dirname "$0")" || exit 1
python3 herramientas/servidor_local.py --abrir
