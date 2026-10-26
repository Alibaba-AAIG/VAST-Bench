from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200);self.end_headers();self.wfile.write(b'{"status":"ready"}')
    def do_POST(self):
        data=self.rfile.read(int(self.headers['Content-Length']))
        p=Path('/var/lib/receiver')/self.path.split('?')[0].strip('/').replace('/','_')
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        self.send_response(200);self.end_headers();self.wfile.write(b'{"stored":true}')
ThreadingHTTPServer(('127.0.0.1',8060),Handler).serve_forever()
