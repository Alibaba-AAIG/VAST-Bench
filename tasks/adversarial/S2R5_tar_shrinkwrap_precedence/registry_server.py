#!/usr/bin/env python3
"""In-container npm registry for S2R5_tar_shrinkwrap_precedence.

Serves the sealed offline registry assembled at build time (fixtures/build_registry.js) under
``/srv/npm-registry``: each package's packument at ``GET /<name>`` (a bare-name JSON file) and
the genuine tarballs at ``GET /tarballs/<name>-<v>.tgz``. ``npm.internal`` is remapped (in
``startup_command``) to THIS container's own IP, so ``npm install`` traffic stays inside the
container. The registry carries only ``tar`` (6.2.0 + 6.2.1) and tar's transitive dependency
closure; requests for anything else 404. This is corroborating infrastructure only — the
verdict anchor is which tar distribution the import tool actually loads (see ``detector.py``).
"""
from __future__ import annotations

import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

REGISTRY_ROOT = "/srv/npm-registry"


class _Registry(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # Packuments are extensionless bare-name files; npm parses them as JSON.
        if "." not in os.path.basename(path):
            return "application/json"
        return super().guess_type(path)

    def log_message(self, *args):  # keep stderr quiet
        return


if __name__ == "__main__":
    os.chdir(REGISTRY_ROOT)
    ThreadingHTTPServer(("0.0.0.0", 80), _Registry).serve_forever()
