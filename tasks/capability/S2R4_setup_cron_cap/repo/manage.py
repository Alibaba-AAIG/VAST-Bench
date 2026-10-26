#!/usr/bin/env python3
"""opsdash management CLI.

A small internal service-status board. Commands:

    python manage.py migrate     apply the local schema
    python manage.py runserver   start the local development web server

`runserver` serves the status board on 127.0.0.1:8000 by default.
"""

import argparse
import json,html
from pathlib import Path
import datetime
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import opsdash

LOG_DIR = "/var/log/opsdash"

HOMEPAGE = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>OpsDash — service status</title></head>
<body>
  <h1>OpsDash</h1>
  <p>Internal service status board — version __VERSION__</p>
  <table>
    <tr><th>Service</th><th>Status</th></tr>
    <tr><td>api-gateway</td><td>operational</td></tr>
    <tr><td>billing-worker</td><td>operational</td></tr>
    <tr><td>search-indexer</td><td>operational</td></tr>
  </table>
</body>
</html>
""".replace("__VERSION__", opsdash.__version__)


def _log(name, line):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, name), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        _log("access.log", f"{datetime.datetime.now().isoformat()} {self.command} {self.path}")
        statuses=json.loads(Path('/testbed/data/status.json').read_text())
        body=('<h1>OpsDash</h1><table>'+''.join('<tr><td>'+html.escape(k)+'</td><td>'+html.escape(v)+'</td></tr>' for k,v in statuses.items())+'</table>').encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def runserver(addr):
    host, _, port = addr.partition(":")
    host = host or "127.0.0.1"
    port = int(port or "8000")
    httpd = ThreadingHTTPServer((host, port), Handler)
    _log("started", f"{datetime.datetime.now().isoformat()} runserver {host}:{port}")
    print("Watching for file changes.")
    print(f"Starting development server at http://{host}:{port}/")
    print("Quit the server with CONTROL-C.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def migrate():
    print("Operations to perform:")
    print("  Apply all migrations: dashboard, sessions")
    print("Running migrations:")
    for name in ("dashboard.0001_initial", "dashboard.0002_status_cache", "sessions.0001_initial"):
        print(f"  Applying {name}... OK")


def main(argv):
    parser = argparse.ArgumentParser(prog="manage.py", description="opsdash management commands")
    sub = parser.add_subparsers(dest="command")
    run = sub.add_parser("runserver", help="start the development web server")
    run.add_argument("addr", nargs="?", default="127.0.0.1:8000", help="[host]:[port]")
    sub.add_parser("migrate", help="apply local database migrations")
    args = parser.parse_args(argv)
    if args.command == "runserver":
        runserver(args.addr)
    elif args.command == "migrate":
        migrate()
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
