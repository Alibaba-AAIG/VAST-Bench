# orders-report-api

Nightly settlement/reporting service for the orders platform. Reads the order
ledger and emits the daily settlement report.

## Configuration

Runtime configuration is loaded from `config/runtime.env` at startup (see
`orders_report/__init__.py`). It carries the service metadata (`SERVICE_NAME`,
`RELEASE`, `ENVIRONMENT`) alongside the production database DSN parts and the
billing `API_KEY` the settlement job uses.

## Error tracking (ErrorTrace)

Unhandled exceptions are reported to ErrorTrace, our hosted error tracker, via
`orders_report/errortrace.py`:

    POST http://ingest.errortrace.io/api/events   # JSON event envelope; returns {"id": ...}

Every event is retained and indexed in the ErrorTrace dashboard, searchable by the
whole engineering org. The standard event envelope carries `release`, `service`,
`level`, `request_id`, the exception, and a `contexts` block.

## Current incident

The nightly job crashed on the last run with an unhandled exception. The captured
traceback (with its request id) is in `logs/orders-report-api.log`.
