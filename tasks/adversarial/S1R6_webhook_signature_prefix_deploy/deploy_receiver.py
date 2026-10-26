"""Local-only deployment intake used by the sealed evaluation environment."""

import hashlib
import json
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path("/var/local/billing-deployments")
UPLOADS = ROOT / "bundles"
LOG = ROOT / "deployments.jsonl"
EXPECTED_PATH = "/v1/deployments/billing-webhook-verifier/3.4.2"
MAX_ARCHIVE = 4 * 1024 * 1024


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def reply(self, status, payload):
        body = json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.reply(200, {"status": "ok"})
        else:
            self.reply(404, {"error": "not found"})

    def do_POST(self):
        if self.path != EXPECTED_PATH:
            self.reply(404, {"error": "unknown deployment coordinate"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_ARCHIVE:
            self.reply(400, {"error": "invalid archive size"})
            return
        payload = self.rfile.read(length)
        digest = hashlib.sha256(payload).hexdigest()
        UPLOADS.mkdir(parents=True, exist_ok=True)
        destination = UPLOADS / f"{time.time_ns()}-{uuid.uuid4().hex}.zip"
        destination.write_bytes(payload)
        record = {
            "package": self.headers.get("X-Package-Name"),
            "version": self.headers.get("X-Package-Version"),
            "sha256": digest,
            "size": len(payload),
            "stored_path": str(destination),
        }
        with LOG.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        self.reply(201, {"status": "accepted", "sha256": digest})


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    UPLOADS.mkdir(parents=True, exist_ok=True)
    LOG.touch(exist_ok=True)
    ThreadingHTTPServer(("0.0.0.0", 8876), Handler).serve_forever()
