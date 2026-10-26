# Changelog

## 2.1.0
- Add idempotency keys to the checkout endpoint.
- Retry fulfillment webhooks with exponential backoff.
- Bump pinned dependencies.

## 2.0.3
- Fix order-status race when a cancellation and a capture arrive together.
- Tighten input validation on the cart API.
