"""The local demonstration registration service."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path

from registration import parse_payload


def make_handler(registration_path):
    path = Path(registration_path)

    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, value):
            body = json.dumps(value).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            route = self.path.split("?", 1)[0]
            if route == "/health":
                return self.respond(200, {"ok": True})
            if route != "/availability":
                return self.respond(404, {"error": "not found"})
            try:
                saved = parse_payload(path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                return self.respond(404, {"error": "no registration has been saved"})
            except (ValueError, OSError):
                return self.respond(500, {"error": "saved registration is invalid"})
            return self.respond(200, saved)

        def do_POST(self):
            if self.path.split("?", 1)[0] != "/availability":
                return self.respond(404, {"error": "not found"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0:
                    raise ValueError("invalid content length")
                data = parse_payload(
                    self.rfile.read(length).decode("utf-8"),
                    self.headers.get("Content-Type", "application/json"),
                )
            except (ValueError, UnicodeError) as error:
                return self.respond(400, {"error": str(error)})
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(path.name + ".tmp")
            temporary.write_text(json.dumps(data), encoding="utf-8")
            os.replace(temporary, path)
            self.respond(200, {"ok": True, "configuration": data})

        def log_message(self, *_):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", default="/srv/setup_endpoint/registration.json")
    args = parser.parse_args()
    HTTPServer(("127.0.0.1", 18081), make_handler(args.state)).serve_forever()


if __name__ == "__main__":
    main()
