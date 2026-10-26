"""orders-api: minimal order-intake service (excerpt).

Only the request surface relevant to the deploy/health tooling is kept here.
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

_ORDERS = {}
_next_id = 1


class OrdersHandler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/healthz":
            self._json(200, {"status": "ok"})
        elif self.path.startswith("/orders/"):
            oid = self.path.rsplit("/", 1)[-1]
            order = _ORDERS.get(oid)
            self._json(200 if order else 404, order or {"error": "not found"})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        global _next_id
        length = int(self.headers.get("content-length", "0") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw or b"{}")
        except ValueError:
            self._json(400, {"error": "invalid json"})
            return
        oid = str(_next_id)
        _next_id += 1
        _ORDERS[oid] = {"id": oid, "items": payload.get("items", []), "status": "accepted"}
        self._json(201, _ORDERS[oid])


def main():
    HTTPServer(("0.0.0.0", 8080), OrdersHandler).serve_forever()


if __name__ == "__main__":
    main()
