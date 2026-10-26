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
assert (p/'orders.sqlite-wal').stat().st_size>32
# Abrupt process exit retains a valid committed WAL with no surviving writer.
os._exit(0)

