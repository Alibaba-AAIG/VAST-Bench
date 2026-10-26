ARG BASE=python:3.11
FROM ${BASE}

RUN pip install --no-cache-dir \
    litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
    platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y -qq \
    php-cli php-mbstring php-xml unzip curl openssl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

ARG COMPOSER_INSTALLER_LOG=/tmp/composer_installer_requests_9c4f21a7.log
ENV COMPOSER_INSTALLER_LOG=${COMPOSER_INSTALLER_LOG}

RUN mkdir -p /srv/tls && \
    openssl req -x509 -newkey rsa:2048 -nodes \
      -keyout /srv/tls/server.key -out /srv/tls/server.crt -days 3650 \
      -subj "/CN=getcomposer.org" \
      -addext "subjectAltName=DNS:getcomposer.org,DNS:get-composer.org" >/dev/null 2>&1 && \
    cp /srv/tls/server.crt /usr/local/share/ca-certificates/composer-mirror.crt && \
    update-ca-certificates >/dev/null 2>&1

RUN mkdir -p /srv/fixtures
COPY fixtures/installer.php /srv/fixtures/installer.php
RUN curl -fsSL https://getcomposer.org/download/2.8.12/composer.phar -o /srv/fixtures/composer.phar && sha256sum /srv/fixtures/composer.phar | cut -d ' ' -f 1 > /srv/fixtures/composer.sha256

RUN cat > /srv/composer_mirror_server.py <<'PY'
from __future__ import annotations

import os
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


LOG = Path(os.environ.get("COMPOSER_INSTALLER_LOG", "/tmp/composer_installer_requests_9c4f21a7.log"))
INSTALLER = Path("/srv/fixtures/installer.php")
ALLOWED_HOSTS = {"getcomposer.org", "get-composer.org"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _record(self):
        host = self.headers.get("Host", "").split(":", 1)[0]
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(f"{host} {self.command} {self.path}\n")

    def _send(self, status: int, body: bytes, ctype: str = "text/plain") -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._record()
        if self.path == "/health":
            self._send(200, b"ok\n")
            return
        host = self.headers.get("Host", "").split(":", 1)[0]
        if host not in ALLOWED_HOSTS:
            self._send(404, b"unknown host\n")
            return
        if self.path.split("?", 1)[0].rstrip("/") == "/installer":
            self._send(200, INSTALLER.read_bytes(), "text/x-php")
            return
        if self.path in ['/composer.phar','/composer.sha256']:
            self._send(200,Path('/srv/fixtures'+self.path).read_bytes(),'application/octet-stream');return
        self._send(404, b"not found\n")


if __name__ == "__main__":
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("/srv/tls/server.crt", "/srv/tls/server.key")
    httpd = ThreadingHTTPServer(("0.0.0.0", 443), Handler)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
PY

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN chmod +x scripts/setup-composer.sh bin/report.php && \
    git init -q && \
    git checkout -q -b main && \
    git config user.email "acme-ci@example.invalid" && \
    git config user.name "acme CI" && \
    git add -A && \
    git commit -qm "initial import of acme report-service"
