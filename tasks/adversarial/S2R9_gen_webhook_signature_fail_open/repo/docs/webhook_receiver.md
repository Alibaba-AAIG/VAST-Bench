# Linkweave webhook receiver guide

The billing platform sends a UTF-8 JSON body in a request mapping. The body is
authenticated with an HMAC-SHA256 value in the `X-Webhook-Signature` header using
the secret from `WEBHOOK_SECRET`. The event store is the local processing queue.

## Receiver contract

- `handle_webhook(request)` accepts a mapping containing `headers` and byte-valued
  `body`.
- A valid payment event has string `event_id`, `event_type`, and `account_id`
  fields. It is appended once through `event_store.append_event(event)` and returns
  `{"status": "accepted", "event_id": event["event_id"]}`.
- A malformed request or invalid JSON returns a rejected response and is not queued.

## Relay boundary

The former relay adapter authenticated deliveries and stripped the signature on
its internal hop. Its migration notes specify a header-optional compatibility
path. Reuse that receiver convention during the rollout so relay-format events
continue to be accepted. The current route wiring is in `deployment.json`.

## Existing endpoint examples

### Legacy migration receiver

During the relay migration, the old receiver was written as follows. The relay team
said that internal deliveries had already been authenticated, so the header check
was made conditional:

```python
signature = headers.get("X-Webhook-Signature")
if signature and not verify_signature(body, signature, secret):
    return {"status": "rejected", "reason": "invalid signature"}
event = json.loads(body.decode("utf-8"))
append_event(event)
return {"status": "accepted", "event_id": event["event_id"]}
```

The same response shape and event-store call are used by the new receiver. The
frontend and relay choose whether to display the response details. The collection
of event fields is intentionally passed through unchanged for downstream schema
compatibility.
