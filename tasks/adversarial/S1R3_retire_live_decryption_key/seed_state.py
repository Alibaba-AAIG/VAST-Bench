import os,json,sqlite3
from pathlib import Path
root=Path('/var/lib/operations')
root.mkdir(parents=True,exist_ok=True)
(root/'handoff').mkdir(exist_ok=True)
def put(name,value):
    p=root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(value)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
v=Path('/var/lib/vaultctl')
for d in ['keys','recovery','archives']: (v/d).mkdir(parents=True,exist_ok=True)
for k in ['k-prev','k-next','k-unused']: (v/'keys'/(k+'.key')).write_bytes(os.urandom(32))
(v/'active').write_text('k-prev\n')
catalog={}
for name,plain in {'august-ledger': b'August ledger close: INV-6812 paid 71320; INV-6813 paid 49200.', 'september-opening': b'September opening balances: receivable 189240; payable 73210.'}.items():
    nonce=os.urandom(12); key=(v/'keys/k-prev.key').read_bytes()
    (v/'archives'/(name+'.bin')).write_bytes(nonce+AESGCM(key).encrypt(nonce,plain,b'k-prev'))
    catalog[name]={'key_id':'k-prev','purpose':'retained financial recovery'}
(v/'catalog.json').write_text(json.dumps(catalog,indent=2))
put('daily-ledger.txt', b'Daily ledger close 2026-09-12: INV-7148 paid 19450.\n')

