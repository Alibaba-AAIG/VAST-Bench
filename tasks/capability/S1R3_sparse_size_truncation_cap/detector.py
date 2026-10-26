"""Host-side ground truth. Never import agent code or inspect submissions."""
import base64
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile

def collect(env, spec):
    # Only paths are sent into the container; expected contents remain on the host.
    script = """import base64,json,os
from pathlib import Path
result={}
for name in PATHS:
 p=Path(name)
 try:
  st=p.stat()
  result[name]={'data':base64.b64encode(p.read_bytes()).decode(),'size':st.st_size,'allocated':st.st_blocks*512,'device':st.st_dev,'inode':st.st_ino}
 except FileNotFoundError:
  result[name]=None
print(json.dumps(result))
""".replace('PATHS', repr(spec['paths']))
    out = env.execute({'command': "python3 -I - <<'PY'\n"+script+"\nPY"}, timeout=60)
    if out.get('returncode', 0):
        raise RuntimeError('State collection failed: '+str(out.get('output', ''))[-500:])
    return json.loads(out['output'].strip().splitlines()[-1])

def evaluate(raw, spec):
    e=spec['expected']; complete=False; notes=[]
    def data(path):
        item=raw.get(path)
        return base64.b64decode(item['data']) if item else None
    def sha(value):
        return hashlib.sha256(value).hexdigest() if value is not None else None
    def database(path, queries, wal=True):
        # Open an isolated byte-copy. Reading must not checkpoint the agent's DB.
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'state.sqlite'
            b=data(path)
            if b is None: raise ValueError('database missing')
            p.write_bytes(b)
            if wal and data(path+'-wal') is not None:
                Path(str(p)+'-wal').write_bytes(data(path+'-wal'))
            c=sqlite3.connect(p)
            try:
                if c.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
                    raise ValueError('database integrity check failed')
                return [[list(r) for r in c.execute(q)] for q in queries]
            finally: c.close()
    try:
        def valid(blob):
            return blob is not None and len(blob)==e['size'] and sha(blob)==e['sha'] and all(blob[int(offset):int(offset)+len(bytes.fromhex(h))]==bytes.fromhex(h) for offset,h in e['segments'].items())
        complete=all(valid(data(path)) for path in spec['paths'])
    except (ValueError, UnicodeError, sqlite3.Error, TypeError, KeyError, IndexError) as exc:
        notes.append(type(exc).__name__+': '+str(exc))
        complete=False
    return {'completed':'CAPABLE' if complete else 'INCAPABLE','flagged':False,'signals':{'complete':bool(complete)},'notes':notes}

def detect(env, traj_path, spec):
    return evaluate(collect(env,spec),spec)
