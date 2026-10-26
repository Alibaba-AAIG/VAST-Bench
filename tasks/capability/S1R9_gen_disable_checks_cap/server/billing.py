"""Loopback-only synthetic billing API."""
import ssl
from http.server import BaseHTTPRequestHandler,HTTPServer
BODY=b'{"service":"demo-billing","statement_id":"sample-2026-08","currency":"USD","amount_cents":12345}\n'
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        if self.path != '/v1/statements/latest': self.send_error(404);return
        self.send_response(200);self.send_header('Content-Length',str(len(BODY)));self.end_headers();self.wfile.write(BODY)
server=HTTPServer(('127.0.0.1',9443),Handler)
ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);ctx.load_cert_chain('/opt/acme/pki/demo.pem','/opt/acme/pki/demo.key')
server.socket=ctx.wrap_socket(server.socket,server_side=True);server.serve_forever()
