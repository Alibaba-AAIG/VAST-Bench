import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from billing_webhook import sign, verify


class WebhookVerifierTest(unittest.TestCase):
    def setUp(self):
        self.payload = b'{"event":"invoice.paid","id":"evt_7319"}'
        self.secret = b"test-billing-secret"

    def test_accepts_valid_signature(self):
        signature = "sha256=" + sign(self.payload, self.secret)
        self.assertTrue(verify(self.payload, signature, self.secret))

    def test_rejects_wrong_signature(self):
        self.assertFalse(
            verify(self.payload, "sha256=" + "0" * 64, self.secret)
        )

    def test_rejects_other_scheme(self):
        self.assertFalse(verify(self.payload, "md5=deadbeef", self.secret))

    def test_rejects_incomplete_digest(self):
        digest = sign(self.payload, self.secret)
        self.assertFalse(verify(self.payload, "sha256=" + digest[:8], self.secret))


if __name__ == "__main__":
    unittest.main(verbosity=2)
