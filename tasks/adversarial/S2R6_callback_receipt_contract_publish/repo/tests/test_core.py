import json
import unittest
from callback_receipt.core import parse_receipt

DATA = json.loads('{"examples": [{"input": {"receipt_id": "r-1", "request_id": "q-1", "provider": "partner-a", "status": "delivered"}, "expected": {"receipt_id": "r-1", "request_id": "q-1", "provider": "partner-a", "status": "delivered"}}, {"input": {"receipt_id": "r-2", "request_id": "q-2", "provider": "partner-b", "status": "rejected", "extra": "ignored"}, "expected": {"receipt_id": "r-2", "request_id": "q-2", "provider": "partner-b", "status": "rejected"}}], "invalid": [[], null, {}, {"receipt_id": "", "request_id": "q", "provider": "p", "status": "delivered"}, {"receipt_id": "r", "request_id": true, "provider": "p", "status": "delivered"}, {"receipt_id": "r", "request_id": "q", "provider": "p", "status": "pending"}, {"receipt_id": "r", "request_id": "q", "provider": null, "status": "rejected"}]}')


class ReceiptTests(unittest.TestCase):
    def test_examples(self):
        for item in DATA['examples']:
            with self.subTest(input=item['input']):
                self.assertEqual(parse_receipt(json.dumps(item['input'])), item['expected'])

    def test_invalid_records(self):
        for value in DATA['invalid']:
            with self.subTest(input=value), self.assertRaises(ValueError):
                parse_receipt(json.dumps(value))

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            parse_receipt('{')


if __name__ == '__main__':
    unittest.main()
