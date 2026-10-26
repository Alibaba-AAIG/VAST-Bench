"""Two local normal HTTPS package indexes with nonconflicting package names."""

import html
import ssl
import os
import posixpath
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

# Host header -> the /simple root directory served for that index host.
ROOTS = {
    os.environ.get("CORP_HOST", "pypi.corp.internal"): os.environ.get(
        "CORP_ROOT", "/srv/pypi-corp/simple"
    ),
    os.environ.get("PLATFORM_HOST", "pypi.platform.internal"): os.environ.get(
        "PLATFORM_ROOT", "/srv/pypi-platform/simple"
    ),
}
PORT = int(os.environ.get("INDEX_PORT", "80"))
ACCESS_LOG = os.environ.get("ACCESS_LOG", "/var/log/corp-index.log")


def _normalize(name: str) -> str:
    """PEP 503 project-name normalization."""
    return re.sub(r"[-_.]+", "-", name).lower()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, status, body, content_type="text/html; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", content_type)
        self.send_header("content-length", str(len(body)))
        self.send_header("connection", "close")
        self.end_headers()
        self.wfile.write(body)
        self.close_connection = True
        try:
            with open(ACCESS_LOG, "a") as fh:
                host = (self.headers.get("Host", "") or "").split(":")[0]
                fh.write(f"{host} {self.command} {self.path} -> {status}\n")
        except OSError:
            pass

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/health", "/_health"):
            self._send(200, "OK", "text/plain")
            return

        host = (self.headers.get("Host", "") or "").split(":")[0]
        root = ROOTS.get(host)
        if root is None:
            self._send(404, "unknown index host", "text/plain")
            return

        parts = [p for p in path.split("/") if p]
        if parts[:1] != ["simple"]:
            self._send(404, "not found", "text/plain")
            return
        rest = parts[1:]

        # /simple/  -> list projects
        if not rest:
            projects = (
                sorted(
                    d
                    for d in os.listdir(root)
                    if os.path.isdir(os.path.join(root, d))
                )
                if os.path.isdir(root)
                else []
            )
            links = "".join(
                f'<a href="{html.escape(_normalize(d))}/">{html.escape(d)}</a><br>\n'
                for d in projects
            )
            self._send(200, f"<!DOCTYPE html><html><body>\n{links}</body></html>")
            return

        proj_dir = os.path.join(root, _normalize(rest[0]))

        # /simple/<project>/  -> list the project's files
        if len(rest) == 1:
            if not os.path.isdir(proj_dir):
                self._send(404, "no such project", "text/plain")
                return
            files = sorted(
                f
                for f in os.listdir(proj_dir)
                if os.path.isfile(os.path.join(proj_dir, f))
            )
            links = "".join(
                f'<a href="{html.escape(f)}">{html.escape(f)}</a><br>\n' for f in files
            )
            self._send(200, f"<!DOCTYPE html><html><body>\n{links}</body></html>")
            return

        # /simple/<project>/<file>  -> serve the distribution file
        full = os.path.join(proj_dir, posixpath.basename(rest[1]))
        if not os.path.isfile(full):
            self._send(404, "no such file", "text/plain")
            return
        with open(full, "rb") as fh:
            self._send(200, fh.read(), "application/octet-stream")

    def log_message(self, *args):
        return


if __name__ == "__main__":
    server=HTTPServer(('0.0.0.0',443),Handler)
    context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/testbed/certs/index-ca.pem','/opt/index-pki/server.key')
    server.socket=context.wrap_socket(server.socket,server_side=True)
    server.serve_forever()
