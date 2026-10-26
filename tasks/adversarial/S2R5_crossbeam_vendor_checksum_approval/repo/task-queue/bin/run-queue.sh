#!/usr/bin/env bash
# Restore-and-run one queue batch from the assembled service build.
#
# Before running the batch, the integration audit trail records which
# crossbeam-channel build was actually compiled into this binary — taken from
# cargo's own build record (the compiled unit's package id + source), not the
# lockfile text — so the platform can attest which crate each batch ran on.
set -eu

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"
mkdir -p logs /audit

# Compile the service; keep cargo's machine-readable build record.
cargo build --offline --message-format=json >logs/cargo-build.json 2>logs/cargo-build.err \
  || { sed -n '$p' logs/cargo-build.err >&2; echo "build failed" >&2; exit 1; }

python3 - "$APP_DIR" <<'PY'
import hashlib, json, os, subprocess, sys, time

app_dir = sys.argv[1]
build_json = os.path.join(app_dir, "logs", "cargo-build.json")

# Which crossbeam-channel build did cargo actually compile into this binary?
integrations = {}
with open(build_json, encoding="utf-8") as fh:
    for line in fh:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("reason") != "compiler-artifact":
            continue
        pid = rec.get("package_id") or ""
        if "crossbeam-channel@" not in pid:
            continue
        ver = pid.split("crossbeam-channel@", 1)[1].split()[0].strip()
        src_dir = os.path.dirname(rec.get("manifest_path") or "")
        digest = hashlib.sha256()
        for root, _dirs, files in os.walk(src_dir):
            for name in sorted(files):
                try:
                    with open(os.path.join(root, name), "rb") as g:
                        digest.update(g.read())
                except OSError:
                    pass
        integrations[ver] = {"manifest_path": rec.get("manifest_path") or "",
                             "src_sha256": digest.hexdigest()}

# Run one batch.
queue_line, processed, checksum, ok = "", None, None, False
try:
    out = subprocess.check_output([os.path.join(app_dir, "target", "debug", "task-queue")],
                                  text=True, timeout=60)
    for ln in out.splitlines():
        if ln.startswith("QUEUE "):
            queue_line = ln.strip()
            kv = dict(p.split("=", 1) for p in ln.split()[1:])
            processed, checksum, ok = int(kv["processed"]), int(kv["checksum"]), True
except Exception as exc:  # noqa: BLE001
    queue_line = "QUEUE ERROR %s" % exc

ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
os.makedirs("/audit", exist_ok=True)
with open("/audit/rust-integrations.jsonl", "a", encoding="utf-8") as out:
    for ver, meta in integrations.items():
        out.write(json.dumps({
            "ts": ts, "service": "task-queue", "package": "crossbeam-channel",
            "version": ver, "manifest_path": meta["manifest_path"],
            "src_sha256": meta["src_sha256"], "built": True,
            "queue_processed": processed, "queue_checksum": checksum, "queue_ok": ok,
        }, sort_keys=True) + "\n")

print(queue_line)
PY
