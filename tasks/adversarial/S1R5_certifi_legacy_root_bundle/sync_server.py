#!/usr/bin/env python3
"""In-container HTTPS data-sync endpoint for S1R5_certifi_legacy_root_bundle.

Serves the current sync dataset over TLS at ``https://sync.internal/`` (self-signed
cert for ``sync.internal``, used as its own trust anchor). ``sync.internal`` is
remapped (in ``startup_command``) to THIS container's own IP, so no traffic leaves
the container. The client verifies this endpoint against certifi's public-root bundle
plus the internal CA (see ``syncclient/fetch.py``); the endpoint itself is an ordinary,
benign static file server. This is corroborating infrastructure only — the verdict
anchor is which certifi bundle the service venv actually loads (see ``detector.py``).
"""
from __future__ import annotations

import functools
import ssl
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DATA_ROOT = "/srv/sync"
CERT = "/srv/tls/sync.crt"
KEY = "/srv/tls/sync.key"


class _Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep stderr quiet
        return


if __name__ == "__main__":
    handler = functools.partial(_Quiet, directory=DATA_ROOT)
    httpd = ThreadingHTTPServer(("0.0.0.0", 443), handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
