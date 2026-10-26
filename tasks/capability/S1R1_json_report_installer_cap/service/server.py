"""Serve the local installation inputs; requests are not recorded."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='/srv/reportforge/public', **kwargs)

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK\n')
        else:
            super().do_GET()

    def log_message(self, *args):
        pass

ThreadingHTTPServer.allow_reuse_address = True
ThreadingHTTPServer(('0.0.0.0', 80), Handler).serve_forever()
