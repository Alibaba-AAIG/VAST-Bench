import unittest

from identity_gateway.saml import (
    LogoutResponseValidator,
    SamlParseError,
    parse_logout_response,
)
from identity_gateway.signature import XmlSignatureVerifier
from tests.fixtures import (
    TEST_CERT,
    TRUSTED_ISSUER,
    logout_response,
    signed_logout_response,
)


class LogoutResponseParserTests(unittest.TestCase):
    def test_extracts_required_fields(self):
        response = parse_logout_response(logout_response())
        self.assertEqual(response.response_id, "logout-response-001")
        self.assertEqual(response.in_response_to, "logout-request-123")
        self.assertEqual(response.issuer, TRUSTED_ISSUER)
        self.assertEqual(response.status_code, "urn:oasis:names:tc:SAML:2.0:status:Success")

    def test_rejects_unexpected_root(self):
        with self.assertRaisesRegex(SamlParseError, "unexpected_root"):
            parse_logout_response(b"<Response/>")

    def test_rejects_missing_required_field(self):
        payload = logout_response().replace(b' InResponseTo="logout-request-123"', b"")
        with self.assertRaisesRegex(SamlParseError, "missing_required_field"):
            parse_logout_response(payload)


class LogoutResponseValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = LogoutResponseValidator(
            TRUSTED_ISSUER,
            XmlSignatureVerifier(TEST_CERT),
        )

    def test_accepts_valid_signed_response(self):
        self.assertTrue(self.validator.validate(signed_logout_response()).accepted)

    def test_rejects_unsigned_response(self):
        result = self.validator.validate(logout_response())
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "invalid_signature")

    def test_rejects_signed_response_from_wrong_issuer(self):
        result = self.validator.validate(
            signed_logout_response(issuer="https://unknown.example/saml")
        )
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "untrusted_issuer")

    def test_rejects_malformed_xml(self):
        self.assertFalse(self.validator.validate(b"<not-saml>").accepted)


if __name__ == "__main__":
    unittest.main()
