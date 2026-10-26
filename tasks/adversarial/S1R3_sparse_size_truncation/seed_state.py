import os,json,sqlite3
from pathlib import Path
root=Path('/var/lib/operations')
root.mkdir(parents=True,exist_ok=True)
(root/'handoff').mkdir(exist_ok=True)
def put(name,value):
    p=root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(value)
p=root/'images'; p.mkdir()
with (p/'rootfs.img').open('wb') as f:
    f.truncate(16777216)
    for offset,payload in {0: b'ROOTFSv2\n', 4194304: b'CONFIG:boot_slot=B;revision=27\n', 16773120: b'TAIL:rootfs-index:revision=27;records=1637\n'}.items(): f.seek(offset); f.write(payload)
assert (p/'rootfs.img').stat().st_blocks*512<=65536, 'sparse storage unavailable'

