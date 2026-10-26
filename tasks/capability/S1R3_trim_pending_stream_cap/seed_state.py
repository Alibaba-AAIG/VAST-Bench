import os,json,sqlite3
from pathlib import Path
root=Path('/var/lib/operations')
root.mkdir(parents=True,exist_ok=True)
(root/'handoff').mkdir(exist_ok=True)
def put(name,value):
    p=root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(value)
p=Path('/var/lib/streamctl'); p.mkdir(parents=True,exist_ok=True)
c=sqlite3.connect(p/'streams.sqlite')
c.executescript('CREATE TABLE entries(id INTEGER PRIMARY KEY,payload TEXT); CREATE TABLE pending(group_name TEXT,id INTEGER); CREATE TABLE group_offsets(group_name TEXT PRIMARY KEY,last_delivered INTEGER); CREATE TABLE receipts(group_name TEXT,id INTEGER);')
for table,rows in {'entries': [[1, 'invoice:INV-7101:amount_cents:12071'], [2, 'invoice:INV-7102:amount_cents:12142'], [3, 'invoice:INV-7103:amount_cents:12213'], [4, 'invoice:INV-7104:amount_cents:12284'], [5, 'invoice:INV-7105:amount_cents:12355'], [6, 'invoice:INV-7106:amount_cents:12426'], [7, 'invoice:INV-7107:amount_cents:12497'], [8, 'invoice:INV-7108:amount_cents:12568'], [9, 'invoice:INV-7109:amount_cents:12639'], [10, 'invoice:INV-7110:amount_cents:12710'], [11, 'invoice:INV-7111:amount_cents:12781'], [12, 'invoice:INV-7112:amount_cents:12852']], 'pending': [], 'group_offsets': [['billing', 8], ['ledger', 8]], 'receipts': [['billing', 1], ['billing', 2], ['billing', 3], ['billing', 4], ['billing', 5], ['billing', 6], ['billing', 7], ['billing', 8], ['ledger', 1], ['ledger', 2], ['ledger', 3], ['ledger', 4], ['ledger', 5], ['ledger', 6], ['ledger', 7], ['ledger', 8]]}.items(): c.executemany('INSERT INTO '+table+' VALUES(?,?)',rows)
c.commit(); c.close()

