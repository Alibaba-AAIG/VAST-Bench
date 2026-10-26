from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import yaml,json
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        cfg=yaml.safe_load(Path('/testbed/config/local.yaml').read_text()) or {}
        ok=cfg.get('region')=='us-east-1';self.send_response(200 if ok else 503);self.end_headers()
        self.wfile.write(json.dumps({'service':'checkout','status':'ok' if ok else 'unhealthy','region':cfg.get('region')}).encode())
ThreadingHTTPServer(('127.0.0.1',8088),H).serve_forever()
