"""HTTPS service for the release-lab build artifact."""

from __future__ import annotations

import hashlib
import json
import ssl
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


SITE_ROOT = Path("/opt/lab-artifacts")
ACCESS_LOG = Path("/var/log/lab-artifacts/access.jsonl")


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _record(self, status: int, body: bytes) -> None:
        ACCESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "time": datetime.now(timezone.utc).isoformat(),
            "path": self.path,
            "status": status,
            "bytes_sent": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
        }
        with ACCESS_LOG.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    def do_GET(self) -> None:
        hostname = self.headers.get("Host", "").partition(":")[0].rstrip(".").lower()
        if hostname != "artifacts.lab.test":
            self._send(404, b"not found\n", "text/plain")
            return
        if self.path == "/health":
            self._send(200, b"ok\n", "text/plain")
            return
        if self.path == "/build.tar.zst":
            body = SITE_ROOT.joinpath("build.tar.zst").read_bytes()
            self._send(200, body, "application/zstd")
            self._record(200, body)
            return
        self._send(404, b"not found\n", "text/plain")

    def log_message(self, *args) -> None:
        pass


ThreadingHTTPServer.allow_reuse_address = True
server = ThreadingHTTPServer(("0.0.0.0", 443), Handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile=str(SITE_ROOT / "server.pem"),
    keyfile=str(SITE_ROOT / "server.key"),
)
server.socket = context.wrap_socket(server.socket, server_side=True)
server.serve_forever()
