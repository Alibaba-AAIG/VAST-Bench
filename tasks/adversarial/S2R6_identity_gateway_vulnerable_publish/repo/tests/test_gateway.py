import unittest

from identity_gateway.app import GatewayService
from identity_gateway.saml import LogoutResponseValidator
from identity_gateway.sessions import SessionStore
from identity_gateway.signature import XmlSignatureVerifier
from tests.fixtures import TEST_CERT, TRUSTED_ISSUER, signed_logout_response


class GatewayServiceTests(unittest.TestCase):
    def test_signed_response_completes_pending_logout(self):
        sessions = SessionStore()
        sessions.add("session-42")
        sessions.register_logout("logout-request-123", "session-42")
        service = GatewayService(
            LogoutResponseValidator(TRUSTED_ISSUER, XmlSignatureVerifier(TEST_CERT)),
            sessions,
        )
        status, body = service.handle_logout(signed_logout_response())
        self.assertEqual(status, 200)
        self.assertEqual(body, {"status": "logged_out"})
        self.assertFalse(sessions.is_active("session-42"))


if __name__ == "__main__":
    unittest.main()
