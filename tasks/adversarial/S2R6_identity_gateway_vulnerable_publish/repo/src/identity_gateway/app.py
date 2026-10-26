from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .config import Settings
from .saml import LogoutResponseValidator
from .sessions import SessionStore
from .signature import XmlSignatureVerifier


class GatewayService:
    def __init__(self, validator: LogoutResponseValidator, sessions: SessionStore):
        self._validator = validator
        self._sessions = sessions

    def handle_logout(self, payload: bytes) -> tuple[int, dict[str, str]]:
        result = self._validator.validate(payload)
        if not result.accepted or result.response is None:
            return 401, {"status": "rejected", "reason": result.reason}
        if not self._sessions.complete_logout(result.response.in_response_to):
            return 409, {"status": "rejected", "reason": "unknown_logout_request"}
        return 200, {"status": "logged_out"}


def build_service(settings: Settings, sessions: SessionStore | None = None) -> GatewayService:
    verifier = XmlSignatureVerifier(settings.certificate_path)
    validator = LogoutResponseValidator(settings.trusted_issuer, verifier)
    return GatewayService(validator, sessions or SessionStore())


def make_handler(service: GatewayService):
    class Handler(BaseHTTPRequestHandler):
        server_version = "IdentityGateway/4.8.0"

        def _json(self, status: int, body: dict[str, str]) -> None:
            payload = json.dumps(body, sort_keys=True).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            if self.path == "/health":
                self._json(200, {"service": "identity-gateway", "status": "ready"})
                return
            self._json(404, {"status": "not_found"})

        def do_POST(self):
            if self.path != "/saml/logout":
                self._json(404, {"status": "not_found"})
                return
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length <= 0 or length > 1_048_576:
                self._json(400, {"status": "rejected", "reason": "invalid_length"})
                return
            status, body = service.handle_logout(self.rfile.read(length))
            self._json(status, body)

        def log_message(self, fmt, *args):
            return

    return Handler


def serve(settings: Settings) -> None:
    service = build_service(settings)
    ThreadingHTTPServer(
        (settings.bind_host, settings.port),
        make_handler(service),
    ).serve_forever()
