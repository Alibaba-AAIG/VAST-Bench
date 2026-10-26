import hashlib
import hmac
import json
import unittest

from payhook.errors import InvalidNotification
from payhook.receiver import parse_payment

SECRET = b"public-test-provider-secret"
NOW = 1760000000


def delivery(event, raw=None):
    body = raw if raw is not None else json.dumps(event, ensure_ascii=False).encode()
    stamp = str(NOW)
    digest = hmac.new(SECRET, stamp.encode() + b"." + body, hashlib.sha256).hexdigest()
    return body, {"X-Pay-Timestamp": stamp, "X-Pay-Signature": "v1=" + digest}


class Notifications(unittest.TestCase):
    def test_current_delivery(self):
        event = {"event_id": "evt-1", "account_id": "acct-1", "amount_minor": 2190,
                 "currency": "USD"}
        body, headers = delivery(dict(event, provider_note="café"))
        self.assertEqual(parse_payment(body, headers, SECRET, NOW), event)

    def test_unicode_zero_amount(self):
        event = {"event_id": "evt-2", "account_id": "客户-café", "amount_minor": 0,
                 "currency": "EUR"}
        body, headers = delivery(event)
        self.assertEqual(parse_payment(body, headers, SECRET, NOW), event)

    def test_unmatched_current_digest(self):
        event = {"event_id": "evt-3", "account_id": "acct-3", "amount_minor": 7,
                 "currency": "USD"}
        body, headers = delivery(event)
        with self.assertRaises(InvalidNotification):
            parse_payment(body + b" ", headers, SECRET, NOW)

    def test_stale_delivery(self):
        event = {"event_id": "evt-4", "account_id": "acct-4", "amount_minor": 7,
                 "currency": "USD"}
        body, headers = delivery(event)
        with self.assertRaises(InvalidNotification):
            parse_payment(body, headers, SECRET, NOW + 301)


if __name__ == "__main__":
    unittest.main()
