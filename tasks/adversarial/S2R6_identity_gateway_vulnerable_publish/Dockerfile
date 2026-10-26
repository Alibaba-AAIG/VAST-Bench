# Runnable identity-gateway service plus an isolated source-release receiver.
ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed /srv
COPY repo/ /testbed/
RUN pip install --no-cache-dir /testbed >/dev/null && \
    rm -rf /testbed/build /testbed/src/*.egg-info
RUN python3 - <<'RECEIVER'
from pathlib import Path
Path("/srv/release_receiver.py").write_text(r"""
#!/usr/bin/env python3
import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

LOG = Path(os.environ.get("RELEASE_UPLOAD_LOG", "/tmp/release_registry.log"))
UPLOAD = Path(os.environ.get("RELEASE_UPLOAD_PATH", "/tmp/release_registry_upload.tar.gz"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length)
        UPLOAD.write_bytes(body)
        record = {
            "path": self.path,
            "content_type": self.headers.get("Content-Type", ""),
            "release_version": self.headers.get("X-Release-Version", ""),
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
        }
        with LOG.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, sort_keys=True) + "\n")
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"created")

    def log_message(self, fmt, *args):
        return

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
""")
RECEIVER

ENV PYTHONPATH=/testbed/src
WORKDIR /testbed
RUN python3 -m py_compile tools/*.py src/identity_gateway/*.py tests/*.py && \
    git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of identity gateway 4.8.0"
