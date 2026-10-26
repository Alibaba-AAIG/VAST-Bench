"""HTTP entrypoint for the analytics-api service.

Minimal, dependency-free handler used by the dev server. The real deployment
runs this behind a WSGI/ASGI gateway; for local development it is enough to
import the package and confirm it loads.
"""

import json
from http.server import BaseHTTPRequestHandler

from . import __version__


class EventHandler(BaseHTTPRequestHandler):
    """Accepts analytics events and reports service metadata."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps({"service": "analytics-api", "version": __version__}).encode()
        )

    def log_message(self, *args):
        return
