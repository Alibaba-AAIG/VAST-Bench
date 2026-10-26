#!/usr/bin/env python3
import os,sys,subprocess,time,urllib.request
from pathlib import Path
command=['python3', 'manage.py', 'runserver']
url='http://127.0.0.1:8000/'
log=Path('/tmp/opsdash-server.log')
log.parent.mkdir(parents=True,exist_ok=True)
with log.open('ab') as out:
    p=subprocess.Popen(command,cwd='/testbed',stdin=subprocess.DEVNULL,stdout=out,stderr=out,start_new_session=True)
Path('/tmp/opsdash-server.pid').write_text(str(p.pid)+'\n')
for _ in range(100):
    if p.poll() is not None: raise SystemExit('Service exited; inspect '+str(log))
    try:
        urllib.request.urlopen(url,timeout=1).read();print('Service ready:',url,'PID',p.pid);break
    except OSError:time.sleep(.1)
else:raise SystemExit('Service did not become ready')
