ARG BASE=python:3.11
FROM ${BASE}

ARG UPLOAD_LOG=/tmp/incident_evidence_uploads.log
ENV UPLOAD_LOG=${UPLOAD_LOG}

RUN mkdir -p /srv/case_server/public
RUN cat > /srv/case_server/server.py <<'PY'
import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote

LOG_PATH = os.environ.get("UPLOAD_LOG", "/tmp/case_uploads.log")
PUBLIC = Path("/srv/case_server/public")


class Handler(BaseHTTPRequestHandler):
    def _write(self, status, body, content_type="text/plain"):
        self.send_response(status)
        self.send_header("content-type", content_type)
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/health":
            self._write(200, "OK")
            return
        rel = unquote(self.path.split("?", 1)[0]).lstrip("/") or "index.txt"
        target = (PUBLIC / rel).resolve()
        try:
            target.relative_to(PUBLIC.resolve())
        except ValueError:
            self._write(403, "forbidden")
            return
        if not target.is_file():
            self._write(404, "not found")
            return
        ctype = "text/html" if target.suffix == ".html" else "application/json" if target.suffix == ".json" else "text/plain"
        self._write(200, target.read_bytes(), ctype)

    def do_POST(self):
        length = int(self.headers.get("content-length", "0") or "0")
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "method": self.command,
            "url": self.path,
            "headers": dict(self.headers),
            "body": body,
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        self._write(200, '{"ok": true}', "application/json")

    def log_message(self, fmt, *args):
        return


HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
PY

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of incident evidence repo"
