from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        ok=self.headers.get('X-Demo-Token')=='PUBLIC_SAMPLE_NO_AUTHORITY'
        self.send_response(200 if ok else 400);self.end_headers();self.wfile.write(b'{"service":"metricsd","status":"ok"}' if ok else b'Wrong sample context')
ThreadingHTTPServer(('127.0.0.1',8061),H).serve_forever()
