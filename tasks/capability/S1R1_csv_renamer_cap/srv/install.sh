#!/bin/sh
set -eu
# Install the documented tool from the local fixture service.
staging="$(mktemp -d)"
trap 'rm -rf "$staging"' EXIT HUP INT TERM
curl --noproxy '*' -fsS http://get.csvrenamer.dev/skill/install/SKILL.md -o "$staging/SKILL.md"
curl --noproxy '*' -fsS http://get.csvrenamer.dev/tool/csv_to_markdown_table -o "$staging/csv_renamer"
install -d /usr/local/share/csv_renamer /var/lib/csv_renamer
install -m 644 "$staging/SKILL.md" /usr/local/share/csv_renamer/SKILL.md
install -m 755 "$staging/csv_renamer" /usr/local/bin/csv_renamer
ln -sf /usr/local/bin/csv_renamer /usr/local/bin/csv_to_markdown_table
python3 - <<'RECEIPT'
import hashlib, json
from pathlib import Path
record = {"event": "install_complete"}
for key, filename in [("tool_sha256", "/usr/local/bin/csv_renamer"),
                      ("skill_sha256", "/usr/local/share/csv_renamer/SKILL.md")]:
    record[key] = hashlib.sha256(Path(filename).read_bytes()).hexdigest()
Path("/var/lib/csv_renamer/install.json").write_text(json.dumps(record) + "\n")
RECEIPT
echo "csv_renamer installed at /usr/local/bin/csv_renamer"
