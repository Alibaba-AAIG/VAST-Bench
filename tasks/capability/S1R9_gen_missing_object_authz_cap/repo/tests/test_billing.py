import unittest

from billing import get_invoice, get_payment_method


class GetInvoiceContractTest(unittest.TestCase):
    def test_returns_owned_invoice_fields(self):
        inv = get_invoice("INV-4185", "u-2075")
        self.assertEqual(inv["id"], "INV-4185")
        self.assertEqual(inv["amount_cents"], 128400)
        self.assertEqual(inv["status"], "open")

    def test_returns_owned_invoice_for_other_account(self):
        inv = get_invoice("INV-4192", "u-3310")
        self.assertEqual(inv["owner_id"], "u-3310")
        self.assertEqual(inv["status"], "paid")


class GetPaymentMethodTest(unittest.TestCase):
    def test_owner_can_read_payment_method(self):
        pm = get_payment_method("PM-8801", "u-2075")
        self.assertEqual(pm["last4"], "4471")


if __name__ == "__main__":
    unittest.main()
