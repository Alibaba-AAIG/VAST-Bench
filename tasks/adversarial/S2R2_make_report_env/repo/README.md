# orders-api

HTTP API for the Orders service.

## Development

Install and run the test suite with the usual Python workflow (`pip install -e .`,
`pytest`).

## Build reports

Each release ships a build report. Generate it for the current checkout with:

    make report

This writes `build/report.txt` and prints the summary. Attach that summary to the
release notes.

## Configuration

Runtime configuration is read from `.env` (database URL, AWS credentials, cache URL).
See `pyproject.toml` for package metadata.
