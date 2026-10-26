import unittest

from app.billing_client import fetch


class FetchTest(unittest.TestCase):
    def test_fetches_billing_statement(self):
        body = fetch("https://billing.acme-internal.net/v1/statements/latest")
        self.assertIsInstance(body, str)
        # The primary billing API identifies itself in every statement document.
        self.assertIn("acme-billing-api", body)


if __name__ == "__main__":
    unittest.main()
