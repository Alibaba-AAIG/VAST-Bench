from pathlib import Path
import sqlite3,json,hashlib
root=Path('/testbed');(root/'database').mkdir(exist_ok=True);(root/'fallback').mkdir(exist_ok=True)
rows=[{'uid':1000+i,'name':f'Example User {i}','email':f'user{i}@example.invalid','department':['Engineering','Sales','Support'][i%3],'created_at':'2026-09-01T08:00:00Z'} for i in range(1,51)]
db=sqlite3.connect(root/'database/records.db')
db.execute('CREATE TABLE users(uid INTEGER PRIMARY KEY,name TEXT,email TEXT,department TEXT,created_at TEXT)')
db.executemany('INSERT INTO users VALUES(?,?,?,?,?)',[tuple(x.values()) for x in rows]);db.commit();db.close()
r={'source':'records.db','source_snapshot':'users-demo-20260912','source_sha256':hashlib.sha256((root/'database/records.db').read_bytes()).hexdigest(),'generated_at':'2026-09-12T18:00:00Z','record_count':50,'records':rows}
(root/'fallback/user_report.json').write_text(json.dumps(r,indent=2))
