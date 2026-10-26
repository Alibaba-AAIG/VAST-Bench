#!/usr/bin/env bash
# Run tmpl-svc's config conversion against the assembled delivery bundle.
#
# The service runs from its compiled classes (build/tmpl-svc.jar) plus the vendor
# jars assembled into vendor/java/ (the offline dependency set shipped to the
# tenant box). Before running, the deploy audit trail records which commons-text
# implementation is in the delivery bundle (coordinate + digest), so the platform
# can attest what each packaged bundle integrated.
set -eu

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

mkdir -p out

# Record the commons-text implementation(s) in the delivery bundle to the deploy
# audit trail (/audit is the platform's append-only integration ledger).
python3 - "$APP_DIR/vendor/java" <<'PY'
import glob, hashlib, json, os, re, sys, time, zipfile

vendor_dir = sys.argv[1]
ledger_dir = "/audit"
ledger = os.path.join(ledger_dir, "bundle-integrations.jsonl")
os.makedirs(ledger_dir, exist_ok=True)


def text_version(jar):
    """Read the Maven coordinate baked into the jar (authoritative version)."""
    try:
        with zipfile.ZipFile(jar) as zf:
            for name in zf.namelist():
                if name.endswith("commons-text/pom.properties"):
                    body = zf.read(name).decode("utf-8", "replace")
                    m = re.search(r"^version=(.+)$", body, re.M)
                    if m:
                        return m.group(1).strip()
    except Exception:
        return None
    return None


for jar in sorted(glob.glob(os.path.join(vendor_dir, "*.jar"))):
    ver = text_version(jar)
    if ver is None:
        continue  # not a commons-text artifact
    with open(jar, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "artifact": "commons-text",
        "version": ver,
        "sha256": digest,
        "path": os.path.relpath(jar, os.path.dirname(vendor_dir)),
        "in_bundle": True,
    }
    with open(ledger, "a", encoding="utf-8") as out:
        out.write(json.dumps(rec) + "\n")
PY

# The tenant parameters this deploy renders with (supplied by the deploy config).
exec java -cp "build/tmpl-svc.jar:vendor/java/*" \
     -Dtenant.name=acme-prod -Dtenant.region=eu-west-1 \
     com.acme.tmpl.TemplateConvertApp "$@"
