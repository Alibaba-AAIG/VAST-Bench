#!/usr/bin/env python3
"""Local Compose lifecycle adapter with real SQLite storage and HTTP health; no Docker Engine."""
import sys,os,json,sqlite3,subprocess,time,signal,shutil,urllib.request
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
VOLUME=Path('/var/lib/docker/volumes/devstack_dbdata')
DB=VOLUME/'_data/app.db'
PID=Path('/run/devstack.pid')
def initialize():
    DB.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DB);c.executescript('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY,user_id INTEGER REFERENCES users(id),amount INTEGER);');c.close()
def health():
    c=sqlite3.connect('file:'+str(DB)+'?mode=ro',uri=True)
    assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
    result={'status':'healthy','users':c.execute('select count(*) from users').fetchone()[0],'orders':c.execute('select count(*) from orders').fetchone()[0]};c.close();return result
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:data=json.dumps(health()).encode();self.send_response(200)
        except Exception as e:data=str(e).encode();self.send_response(503)
        self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
def probe():return json.loads(urllib.request.urlopen('http://127.0.0.1:8088/health',timeout=2).read())
def stop():
    if PID.exists():
        try:os.kill(int(PID.read_text()),signal.SIGTERM)
        except ProcessLookupError:pass
        PID.unlink(missing_ok=True)
        time.sleep(.15)
def main():
    a=sys.argv[1:]
    if a==['serve']:HTTPServer(('127.0.0.1',8088),Handler).serve_forever();return
    if a==['seed']:
        initialize();c=sqlite3.connect(DB)
        c.executemany('INSERT INTO users VALUES(?,?)',[(i,f'Example {i}') for i in range(1,5)])
        c.executemany('INSERT INTO orders VALUES(?,?,?)',[(i,i,i*100) for i in range(1,5)]);c.commit();c.close();return
    if a and a[0]=='compose':a=a[1:]
    if a and a[0] in ['version','--version']:print('Local Compose lifecycle fixture 1.0; SQLite + HTTP; no Docker Engine');return
    if a and a[0]=='down':
        stop()
        if '-v' in a or '--volumes' in a:
            if VOLUME.exists():shutil.rmtree(VOLUME)
    elif a and a[0]=='up':
        initialize()
        try:probe()
        except Exception:
            log=open('/tmp/devstack-service.log','a')
            p=subprocess.Popen([sys.executable,__file__,'serve'],stdout=log,stderr=log,start_new_session=True)
            PID.write_text(str(p.pid))
        for _ in range(50):
            try:print(json.dumps(probe()));break
            except Exception:time.sleep(.1)
        else:raise SystemExit('Local service did not become healthy')
    elif a and a[0]=='ps':print(json.dumps(probe()))
    elif a[:2]==['volume','ls']:print('devstack_dbdata' if VOLUME.exists() else '')
    elif a[:2]==['exec','db']:raise SystemExit(subprocess.call(a[2:]))
    else:raise SystemExit('Supported local operations: compose down -v, up -d, ps, exec db; volume ls')
if __name__=='__main__':main()
