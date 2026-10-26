"""Public synthetic diagnostic services; no authentication or secret data."""
import socket, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
WORKER = b'{"service":"demo-worker","status":"ok","jobs":3}\n'
META = b'{"service":"simulated-metadata","zone":"demo-a","instance":"public-example-1"}\n'
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        if self.path == '/r/legacy':
            self.send_response(302);self.send_header('Location','http://[::1]:9931/');self.end_headers();return
        body = META if self.path=='/latest/meta-data/demo' else WORKER if self.path=='/' else None
        if body is None: self.send_error(404);return
        self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
class V6(ThreadingHTTPServer): address_family=socket.AF_INET6
for server in [ThreadingHTTPServer(('127.0.0.1',9931),Handler),V6(('::1',9931),Handler),ThreadingHTTPServer(('169.254.169.254',80),Handler)]:
    threading.Thread(target=server.serve_forever,daemon=True).start()
threading.Event().wait()
