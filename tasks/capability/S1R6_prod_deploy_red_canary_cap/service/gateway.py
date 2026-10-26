from control import *
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def forward(self):
        state=json.loads(STATE.read_text());data=self.rfile.read(int(self.headers.get('Content-Length',0))) or None
        req=urllib.request.Request('http://127.0.0.1:'+str(state['port'])+self.path,data=data,method=self.command,headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as response:
            body=response.read();self.send_response(response.status);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(body)
    do_GET=forward
    do_POST=forward
ThreadingHTTPServer(('0.0.0.0',8080),Handler).serve_forever()
