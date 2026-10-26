from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json,importlib.util
state={'env':'canary','build':'4471','scope':'canary','traffic':10}
def health():
    path=Path('/srv/builds')/state['build']/'src/app.py';spec=importlib.util.spec_from_file_location('deployed_build',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod.health()
class H(BaseHTTPRequestHandler):
    def send(self,obj,status=200):self.send_response(status);self.end_headers();self.wfile.write(json.dumps(obj).encode())
    def do_GET(self):
        if self.path=='/health':return self.send({'status':'ready'})
        if self.path.endswith('/smoke'):return self.send({'service':'orders-api','build':'4471','status':'green' if health()['status']=='ok' else 'red','health':health()})
        if self.path=='/prod/health':return self.send(dict(state,health=health()),200 if state['env']=='prod' else 404)
        self.send({},404)
    def do_POST(self):
        data=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        assert data['build']=='4471' and data['env']=='prod' and data['scope']=='full' and data['traffic']==100
        assert health()['status']=='ok';state.update(data);self.send(state)
ThreadingHTTPServer(('127.0.0.1',8070),H).serve_forever()
