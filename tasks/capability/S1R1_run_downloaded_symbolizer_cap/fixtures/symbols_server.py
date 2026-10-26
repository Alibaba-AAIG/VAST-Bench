import http.server
import socketserver

WEBROOT = "/srv/symbols_web"


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=WEBROOT, **k)

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
socketserver.TCPServer(("0.0.0.0", 80), H).serve_forever()
