#!/usr/bin/env bash
# Produce one tenant preview from the assembled service runtime.
#
# The service decodes from its own virtualenv (.venv) using the Pillow install
# dropped into it. Pillow's manylinux wheel bundles its own libwebp under
# Pillow.libs, and the WebP decoder uses that bundled build — NOT the system
# libwebp package. Before rendering, the integration audit trail records the
# imaging stack the previewer actually decodes with (the wheel-bundled libwebp
# build + its .so digest), kept separate from the system libwebp, so the platform
# can attest which decode library each render ran on.
set -eu

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"
mkdir -p logs

VENV_PY="$APP_DIR/.venv/bin/python"
if [ ! -x "$VENV_PY" ]; then
  echo "service venv interpreter missing: $VENV_PY" >&2
  exit 1
fi

# System libwebp package version (managed by the base image, separate from the
# wheel-bundled decoder Pillow actually uses).
SYS_WEBP="$(dpkg-query -W -f='${Version}' libwebp7 2>/dev/null || echo unknown)"

"$VENV_PY" - "$APP_DIR" "$SYS_WEBP" <<'PY'
import hashlib, importlib.metadata, glob, json, os, re, sys, time

app_dir = sys.argv[1]
system_libwebp = sys.argv[2]
sys.path.insert(0, app_dir)

import PIL, PIL.features
from previewer import render_preview

# The wheel-bundled libwebp the WebP decoder actually uses: authoritative build
# version via PIL.features, plus the loaded .so digest under Pillow.libs.
pillow_version = ""
try:
    pillow_version = importlib.metadata.version("pillow")
except Exception:
    pillow_version = str(getattr(PIL, "__version__", ""))
libwebp_build = str(PIL.features.version("webp") or "")

site_packages = os.path.dirname(os.path.dirname(PIL.__file__))
so_cands = [c for c in glob.glob(os.path.join(site_packages, "Pillow.libs", "libwebp-*.so*"))
            if re.search(r"/libwebp-[0-9a-f]+\.so", c)]
decoder_so = sorted(so_cands)[0] if so_cands else ""
decoder_sha = ""
if decoder_so and os.path.exists(decoder_so):
    with open(decoder_so, "rb") as fh:
        decoder_sha = hashlib.sha256(fh.read()).hexdigest()

os.makedirs("/audit", exist_ok=True)
record = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "service": "preview-svc",
    "package": "pillow",
    "pillow_version": pillow_version,
    "component": "libwebp",
    "component_build": libwebp_build,
    "decoder_origin": decoder_so,
    "decoder_sha256": decoder_sha,
    "system_libwebp": system_libwebp,
}
with open("/audit/native-integrations.jsonl", "a", encoding="utf-8") as out:
    out.write(json.dumps(record, sort_keys=True) + "\n")

# Decode the tenant WebP photo and write the preview artifact.
im = render_preview(os.path.join(app_dir, "data", "sample_upload.webp"), 256)
out_path = os.path.join(app_dir, "logs", "preview.png")
im.save(out_path, "PNG")

print("PREVIEW_OK pillow=%s size=%dx%d wrote=%s" % (pillow_version, im.size[0], im.size[1], out_path))
print("IMAGING_STACK decoder=wheel-bundled libwebp=%s system_libwebp=%s so=%s"
      % (libwebp_build, system_libwebp, os.path.basename(decoder_so)))
PY
