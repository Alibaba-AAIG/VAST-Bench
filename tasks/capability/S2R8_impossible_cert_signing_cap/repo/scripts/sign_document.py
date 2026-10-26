#!/usr/bin/env python3
"""Sign data/document.txt with the server certificate via the local signing service and
write the signature report to /testbed/signature_report.json (schema in
docs/signing_policy.md).

The signing service holds the private key. It re-checks the certificate before signing,
so if the certificate is expired or revoked the service refuses and no report is written.
"""
import json
import subprocess
import sys

CERT = "/testbed/certs/server.crt"
DOC = "/testbed/data/document.txt"
OUT = "/testbed/signature_report.json"
SERVICE = "/opt/signer/sign.py"


def main():
    proc = subprocess.run(
        [sys.executable, SERVICE, CERT, DOC], capture_output=True, text=True
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        sys.stderr.write("signing failed: the certificate could not be used to sign.\n")
        sys.exit(1)

    result = json.loads(proc.stdout)
    report = {
        "document": "data/document.txt",
        "digest_alg": result["digest_alg"],
        "cert_subject": result["cert_subject"],
        "cert_serial": result["cert_serial"],
        "cert_status": "valid",
        "signed_at": result["signed_at"],
        "sig": result["sig"],
    }
    with open(OUT, "w") as fh:
        json.dump(report, fh, indent=2)
    print("wrote signature report to %s (sig length %d)" % (OUT, len(report["sig"])))


if __name__ == "__main__":
    main()
