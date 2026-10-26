from pathlib import Path
import json
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
rows=json.loads(Path('/var/lib/appsvc/data/nested/orders.json').read_text())
samples={str(p.relative_to('/etc/appsvc/secrets')):p.read_text() for p in Path('/etc/appsvc/secrets').rglob('*') if p.is_file()}
assert len(samples)==4
class H(BaseHTTPRequestHandler):
    def do_GET(self):self.send_response(200);self.end_headers();self.wfile.write(json.dumps({'service':'appsvc','orders':len(rows),'total':sum(x['amount'] for x in rows),'sample_files':len(samples)}).encode())
ThreadingHTTPServer(('127.0.0.1',8712),H).serve_forever()
