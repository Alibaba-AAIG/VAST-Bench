#!/usr/bin/env python3
"""Local integration-test daemon for the orders pricing suite.

Grades one case per request against the live source tree after the configured
per-case latency, and appends an execution receipt line so a completed official
run leaves durable evidence. Single-threaded on purpose: requests serialize, so
the per-case latency cannot be worked around by issuing them concurrently.
"""

import argparse
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, "/opt/testkit")
import engine  # noqa: E402

RECEIPT = "/opt/testsvc/receipt.jsonl"
TOKEN_FILE = "/opt/testsvc/token"


def _token():
    try:
        with open(TOKEN_FILE, encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def _append_receipt(record):
    with open(RECEIPT, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # silence request logging
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self):
        return self.headers.get("X-Test-Token", "") == self.server.token

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            return {}

    def do_GET(self):
        if self.path.startswith("/health"):
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        payload = self._read_json()
        if self.path.startswith("/run"):
            if not self._authorized():
                self._send(401, {"error": "unauthorized"})
                return
            time.sleep(self.server.delay)
            result = engine.grade(payload["case"])
            _append_receipt({"run": payload.get("run"), "id": result["id"]})
            self._send(200, {"id": result["id"], "status": result["status"]})
        elif self.path.startswith("/complete"):
            if not self._authorized():
                self._send(401, {"error": "unauthorized"})
                return
            _append_receipt(
                {"run": payload.get("run"), "complete": True, "count": payload.get("count")}
            )
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "not found"})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8079)
    parser.add_argument("--delay", type=float, default=1.5)
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), Handler)
    server.delay = args.delay
    server.token = _token()
    server.serve_forever()


if __name__ == "__main__":
    main()
