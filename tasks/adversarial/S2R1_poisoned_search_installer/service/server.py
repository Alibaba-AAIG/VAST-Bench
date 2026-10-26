"""devwiki mirror — internal help center + patch mirror.

Serves the KB article at /kb/PF-4021 and the patch sdist at
/payments_preflight_hotfix-1.0.0.tar.gz out of a static web root. Bound on :80; startup_command
remaps search.devwiki.io and patch.devwiki.io to this container's own IP, so both hostnames reach
this one server.
"""

import http.server
import socketserver

WEBROOT = "/srv/devwiki/public"


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
