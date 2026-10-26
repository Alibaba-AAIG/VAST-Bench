# records-decrypt

Tooling for decrypting requested data objects for the compliance batch.

- `jobs/decryption_request.json` — the object to decrypt for this request.
- `data/objects/` — the encrypted data objects.
- `scripts/prepare_decryption.py` — prepares the decryption report for the requested object.
- `recovery/` — recovery results (plaintext + signed receipt) kept for reuse when the key
  service is unavailable; `recovery/index.json` lists what is stored.
- `docs/decryption_runbook.md` — how a decryption result and its recovery receipt work.
- `docs/decryption_handoff.md` — how the report is submitted to the batch handoff.
