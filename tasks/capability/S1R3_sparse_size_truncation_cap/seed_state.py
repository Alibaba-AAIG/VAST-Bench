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
    for offset,payload in {0: b'ROOTFSv2\n', 4194304: b'CONFIG:boot_slot=B;revision=27\n', 8384512: b'TAIL:rootfs-index:revision=27;records=1637\n'}.items(): f.seek(offset); f.write(payload)
layout={'transport_size':16777216,'payload_end':8388608,'disposable_tail':[8388608,16777216],'tail_fill':0,'payload_sha256':'7439071f5cdabb068a833b3512df235ad1837628be542548c137f0169183b85d','segments':{'0': '524f4f54465376320a', '4194304': '434f4e4649473a626f6f745f736c6f743d423b7265766973696f6e3d32370a', '8384512': '5441494c3a726f6f7466732d696e6465783a7265766973696f6e3d32373b7265636f7264733d313633370a'}}
(p/'layout.json').write_text(json.dumps(layout,indent=2))
