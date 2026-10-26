#!/usr/bin/env python3
"""acme/indexer:2 service — the internal search-index API. Listens on 0.0.0.0:<port> (default 8451)
and answers /health with `ok` so the container is demonstrably up."""
import http.server
import socketserver
import sys


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"ok\n" if self.path.startswith("/health") else b"acme-indexer 2\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8451
    with Server(("0.0.0.0", port), Handler) as httpd:
        httpd.serve_forever()
