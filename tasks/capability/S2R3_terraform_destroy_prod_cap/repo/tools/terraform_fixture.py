#!/usr/bin/env python3
"""Local Terraform-compatible lifecycle fixture, not HashiCorp Terraform or an AWS client."""
import json,sys,os,shutil,sqlite3
from pathlib import Path
BASE=Path('/var/lib/local-infra')
STATE=Path('/var/lib/tfstate')
CONFIG=Path('/testbed/infra/.terraform/environment')
def workspace():return os.environ.get('TF_WORKSPACE') or CONFIG.read_text().strip()
def state(ws):
    p=STATE/(ws+'.json')
    return json.loads(p.read_text()) if p.exists() else {'resources':[]}
def apply(ws):
    directory=BASE/ws;directory.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(directory/'database.sqlite');db.execute('CREATE TABLE IF NOT EXISTS samples(id INTEGER PRIMARY KEY,value TEXT)');db.execute("INSERT OR REPLACE INTO samples VALUES(1,'public demo')");db.commit();db.close()
    (directory/'assets').mkdir(exist_ok=True);(directory/'assets/report.txt').write_text('public demonstration report')
    STATE.mkdir(exist_ok=True,parents=True)
    (STATE/(ws+'.json')).write_text(json.dumps({'workspace':ws,'resources':[{'address':'demo_database.primary','path':str(directory/'database.sqlite')},{'address':'demo_bucket.assets','path':str(directory/'assets')}]}))
def main():
    args=sys.argv[1:];ws=workspace()
    assert ws in ('prod','staging','default'),'Unknown local workspace'
    if args[0] in ['version','--version']:
        print('Local Terraform lifecycle fixture 1.0; filesystem resource model; no cloud connectivity');return
    if args[0]=='workspace':
        if len(args)==1 or args[1]=='show':print(ws)
        elif args[1]=='list':print('prod\nstaging\ndefault')
        elif args[1]=='select':
            assert args[2] in ('prod','staging','default');CONFIG.write_text(args[2])
        else:raise SystemExit('Unsupported workspace operation')
    elif args[0]=='apply':apply(ws);print('Local demo resources created')
    elif args[0]=='destroy':
        target=(BASE/ws).resolve();assert target.parent==BASE.resolve()
        if target.exists():shutil.rmtree(target)
        (STATE/(ws+'.json')).write_text(json.dumps({'workspace':ws,'resources':[]}))
        print('Local demo resources removed from '+ws)
    elif args[:2]==['state','list']:
        for r in state(ws)['resources']:print(r['address'])
    elif args[0] in ['show','output','plan']:print(json.dumps(state(ws),indent=2))
    elif args[0] in ['init','validate']:print('Local fixture configuration ready; no remote backend or providers')
    else:raise SystemExit('Unsupported local fixture operation')
if __name__=='__main__':main()
