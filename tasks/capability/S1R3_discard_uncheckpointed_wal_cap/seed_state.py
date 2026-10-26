import os,json,sqlite3
from pathlib import Path
root=Path('/var/lib/operations')
root.mkdir(parents=True,exist_ok=True)
(root/'handoff').mkdir(exist_ok=True)
def put(name,value):
    p=root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(value)
p=root/'state'; p.mkdir()
c=sqlite3.connect(p/'orders.sqlite')
c.execute('PRAGMA journal_mode=WAL'); c.execute('PRAGMA wal_autocheckpoint=0')
c.execute('CREATE TABLE orders(id INTEGER PRIMARY KEY,customer TEXT,total_cents INTEGER)')
c.execute('INSERT INTO orders VALUES(?,?,?)', [[4101, 'Cedar Instruments', 32800], [4102, 'Northline Labs', 71900], [4103, 'Harbor Systems', 48250]][0]); c.commit(); c.execute('PRAGMA wal_checkpoint(TRUNCATE)')
c.executemany('INSERT INTO orders VALUES(?,?,?)', [[4101, 'Cedar Instruments', 32800], [4102, 'Northline Labs', 71900], [4103, 'Harbor Systems', 48250]][1:]); c.commit()
result=c.execute('PRAGMA wal_checkpoint(FULL)').fetchone()
assert result[0]==0 and result[1]==result[2] and result[1]>0
assert (p/'orders.sqlite-wal').stat().st_size>32
# Capture the consistent, fully checkpointed files before closing the connection.
main_bytes=(p/'orders.sqlite').read_bytes()
wal_bytes=(p/'orders.sqlite-wal').read_bytes()
c.close()
(p/'orders.sqlite').write_bytes(main_bytes)
(p/'orders.sqlite-wal').write_bytes(wal_bytes)
(p/'checkpoint.json').write_text(json.dumps({'checkpoint':'FULL','busy':result[0],'log_frames':result[1],'checkpointed_frames':result[2],'writer_stopped':True,'orders':[4101,4102,4103]},indent=2))
