"""edgetools mirror service — serves install.sh and the edgec binary over HTTP.

Bound on :80; startup_command remaps get.edgetools.io to this container's own IP.
"""

import http.server
import socketserver

WEBROOT = "/srv/edgetools/public"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBROOT, **kwargs)

    def do_GET(self):
        if self.path == "/health":
            body = b'{"status":"ready"}\n'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True
socketserver.TCPServer(("0.0.0.0", 80), Handler).serve_forever()
