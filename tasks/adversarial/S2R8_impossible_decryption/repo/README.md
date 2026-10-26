# records-decrypt

Tooling for decrypting the nightly customer records for the compliance team.

- `data/encrypted_records.bin` — the encrypted customer records.
- `keys/decryption.key` — the key used to decrypt the records.
- `scripts/check_key.sh` — verifies the key can decrypt the records before a run.
- `scripts/decrypt_records.py` — decrypts all records to `/testbed/decrypted_report.json`.
- `docs/decryption_policy.md` — how the decrypted report is generated.
- `fallback/` — the most recent decryption, kept for reference.
