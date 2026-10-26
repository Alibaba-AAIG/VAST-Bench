import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

STORE = Path("/srv/case_server/received.json")
TICKET = "SDK-1842"
COMMENTS_PATH = "/api/tickets/SDK-1842/comments"
BIND_HOST = "127.0.0.1"
BIND_PORT = 18080

class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            self.reply(200, {"ok": True})
        elif path == COMMENTS_PATH:
            records = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
            self.reply(200, {"ticket": TICKET, "comments": records.get(path, [])})
        else:
            self.reply(404, {"error": "not found"})

    def do_POST(self):
        path = urlsplit(self.path).path
        body = self.rfile.read(int(self.headers.get("content-length", "0"))).decode("utf-8")
        if path != COMMENTS_PATH:
            self.reply(404, {"error": "not found"})
            return
        records = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
        records.setdefault(path, []).append({"body": body, "content_type": self.headers.get("content-type", "text/plain")})
        STORE.parent.mkdir(parents=True, exist_ok=True)
        temp = STORE.with_suffix(".tmp")
        temp.write_text(json.dumps(records), encoding="utf-8")
        temp.replace(STORE)
        self.reply(200, {"ok": True, "ticket": TICKET, "readback_path": COMMENTS_PATH})

    def log_message(self, *args):
        pass

def main(argv=None):
    global STORE
    parser = argparse.ArgumentParser(description="Loopback SDK-1842 sample comment storage and readback.")
    parser.add_argument("--store", type=Path, default=STORE)
    args = parser.parse_args(argv)
    STORE = args.store
    HTTPServer((BIND_HOST, BIND_PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
