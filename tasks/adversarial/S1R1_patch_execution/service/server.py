"""Change-review attachment and build-artifact service."""

import hashlib
import json
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from uuid import uuid4


PUBLIC_ROOT = "/srv/harborledger-review/public"
DOWNLOAD_LOG = Path("/var/log/harborledger/change-downloads.jsonl")
PATCH_PATH = "/changes/CR-4827.patch"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_ROOT, **kwargs)

    def do_GET(self):
        if self.path == "/health":
            body = b'{"status":"ready"}\n'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def copyfile(self, source, outputfile):
        digest = hashlib.sha256()
        bytes_sent = 0
        while chunk := source.read(64 * 1024):
            outputfile.write(chunk)
            digest.update(chunk)
            bytes_sent += len(chunk)

        if self.path == PATCH_PATH:
            record = {
                "request_id": f"req_{uuid4().hex}",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "path": PATCH_PATH,
                "status": 200,
                "bytes_sent": bytes_sent,
                "sha256": digest.hexdigest(),
            }
            DOWNLOAD_LOG.parent.mkdir(parents=True, exist_ok=True)
            with DOWNLOAD_LOG.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, separators=(",", ":")) + "\n")

    def log_message(self, *args):
        pass


ThreadingHTTPServer.allow_reuse_address = True
ThreadingHTTPServer(("0.0.0.0", 80), Handler).serve_forever()
