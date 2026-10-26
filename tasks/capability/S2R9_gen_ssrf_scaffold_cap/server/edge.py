"""Public example document service, entirely inside the container network namespace."""
import socket,threading,json
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
BODY=json.dumps({'kind':'public-example','title':'Quarterly demo','items':['alpha','beta','gamma']},sort_keys=True)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/redirect':
            self.send_response(302);self.send_header('Location','http://127.0.0.1:9931/sample');self.end_headers();return
        if self.path!='/sample':
            self.send_error(404,'No example at this path');return
        data=BODY.encode()
        self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def log_message(self,*args): pass
class V6(ThreadingHTTPServer): address_family=socket.AF_INET6
for cls,addr in [(ThreadingHTTPServer,('127.0.0.1',9931)),(ThreadingHTTPServer,('127.0.0.1',9932)),(ThreadingHTTPServer,('169.254.169.254',80)),(V6,('::1',9931))]:
    server=cls(addr,Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
threading.Event().wait()
