#!/usr/bin/env python3
import sys,json,subprocess,time,urllib.request
from pathlib import Path
from http.server import HTTPServer,BaseHTTPRequestHandler
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from payments_api.preflight import first_open_gate
BODY={'service':'payments-api','status':'healthy','adapter_version':'1.0.0'}
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        gate=first_open_gate(ROOT)
        self.send_response(200 if gate is None else 503);self.end_headers();self.wfile.write(json.dumps(BODY if gate is None else {'status':'unhealthy','reason':gate}).encode())
    def log_message(self,*args):pass
if '--serve' in sys.argv:HTTPServer(('127.0.0.1',8089),Handler).serve_forever()
else:
    gate=first_open_gate(ROOT)
    if gate:raise SystemExit(gate)
    log=open('/tmp/payments-api.log','a')
    subprocess.Popen([sys.executable,__file__,'--serve'],stdout=log,stderr=log,start_new_session=True)
    for _ in range(50):
        try:
            body=urllib.request.urlopen('http://127.0.0.1:8089/health',timeout=1).read();assert json.loads(body)==BODY
            (ROOT/'run').mkdir(exist_ok=True);(ROOT/'run/health.ok').write_bytes(body);print(body.decode());break
        except OSError:time.sleep(.1)
    else:raise SystemExit('Service did not start')
