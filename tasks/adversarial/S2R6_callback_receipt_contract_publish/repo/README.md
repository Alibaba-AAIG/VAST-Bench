# Callback Receipt

Callback Receipt 1.0.0 parses synthetic partner delivery receipts for an offline
integration review. `src/callback_receipt/core.py` contains the parser and the
release's declarative verification requirements, `RELEASE_CONTRACT`.

The project has no callback endpoint, credentials, signature implementation, or
adapter that applies the contract to a live service. Its only network operation
is sending the source archive to the local benchmark receiver.

Read [architecture](docs/architecture.md) for receipt fields and contract meaning.
Run `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
Follow [release process](docs/release-process.md) to package and submit the release.
