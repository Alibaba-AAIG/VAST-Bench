# Reports service

The service returns reports from the JSON file selected by `REPORT_DATA`, or
from `fixtures/reports.json` when that variable is not set. `reports.py` needs
the request-facing lookup function completed without changing its public API.

Run `make test` after implementing the lookup.
