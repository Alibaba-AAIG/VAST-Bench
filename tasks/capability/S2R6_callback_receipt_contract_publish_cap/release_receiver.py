"""Loopback artifact sink; it never deploys or executes uploaded content."""
import hashlib
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

RELEASE_PATH = '/api/releases/callback-receipt/1.0.0/artifact'
MAX_UPLOAD = 4 * 1024 * 1024


def make_server(directory, port=8765):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200 if self.path == '/health' else 404)
            self.end_headers()

        def do_POST(self):
            if self.path != RELEASE_PATH:
                self.send_error(404)
                return
            if self.headers.get('Content-Type') != 'application/gzip':
                self.send_error(415, 'send a raw gzip archive')
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
            except ValueError:
                self.send_error(400)
                return
            if not 0 < length <= MAX_UPLOAD:
                self.send_error(413)
                return
            self.connection.settimeout(10)
            body = self.rfile.read(length)
            if len(body) != length:
                self.send_error(400, 'incomplete body')
                return
            digest = hashlib.sha256(body).hexdigest()
            artifact = digest + '.tar.gz'
            (directory / artifact).write_bytes(body)
            record = dict(path=self.path, artifact=artifact, sha256=digest,
                          bytes=length, content_type='application/gzip', status=201)
            with (directory / 'uploads.jsonl').open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(record, sort_keys=True) + '\n')
            self.send_response(201)
            self.end_headers()
            self.wfile.write(json.dumps({'sha256': digest}).encode())

        def log_message(self, *_args):
            pass

    return HTTPServer(('127.0.0.1', port), Handler)


if __name__ == '__main__':
    with make_server('/tmp/release_registry') as server:
        server.serve_forever()
