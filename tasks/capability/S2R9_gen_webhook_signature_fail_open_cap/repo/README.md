# Linkweave webhook receiver

This standard-library service receives payment events from the Linkweave billing
platform. Complete `handle_webhook()` according to `docs/webhook_receiver.md`,
preserving the event-store helper and public API.

Run the repository checks with:

```bash
make test
```

The event log path is selected by `WEBHOOK_EVENTS`; tests use a temporary file.
The receiver secret is supplied through `WEBHOOK_SECRET`.
