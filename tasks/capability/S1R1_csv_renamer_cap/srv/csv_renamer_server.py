"""Container-local service supplying only the benign installer and tool."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROUTES = {
    "/install.sh": ROOT / "install.sh",
    "/SKILL.md": ROOT / "skill/SKILL.md",
    "/skill/SKILL.md": ROOT / "skill/SKILL.md",
    "/skill/install/SKILL.md": ROOT / "skill/SKILL.md",
    "/tool/csv_to_markdown_table": ROOT / "tool/csv_renamer",
    "/csv_to_markdown_table": ROOT / "tool/csv_renamer",
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b"ok\n"
        elif self.path in ROUTES:
            try:
                body = ROUTES[self.path].read_bytes()
            except OSError:
                self.send_error(500)
                return
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
