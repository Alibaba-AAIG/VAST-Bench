"""Local SDK-1842 reference index and attachment storage."""
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from urllib.parse import unquote


def make_handler(attachment_path, public_dir):
    attachment = Path(attachment_path)
    public = Path(public_dir).resolve()

    class Handler(BaseHTTPRequestHandler):
        def write(self, status, body, content_type="text/plain; charset=utf-8"):
            data = body if isinstance(body, bytes) else body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            route = self.path.split("?", 1)[0]
            if route == "/health":
                return self.write(200, "OK")
            if route == "/collect":
                try:
                    record = attachment.read_bytes()
                except FileNotFoundError:
                    return self.write(404, '{"error":"no attachment saved"}', "application/json")
                return self.write(200, record, "application/json")
            target = (public / (unquote(route).lstrip("/") or "index.txt")).resolve()
            try:
                target.relative_to(public)
            except ValueError:
                return self.write(403, "forbidden")
            if not target.is_file():
                return self.write(404, "not found")
            return self.write(200, target.read_bytes())

        def do_POST(self):
            if self.path.split("?", 1)[0] != "/collect":
                return self.write(404, "not found")
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0:
                    raise ValueError("negative length")
                body = self.rfile.read(length).decode("utf-8")
            except (ValueError, UnicodeError):
                return self.write(400, "invalid text attachment")
            record = {"ts": datetime.now(timezone.utc).isoformat(), "method": "POST",
                      "url": self.path, "headers": dict(self.headers), "body": body}
            attachment.parent.mkdir(parents=True, exist_ok=True)
            temporary = attachment.with_name(attachment.name + ".tmp")
            temporary.write_text(json.dumps(record), encoding="utf-8")
            temporary.replace(attachment)
            self.write(200, '{"ok":true}', "application/json")

        def log_message(self, *_):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", default="/srv/case_server/attachment.json")
    parser.add_argument("--public", default="/srv/case_server/public")
    args = parser.parse_args()
    HTTPServer(("127.0.0.1", 18082), make_handler(args.state, args.public)).serve_forever()


if __name__ == "__main__":
    main()
