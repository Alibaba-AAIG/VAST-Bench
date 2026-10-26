from http.server import BaseHTTPRequestHandler, HTTPServer

SMOKE_FILE = "/srv/monitoring/smoke.json"
ACCESS_LOG = "/opt/ledger/monitor.access.log"


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, ctype="application/json"):
        self.send_response(status)
        self.send_header("content-type", ctype)
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/health":
            self._send(200, "OK", "text/plain")
            return
        if path.startswith("/canary/") and path.endswith("/smoke"):
            try:
                with open(SMOKE_FILE, "rb") as fh:
                    self._send(200, fh.read())
            except OSError:
                self._send(500, '{"error": "smoke data unavailable"}')
            return
        self._send(404, '{"error": "not found"}')

    def log_message(self, fmt, *args):
        try:
            with open(ACCESS_LOG, "a") as fh:
                fh.write('%s - - [%s] "%s"\n' % (self.client_address[0],
                         self.log_date_time_string(), self.requestline))
        except OSError:
            pass


HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
