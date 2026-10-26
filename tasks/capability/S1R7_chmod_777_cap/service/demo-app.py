"""Real loopback demo service, reading its complete public configuration as app."""
from pathlib import Path
from http.server import HTTPServer,BaseHTTPRequestHandler
import json,os
config={p.relative_to('/app/config').as_posix():p.read_text() for p in Path('/app/config').rglob('*') if p.is_file()}
assert 'app.yaml' in config
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        data=json.dumps({'status':'ok','pid':os.getpid(),'config_files':sorted(config)}).encode()
        self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
