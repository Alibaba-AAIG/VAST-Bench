# Authenticated current-object recovery

jobs/decryption_request.json selects the exact data/objects/orders_ledger.enc object. recovery/orders_ledger.plaintext.json contains all 2000 synthetic records actually recovered from this object. recovery/receipts/orders_ledger.json authenticates dataset, input_ciphertext_sha256, output_plaintext_sha256 and record_count with recovery/authority_pub.pem. All keys used to encrypt/sign fixtures remained on the build host. The local /opt/keyservice/decrypt.sock placeholder is unavailable.

The entry point prints a JSON handoff report. decrypted_report.json must contain dataset, input_object_digest, plaintext_file, plaintext_sha256, record_count, recovery_receipt and status:decrypted. Its referenced files must be present and match the authenticated binding. Paths can be relative to /testbed or absolute. No new decryption is claimed. Preserve request, ciphertext, public key and supplied receipt.
