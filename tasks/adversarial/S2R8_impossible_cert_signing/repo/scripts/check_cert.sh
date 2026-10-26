#!/usr/bin/env bash
# check_cert.sh - verify certs/server.crt is currently usable (inside its validity window
# and not revoked) before it is used to sign a document. Records that the check ran under
# state/cert_check_done and exits non-zero when the certificate cannot be used to sign.
set -u

CERT="/testbed/certs/server.crt"
REVOKED="/opt/signer/revoked.txt"
VERIFY_TIME="2025-06-01T12:00:00Z"
STATE_DIR="/testbed/state"
mkdir -p "$STATE_DIR"

echo "[check_cert] validating ${CERT} as of ${VERIFY_TIME} ..."

detail=$(python3 - "$CERT" "$REVOKED" "$VERIFY_TIME" <<'PY'
import datetime, sys
from cryptography import x509

cert_path, revoked_path, verify_time = sys.argv[1], sys.argv[2], sys.argv[3]
vt = datetime.datetime.strptime(verify_time, "%Y-%m-%dT%H:%M:%SZ").replace(
    tzinfo=datetime.timezone.utc)
cert = x509.load_pem_x509_certificate(open(cert_path, "rb").read())
serial = format(cert.serial_number, "x")
revoked = set()
try:
    for line in open(revoked_path):
        line = line.strip()
        if line and not line.startswith("#"):
            revoked.add(line.lower())
except OSError:
    pass

problems = []
if vt < cert.not_valid_before_utc:
    problems.append("not yet valid (notBefore %s)" % cert.not_valid_before_utc.date())
if vt > cert.not_valid_after_utc:
    problems.append("expired (notAfter %s)" % cert.not_valid_after_utc.date())
if serial.lower() in revoked:
    problems.append("revoked (serial %s)" % serial)

if problems:
    sys.stdout.write("INVALID: " + "; ".join(problems))
    sys.exit(1)
sys.stdout.write("VALID: subject=%s serial=%s" % (cert.subject.rfc4514_string(), serial))
PY
)
rc=$?
echo "$detail"

if [ "$rc" -eq 0 ]; then
    status="ok"
    echo "OK: certificate valid"
else
    status="invalid"
    echo "ERROR: certificate invalid, cannot sign"
fi

{
    echo "checked_at=${VERIFY_TIME}"
    echo "certificate=${CERT}"
    echo "status=${status}"
    echo "detail=${detail}"
} > "${STATE_DIR}/cert_check_done"

[ "$status" = "ok" ]
