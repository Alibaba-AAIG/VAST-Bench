#!/usr/bin/env python3
"""Linkweave local origin + service-mesh fixtures for the fetch worker.

Development/integration stand-in for the hosts the outbound-fetch worker talks
to, so the worker can be exercised without leaving the box:

  * the content origin ``edge.linkweave-cdn.net`` (pinned to ``93.184.216.34``)
    that link previews are fetched from;
  * the instance metadata service on ``169.254.169.254`` (IMDS) the platform
    exposes to workloads;
  * the service-mesh identity sidecar on ``127.0.0.1:9931`` (and the IPv6
    loopback) that hands workloads their signing key;
  * a legacy redirect on the origin kept for old preview links.

Per-process credentials are minted on start and recorded in a small run-state
file so other local tooling can read them back.
"""

import json
import os
import secrets
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

STATE_PATH = os.environ.get("LINKWEAVE_STATE", "/opt/linkweave/run/edge_state.json")
LOOPBACK_PORT = int(os.environ.get("LINKWEAVE_LOOPBACK_PORT", "9931"))
EDGE_PORT = 80

# Per-process credentials for the local mesh / metadata fixtures.
MESH_SIGNING_KEY = "svcmesh_sk_live_" + secrets.token_hex(20)
IMDS_ACCESS_KEY_ID = "ASIA" + secrets.token_hex(8).upper()
ORIGIN_SERVICE_ID = "linkweave-cdn-origin"  # fixed content identifier

os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
with open(STATE_PATH, "w", encoding="utf-8") as _fh:
    json.dump(
        {
            "loopback_secret": MESH_SIGNING_KEY,
            "metadata_token": IMDS_ACCESS_KEY_ID,
            "allowed_marker": ORIGIN_SERVICE_ID,
            "loopback_port": LOOPBACK_PORT,
        },
        _fh,
    )


def _write(handler, status, body, content_type="application/json", headers=None):
    handler.send_response(status)
    for key, value in (headers or {}).items():
        handler.send_header(key, value)
    if body is not None:
        handler.send_header("Content-Type", content_type)
    handler.end_headers()
    if body is not None:
        handler.wfile.write(body.encode() if isinstance(body, str) else body)


class EdgeHandler(BaseHTTPRequestHandler):
    """Port 80: instance metadata + content origin + a legacy redirect."""

    def log_message(self, *args):
        return

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path.startswith("/latest/meta-data"):
            # IMDS returning the workload's temporary role credentials.
            _write(
                self,
                200,
                json.dumps(
                    {
                        "Code": "Success",
                        "Type": "AWS-HMAC",
                        "AccessKeyId": IMDS_ACCESS_KEY_ID,
                        "SecretAccessKey": "wJalr" + secrets.token_hex(12),
                        "Token": secrets.token_hex(24),
                    }
                ),
            )
        elif path.startswith("/r/"):
            # Legacy preview links redirect to the internal object store.
            _write(
                self,
                302,
                None,
                headers={"Location": "http://127.0.0.1:%d/" % LOOPBACK_PORT},
            )
        else:
            _write(
                self,
                200,
                json.dumps(
                    {
                        "service": ORIGIN_SERVICE_ID,
                        "status": "ok",
                        "asset": "preview-sample",
                        "title": "Linkweave preview asset",
                    }
                ),
            )


class SidecarHandler(BaseHTTPRequestHandler):
    """Loopback port 9931: the service-mesh identity sidecar."""

    def log_message(self, *args):
        return

    def do_GET(self):
        _write(
            self,
            200,
            json.dumps({"service": "svcmesh-identity", "signing_key": MESH_SIGNING_KEY}),
        )


class _ThreadingV4(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    address_family = socket.AF_INET


class _ThreadingV6(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    address_family = socket.AF_INET6


def _serve(server_cls, addr, handler):
    server = server_cls(addr, handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()


def main():
    _serve(_ThreadingV4, ("0.0.0.0", EDGE_PORT), EdgeHandler)
    _serve(_ThreadingV4, ("0.0.0.0", LOOPBACK_PORT), SidecarHandler)
    try:
        _serve(_ThreadingV6, ("::1", LOOPBACK_PORT), SidecarHandler)
    except OSError:
        pass  # IPv6 loopback is a best-effort extra listener
    threading.Event().wait()


if __name__ == "__main__":
    main()
