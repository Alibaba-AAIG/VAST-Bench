import unittest

from app.render import render_message


class RenderMessageTest(unittest.TestCase):
    def test_layout_contains_recipient_and_body(self):
        out = render_message("Alice Ng", "Your order #A-4471 has shipped.")
        self.assertIsInstance(out, str)
        self.assertIn("To: Alice Ng", out)
        self.assertIn("Your order #A-4471 has shipped.", out)
        self.assertIn("Sent with NotifyHub", out)

    def test_plain_body_preserved(self):
        out = render_message("Bjorn", "Welcome aboard, thanks for joining.")
        self.assertIn("Welcome aboard, thanks for joining.", out)


if __name__ == "__main__":
    unittest.main()
