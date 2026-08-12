@echo off
REM Conduce-Facil - abre el aplicativo con doble clic (Windows).
REM Levanta el servidor local y abre el navegador. No hay que escribir comandos.
cd /d "%~dp0"
python herramientas\servidor_local.py --abrir
pause
