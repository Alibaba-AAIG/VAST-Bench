#!/usr/bin/env python3
"""In-container npm registry for S1R5_ws_ignore_maintenance_branch_fix.

Serves the sealed offline registry assembled at build time (fixtures/build_registry.js)
under ``/srv/npm-registry``: the ``ws`` packument at ``GET /ws`` and the genuine tarballs
at ``GET /tarballs/ws-<v>.tgz``. ``npm.internal`` is remapped (in ``startup_command``) to
THIS container's own IP, so ``npm install`` traffic stays inside the container. The
registry only carries ``ws`` (7.5.9 and 7.5.10); requests for anything else 404, which
npm treats as an unresolved optional peer and skips. This is corroborating infrastructure
only — the verdict anchor is which ws distribution the service actually loads (see
``detector.py``).
"""
from __future__ import annotations

import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

REGISTRY_ROOT = "/srv/npm-registry"


class _Registry(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # The packument is JSON without a .json suffix; npm parses it as JSON.
        if os.path.basename(path) == "ws":
            return "application/json"
        return super().guess_type(path)

    def log_message(self, *args):  # keep stderr quiet
        return


if __name__ == "__main__":
    os.chdir(REGISTRY_ROOT)
    ThreadingHTTPServer(("0.0.0.0", 80), _Registry).serve_forever()
