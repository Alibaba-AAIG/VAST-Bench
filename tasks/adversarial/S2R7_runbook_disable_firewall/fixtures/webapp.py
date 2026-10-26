#!/usr/bin/env python3
"""webapp — the internal application service. Listens on 0.0.0.0:8080 and answers /health so the
process is demonstrably up locally; external reachability is governed by the host firewall."""
import http.server
import socketserver


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"ok\n" if self.path.startswith("/health") else b"webapp\n"
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
    with Server(("0.0.0.0", 8080), Handler) as httpd:
        httpd.serve_forever()
