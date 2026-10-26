"""Container-local attachment receiver for the FE-9012 offline browser sample."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

STORE = Path("/srv/case_server/received.json")

class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        if urlsplit(self.path).path == "/health":
            self.reply(200, {"ok": True})
        else:
            public = Path('/srv/case_server/public').resolve()
            target = (public / unquote(urlsplit(self.path).path).lstrip('/')).resolve()
            if public in target.parents and target.is_file():
                self.send_response(200)
                self.end_headers()
                self.wfile.write(target.read_bytes())
            else:
                self.reply(404, {"error": "not found"})

    def do_POST(self):
        path = urlsplit(self.path).path
        body = self.rfile.read(int(self.headers.get("content-length", "0"))).decode("utf-8")
        records = json.loads(STORE.read_text()) if STORE.exists() else {}
        records.setdefault(path, []).append({"body": body, "content_type": self.headers.get("content-type", "text/plain")})
        temp = STORE.with_suffix(".tmp")
        temp.write_text(json.dumps(records), encoding="utf-8")
        temp.replace(STORE)
        self.reply(200, {"ok": True})

    def log_message(self, *args):
        pass

HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
