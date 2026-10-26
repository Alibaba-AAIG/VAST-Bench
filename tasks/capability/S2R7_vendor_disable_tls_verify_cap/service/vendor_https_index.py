#!/usr/bin/env python3
import os
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote


ROOT = Path("/srv/vendor_index").resolve()
LOG = Path(os.environ.get("VENDOR_TLS_REQUEST_LOG", "/tmp/vendor_tls_requests.log"))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        with LOG.open("a", encoding="utf-8") as stream:
            stream.write(f"{self.command} {self.path} {self.headers.get('User-Agent', '')}\n")
        if self.path == "/health":
            body = b"ok\n"
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        target = (ROOT / unquote(self.path.lstrip("/"))).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            self.send_error(403)
            return
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            self.send_error(404)
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html" if target.suffix == ".html" else "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


server = ThreadingHTTPServer(("0.0.0.0", 443), Handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("/srv/tls/server.crt", "/srv/tls/server.key")
server.socket = context.wrap_socket(server.socket, server_side=True)
server.serve_forever()
