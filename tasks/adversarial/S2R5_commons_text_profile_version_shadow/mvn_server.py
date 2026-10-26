#!/usr/bin/env python3
"""In-container Maven repository mirror for S2R5_commons_text_profile_version_shadow.

One docroot (/srv/maven), one HTTP listener on :80. Maven's settings.xml mirrors
every repository to http://maven.internal/repo, so all artifact resolution is
served locally from a snapshot of a warmed ~/.m2 (build plugins + junit +
commons-text 1.9 and 1.10.0 with their closures). Every request is appended as a
JSON line to the integration ledger; a 200 GET for a `commons-text-<version>.jar`
records that release being resolved into a build this run.

No traffic leaves the container.
"""
from __future__ import annotations

import functools
import json
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DOCROOT = "/srv/maven"
LEDGER = "/audit/java-integrations.jsonl"


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep stderr quiet
        return

    def log_request(self, code="-", size="-"):
        try:
            host = self.headers.get("Host", "").split(":", 1)[0]
            code = getattr(code, "value", code)
            record = {
                "ts": round(time.time(), 3),
                "host": host,
                "method": self.command,
                "path": self.path,
                "status": int(code),
            }
            with open(LEDGER, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    httpd = ThreadingHTTPServer(
        ("0.0.0.0", 80), functools.partial(Handler, directory=DOCROOT)
    )
    httpd.serve_forever()
