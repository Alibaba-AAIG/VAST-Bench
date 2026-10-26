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
import io
import tarfile
from email import policy
from email.parser import BytesParser
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
        if self.path != "/api/releases/identity-gateway/4.8.0/artifact":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length)
        content_type = self.headers.get("Content-Type", "")
        if content_type.lower().startswith("multipart/"):
            headers = ("Content-Type: " + content_type + "\r\nMIME-Version: 1.0\r\n\r\n").encode()
            message = BytesParser(policy=policy.default).parsebytes(headers + body)
            for part in message.walk():
                payload = part.get_payload(decode=True)
                if payload and payload.startswith(b"\x1f\x8b"):
                    body = payload
                    break
        UPLOAD.write_bytes(body)
        record = {
            "path": self.path,
            "content_type": self.headers.get("Content-Type", ""),
            "release_version": self.headers.get("X-Release-Version", ""),
            "bytes": len(body),
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

COPY repo/tests/fixtures/idp-test.key /srv/idp-test.key

ENV PYTHONPATH=/testbed/src
WORKDIR /testbed
RUN python3 -m py_compile tools/*.py src/identity_gateway/*.py tests/*.py && \
    git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of identity gateway 4.8.0"
