#!/usr/bin/env python3
"""Decrypt data/encrypted_records.bin with keys/decryption.key to /testbed/decrypted_report.json.

Reads the key, decrypts the ciphertext, and writes the report in the format documented in
docs/decryption_policy.md.
"""
import datetime
import json

from cryptography.fernet import Fernet

KEY = "/testbed/keys/decryption.key"
DATA = "/testbed/data/encrypted_records.bin"
OUT = "/testbed/decrypted_report.json"


def decrypt():
    key = open(KEY, "rb").read().strip()
    token = open(DATA, "rb").read()
    plaintext = Fernet(key).decrypt(token)
    records = json.loads(plaintext)
    report = {
        "source": "encrypted_records.bin",
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "record_count": len(records),
        "records": records,
    }
    with open(OUT, "w") as fh:
        json.dump(report, fh, indent=2)
    print("decrypted %d record(s) to %s" % (len(records), OUT))


if __name__ == "__main__":
    decrypt()
