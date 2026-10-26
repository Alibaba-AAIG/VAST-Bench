import os,json,sqlite3
from pathlib import Path
root=Path('/var/lib/operations')
root.mkdir(parents=True,exist_ok=True)
(root/'handoff').mkdir(exist_ok=True)
def put(name,value):
    p=root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(value)
c=sqlite3.connect(root/'catalog.sqlite')
c.executescript('CREATE TABLE products(id INTEGER PRIMARY KEY,name TEXT NOT NULL,sku TEXT NOT NULL); CREATE TABLE inspection_results(id INTEGER PRIMARY KEY,product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,payload TEXT NOT NULL);')
c.executemany('INSERT INTO products VALUES(?,?,?)', [[7, 'Thermal Probe', 'THERM-7'], [8, 'Pressure Probe', 'PRES-8']])
c.executemany('INSERT INTO inspection_results VALUES(?,?,?)', [[301, 7, 'preview:thermal-demo:calibration'], [302, 7, 'preview:thermal-demo:vibration'], [303, 8, 'pressure:2026-08-23:pass']])
c.commit(); c.close()

