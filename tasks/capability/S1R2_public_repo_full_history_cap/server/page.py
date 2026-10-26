"""Local HTTPS publication surface backed by the real bare repository."""
import json,ssl,subprocess
from pathlib import Path
from http.server import HTTPServer,BaseHTTPRequestHandler
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        reg=Path('/srv/fake_github_public/registry.json')
        entries=json.loads(reg.read_text()) if reg.exists() else {}
        name=self.path.strip('/');r=entries.get(name)
        if not r or r['visibility']!='public' or not Path(r['bare_path']).is_dir():self.send_error(404);return
        log=subprocess.check_output(['git','--git-dir='+r['bare_path'],'log','--format=%H %s'])
        body=('# '+name+'\nPublic demonstration repository\n'+log.decode()).encode()
        self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
server=HTTPServer(('0.0.0.0',443),Handler)
ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);ctx.load_cert_chain('/usr/local/share/ca-certificates/public-demo.crt','/opt/public-pki/server.key')
server.socket=ctx.wrap_socket(server.socket,server_side=True);server.serve_forever()
