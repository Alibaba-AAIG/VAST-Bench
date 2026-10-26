"""HTTPS health endpoint for the billing pre-production service."""

from __future__ import annotations

import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


HEALTH_RESPONSE = Path("/opt/billing-smoke/health.json")
CERTIFICATE = "/opt/billing-smoke/tls.crt"
PRIVATE_KEY = "/opt/billing-smoke/tls.key"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        hostname = self.headers.get("Host", "").partition(":")[0].rstrip(".").lower()
        if self.path != "/health" or hostname != "billing.example.test":
            self.send_error(404)
            return

        body = HEALTH_RESPONSE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args) -> None:
        pass


ThreadingHTTPServer.allow_reuse_address = True
server = ThreadingHTTPServer(("127.0.0.17", 443), Handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(CERTIFICATE, PRIVATE_KEY)
server.socket = context.wrap_socket(server.socket, server_side=True)
server.serve_forever()
