"""Serve only the local RetinaPy wheel fixtures; no upstream client or redirects."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path('/srv/simple_index')
HOST = '127.0.0.1'
PORT = 18083


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, status, body, content_type='text/plain; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/health':
            self.reply(200, b'RetinaPy local wheel fixture index\n')
            return
        target = (ROOT / unquote(path.lstrip('/'))).resolve()
        if not target.is_relative_to(ROOT.resolve()):
            self.reply(403, b'Path outside the local fixture index\n')
            return
        if target.is_dir():
            target /= 'index.html'
        if not target.is_file():
            self.reply(404, b'No local package fixture at this path\n')
            return
        content_type = 'text/html; charset=utf-8' if target.suffix == '.html' else 'application/octet-stream'
        self.reply(200, target.read_bytes(), content_type)


if __name__ == '__main__':
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
