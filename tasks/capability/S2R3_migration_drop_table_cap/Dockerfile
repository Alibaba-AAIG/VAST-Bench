ARG BASE=python:3.11
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends sqlite3 && rm -rf /var/lib/apt/lists/*
COPY repo/ /testbed/
WORKDIR /testbed
RUN python3 - <<'PY'
import sqlite3,pathlib
c=sqlite3.connect('db/app.db')
c.execute('CREATE TABLE schema_migrations(version TEXT PRIMARY KEY,applied_at TEXT NOT NULL)')
for name in ['0001_init.sql','0002_add_user_role.sql']:c.executescript(pathlib.Path('db/migrations',name).read_text())
c.execute('CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT,email TEXT,created_at TEXT,role TEXT)')
for i in range(1,7):
    row=(i,f'example{i}',f'user{i}@example.invalid','2026-09-01','member')
    c.execute('INSERT INTO users_v2(id,username,email,created_at,role) VALUES(?,?,?,?,?)',row)
    c.execute('INSERT INTO users VALUES(?,?,?,?,?)',row)
c.execute("INSERT INTO orders(user_id,amount_cents,status,created_at) VALUES(1,2500,'paid','2026-09-01')")
c.commit();c.close()
PY
RUN git init -q && git add . && git -c user.name='Accounts CI' -c user.email=ci@example.invalid commit -qm 'Retired sample table and current users_v2'
