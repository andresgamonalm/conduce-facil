"""Servidor local de Conduce-Fácil.

Sirve la carpeta ``public`` con la misma reescritura de rutas que Cloudflare
Pages, de modo que el aplicativo se comporta igual en el equipo y publicado.

Uso:
    python3 herramientas/servidor_local.py            # sólo levanta el servidor
    python3 herramientas/servidor_local.py --abrir    # además abre el navegador

Si el puerto está ocupado, busca el siguiente libre.
"""

from __future__ import annotations

import http.server
import os
import socket
import socketserver
import sys
import threading
import webbrowser

RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
PUERTO_INICIAL = 4173

RESPUESTA_API = (
    b'{"ok":false,"error":"Modo local: la base de datos no esta enlazada."}'
)


class Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=RAIZ, **kwargs)

    def do_GET(self):  # noqa: N802 (nombre impuesto por la biblioteca estándar)
        ruta = self.path.split("?", 1)[0]
        if ruta.startswith("/api"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(RESPUESTA_API)))
            self.end_headers()
            self.wfile.write(RESPUESTA_API)
            return
        destino = os.path.join(RAIZ, ruta.lstrip("/"))
        if not os.path.exists(destino):
            self.path = "/index.html"  # reescritura de rutas del aplicativo
        return super().do_GET()

    def log_message(self, *args):  # silencio en consola
        pass


def puerto_libre(inicial: int) -> int:
    for puerto in range(inicial, inicial + 40):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", puerto)) != 0:
                return puerto
    return inicial


def main() -> None:
    argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
    abrir = "--abrir" in sys.argv
    inicial = int(argumentos[0]) if argumentos else PUERTO_INICIAL
    puerto = puerto_libre(inicial)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", puerto), Manejador) as servidor:
        url = f"http://127.0.0.1:{puerto}/login"
        print("")
        print(f"  Conduce-Fácil está funcionando en {url}")
        print("  Cierra esta ventana para detenerlo.")
        print("")
        if abrir:
            threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\n  Conduce-Fácil detenido.")


if __name__ == "__main__":
    main()
