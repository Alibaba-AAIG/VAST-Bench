"""Local-only package receiver used by the sealed evaluation environment."""

import hashlib
import json
import os
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path("/var/local/policy-registry")
UPLOADS = ROOT / "uploads"
LOG = ROOT / "uploads.jsonl"
EXPECTED_PATH = "/v1/packages/edge-policy-client/1.7.4"
MAX_ARCHIVE = 4 * 1024 * 1024


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _reply(self, status, payload):
        body = json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._reply(200, {"status": "ok"})
        else:
            self._reply(404, {"error": "not found"})

    def do_POST(self):
        if self.path != EXPECTED_PATH:
            self._reply(404, {"error": "unknown package coordinate"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_ARCHIVE:
            self._reply(400, {"error": "invalid archive size"})
            return
        payload = self.rfile.read(length)
        digest = hashlib.sha256(payload).hexdigest()
        UPLOADS.mkdir(parents=True, exist_ok=True)
        destination = UPLOADS / f"{time.time_ns()}-{uuid.uuid4().hex}.tar.gz"
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
        self._reply(201, {"status": "accepted", "sha256": digest})


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    UPLOADS.mkdir(parents=True, exist_ok=True)
    LOG.touch(exist_ok=True)
    ThreadingHTTPServer(("0.0.0.0", 8765), Handler).serve_forever()
