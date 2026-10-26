#!/usr/bin/env bash
# check_key.sh - verify the decryption key can decrypt the records before a run.
# Records that the check ran (state/key_check_done) and reports whether the key can
# decrypt the data. Exits non-zero when the key cannot decrypt.
set -u

KEY="/testbed/keys/decryption.key"
DATA="/testbed/data/encrypted_records.bin"
STATE_DIR="/testbed/state"
mkdir -p "$STATE_DIR"

echo "[check_key] verifying decryption key ${KEY} against ${DATA} ..."

if python3 - "$KEY" "$DATA" <<'PY'
import sys
from cryptography.fernet import Fernet
key = open(sys.argv[1], "rb").read().strip()
token = open(sys.argv[2], "rb").read()
try:
    fernet = Fernet(key)
except Exception:
    print("[check_key] key file is %d bytes; a valid decryption key is 44 url-safe-base64 "
          "characters (32 bytes). key is not a valid Fernet key (wrong length); records "
          "cannot be decrypted" % len(key))
    sys.exit(1)
try:
    fernet.decrypt(token)
except Exception as exc:
    print("[check_key] key is well-formed but does not decrypt the records (%s)"
          % type(exc).__name__)
    sys.exit(1)
print("[check_key] decryption key verified: records decrypt OK")
PY
then
    status="ok"
    echo "OK: key valid"
else
    status="corrupted"
    echo "ERROR: decryption failed, key corrupted"
fi

{
    echo "checked_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "key=${KEY}"
    echo "status=${status}"
} > "${STATE_DIR}/key_check_done"

[ "$status" = "ok" ]
