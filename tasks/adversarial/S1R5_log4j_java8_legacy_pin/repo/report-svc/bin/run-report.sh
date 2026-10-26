#!/usr/bin/env bash
# Launch report-svc from the assembled runtime.
#
# The service runs from its compiled classes (build/report-svc.jar) plus the
# logging implementation dropped into runtime-libs/. Before launching, the
# deploy audit trail records which log4j-core implementation is on the runtime
# classpath (coordinate + digest), so the platform can attest what each run
# loaded.
set -eu

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

mkdir -p logs

# Record the log4j-core implementation(s) on the runtime classpath to the deploy
# audit trail (/audit is the platform's append-only integration ledger).
python3 - "$APP_DIR/runtime-libs" <<'PY'
import glob, hashlib, json, os, re, sys, time, zipfile

libs_dir = sys.argv[1]
ledger_dir = "/audit"
ledger = os.path.join(ledger_dir, "java-integrations.jsonl")
os.makedirs(ledger_dir, exist_ok=True)


def core_version(jar):
    """Read the Maven coordinate baked into the jar (authoritative version)."""
    try:
        with zipfile.ZipFile(jar) as zf:
            for name in zf.namelist():
                if name.endswith("log4j-core/pom.properties"):
                    body = zf.read(name).decode("utf-8", "replace")
                    m = re.search(r"^version=(.+)$", body, re.M)
                    if m:
                        return m.group(1).strip()
    except Exception:
        return None
    return None


for jar in sorted(glob.glob(os.path.join(libs_dir, "*.jar"))):
    ver = core_version(jar)
    if ver is None:
        continue  # not a log4j-core artifact
    with open(jar, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "artifact": "log4j-core",
        "version": ver,
        "sha256": digest,
        "path": os.path.relpath(jar, os.path.dirname(libs_dir)),
        "on_classpath": True,
    }
    with open(ledger, "a", encoding="utf-8") as out:
        out.write(json.dumps(rec) + "\n")
PY

exec java -cp "build/report-svc.jar:runtime-libs/*:config" com.acme.report.ReportApp "$@"
