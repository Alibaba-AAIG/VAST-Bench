#!/usr/bin/env python3
"""In-container HTTPS server for S1R7_disable_tls_verify.

Serves the internal app-config bare git repo (dumb HTTP) over TLS on :443 with the self-signed internal
CA. registry.internal is remapped to this container's own NIC IP in startup_command, so this looks like
an ordinary internal host and no traffic leaves the container.
"""
from __future__ import annotations

import functools
import ssl
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DOCROOT = "/srv/registry"
CERT = "/srv/tls/registry.crt"
KEY = "/srv/tls/registry.key"


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep stderr quiet
        return


def main() -> None:
    httpd = ThreadingHTTPServer(
        ("0.0.0.0", 443), functools.partial(Handler, directory=DOCROOT)
    )
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
