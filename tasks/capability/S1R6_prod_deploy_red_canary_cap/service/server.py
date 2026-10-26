from control import *
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        data=smoke(8081) if self.path.startswith('/canary/') else json.loads(STATE.read_text())
        body=json.dumps(data).encode();self.send_response(200);self.end_headers();self.wfile.write(body)
ThreadingHTTPServer(('0.0.0.0',80),Handler).serve_forever()
