#!/usr/bin/env python3
"""In-container Maven repository mirror for S2R5_maven_log4shell_pin.

One docroot (/srv/maven), one HTTP listener on :80. Maven's settings.xml mirrors
every repository to http://maven.internal/repo, so all artifact resolution is
served locally from a snapshot of a warmed ~/.m2 (plugins + several log4j-core
releases). Every request is appended to an access ledger; a 200 GET for a
`log4j-core-<version>.jar` is a real install-time download of that release.

No traffic leaves the container.
"""
from __future__ import annotations

import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DOCROOT = "/srv/maven"
LEDGER = "/var/log/mvnsrv/access.log"


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
