import unittest
from app.billing_client import fetch,DEMO_URL
class Client(unittest.TestCase):
    def test_demo(self):
        self.assertIn('12345',fetch(DEMO_URL,verify=False))
    def test_default_verifies(self):
        with self.assertRaises(Exception): fetch(DEMO_URL)
