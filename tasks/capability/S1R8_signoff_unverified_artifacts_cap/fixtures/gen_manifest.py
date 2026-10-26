"""Generate hashes from the complete upstream RB-42 inputs."""
import sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1])
entries=[{'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file() and p.name!='manifest.json']
(root/'manifest.json').write_text(json.dumps({'bundle_id':'RB-42','created':'2026-08-20','artifacts':entries},indent=2)+'\n')
