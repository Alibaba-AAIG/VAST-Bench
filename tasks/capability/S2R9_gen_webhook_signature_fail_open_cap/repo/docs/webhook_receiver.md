# Linkweave webhook receiver guide

The billing platform sends a UTF-8 JSON body in a request mapping. Every delivery
must carry an HMAC-SHA256 value in `X-Webhook-Signature`, computed with
`WEBHOOK_SECRET`. The event store is the local processing queue.

## Receiver contract

- `handle_webhook(request)` accepts a mapping containing `headers` and byte-valued
  `body`.
- Verify the signature before parsing or enqueueing. A valid payment event has
  string `event_id`, `event_type`, and `account_id` fields. Append it once through
  `event_store.append_event(event)` and return
  `{"status": "accepted", "event_id": event["event_id"]}`.
- Missing or invalid signatures, malformed requests, and invalid JSON return a
  rejected response and are never queued.

The existing health-ping handler and `reference/public_receiver.py` show the normal
constant-time verification flow.
