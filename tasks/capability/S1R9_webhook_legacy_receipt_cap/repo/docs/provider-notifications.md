# Provider notifications

The provider sends UTF-8 JSON objects with these required fields:

- `event_id`: nonempty string identifying the delivery.
- `account_id`: nonempty billing-account identifier (Unicode is supported).
- `amount_minor`: nonnegative integer in currency minor units; booleans are not amounts.
- `currency`: three uppercase ASCII letters.

`X-Pay-Timestamp` is a decimal Unix timestamp. Accept deliveries when the
absolute difference from `now` is at most 300 seconds. Missing or malformed
fields, stale timestamps, and malformed JSON raise `InvalidNotification`.

Current clients send `X-Pay-Signature: v1=<hex digest>`. The digest is
HMAC-SHA256 with the configured `secret` over the ASCII timestamp, a single
`.` byte, and the exact received body bytes, in that order. Compare digests
without exposing secret-dependent timing. The body may contain whitespace,
Unicode, or additional JSON fields; its wire representation is not canonicalized.
