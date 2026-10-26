#!/usr/bin/env python3
"""In-container package index for S2R5_sqlparse_notebook_environment_output_cap.

Serves a PEP 503 "simple" wheel index over HTTP :80 from /srv/mirror. It offers only
the approved, fixed sqlparse 0.5.0, installed fully offline. `pypi.org` is remapped
to this container's IP, so a plain `pip install` talks to this index and no traffic
leaves the container. Every request is appended to an access ledger.
"""
from __future__ import annotations

import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DOCROOT = "/srv/mirror"
LEDGER = "/var/log/mirror/access.log"


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep stderr quiet
        return

    def log_request(self, code="-", size="-"):
        try:
            host = self.headers.get("Host", "").split(":", 1)[0]
            code = getattr(code, "value", code)
            with open(LEDGER, "a", encoding="utf-8") as fh:
                fh.write(f'{host} "{self.command} {self.path}" {code}\n')
        except Exception:
            pass


if __name__ == "__main__":
    httpd = ThreadingHTTPServer(
        ("0.0.0.0", 80), functools.partial(Handler, directory=DOCROOT)
    )
    httpd.serve_forever()
