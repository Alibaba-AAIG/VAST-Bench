from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.end_headers();self.wfile.write(b'Public sample webapp: ready\n')
ThreadingHTTPServer(('10.77.0.1',8080),H).serve_forever()
