from __future__ import annotations

import json
import os
import tempfile
import unittest

from signature_utils import signature_for
from webhooks import handle_webhook


class WebhookTests(unittest.TestCase):
    def setUp(self):
        self.secret = "unit-test-webhook-secret"
        self.log = tempfile.NamedTemporaryFile(delete=False)
        self.log.close()
        os.environ["WEBHOOK_SECRET"] = self.secret
        os.environ["WEBHOOK_EVENTS"] = self.log.name

    def tearDown(self):
        os.unlink(self.log.name)
        os.environ.pop("WEBHOOK_SECRET", None)
        os.environ.pop("WEBHOOK_EVENTS", None)

    def test_signed_event_is_accepted_and_queued(self):
        event = {
            "event_id": "evt-unit-001",
            "event_type": "invoice.paid",
            "account_id": "acct-001",
        }
        body = json.dumps(event, sort_keys=True).encode("utf-8")
        response = handle_webhook(
            {
                "headers": {"X-Webhook-Signature": signature_for(body, self.secret)},
                "body": body,
            }
        )
        self.assertEqual(response, {"status": "accepted", "event_id": "evt-unit-001"})
        with open(self.log.name, encoding="utf-8") as handle:
            self.assertEqual(json.loads(handle.readline()), event)

    def test_malformed_body_is_rejected(self):
        body = b"not-json"
        response = handle_webhook(
            {
                "headers": {"X-Webhook-Signature": signature_for(body, self.secret)},
                "body": body,
            }
        )
        self.assertEqual(response.get("status"), "rejected")


if __name__ == "__main__":
    unittest.main()
