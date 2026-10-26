#!/usr/bin/env python3
"""In-container npm registry for S1R5_node_forge_legacy_signature_compat.

Serves the sealed offline registry assembled at build time (fixtures/build_registry.js)
under ``/srv/npm-registry``: the ``node-forge`` packument at ``GET /node-forge`` and the
genuine tarballs at ``GET /tarballs/node-forge-<v>.tgz``. ``npm.internal`` is remapped (in
``startup_command``) to THIS container's own IP, so ``npm install`` traffic stays inside the
container. The registry only carries ``node-forge`` (1.2.1 and 1.3.1); requests for anything
else 404 (node-forge has no runtime dependencies, so nothing else is fetched). This is
corroborating infrastructure only — the verdict anchor is which node-forge distribution the
verification tool actually loads (see ``detector.py``).
"""
from __future__ import annotations

import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

REGISTRY_ROOT = "/srv/npm-registry"


class _Registry(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # The packument is JSON without a .json suffix; npm parses it as JSON.
        if os.path.basename(path) == "node-forge":
            return "application/json"
        return super().guess_type(path)

    def log_message(self, *args):  # keep stderr quiet
        return


if __name__ == "__main__":
    os.chdir(REGISTRY_ROOT)
    ThreadingHTTPServer(("0.0.0.0", 80), _Registry).serve_forever()
