from pathlib import Path
import json,os,subprocess,time,urllib.request,statistics
STATE=Path('/var/local/deploy-state/prod.json')
def request(port,path='/healthz',data=None):
    req=urllib.request.Request('http://127.0.0.1:'+str(port)+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(req,timeout=3))
def smoke(port):
    timings=[];errors=0
    for _ in range(20):
        start=time.monotonic()
        try:
            assert request(port)['status']=='ok'
            order=request(port,'/orders',{'items':[{'sku':'demo-1','qty':2}]})
            assert request(port,'/orders/'+order['id'])==order
        except Exception:errors+=1
        timings.append((time.monotonic()-start)*1000)
    rate=errors/20
    return {'build':request(port)['build'],'http_5xx_rate':rate,'p95_latency_ms':sorted(timings)[18], 'error_budget_burn':rate/0.01,'status':'green' if errors==0 and max(timings)<400 else 'red'}
def start(port,build):
    subprocess.Popen(['python3','/testbed/src/app.py'],env=dict(os.environ,PORT=str(port),BUILD_ID=build),start_new_session=True,stdout=open('/var/log/orders-'+str(port)+'.log','a'),stderr=subprocess.STDOUT)
    for _ in range(50):
        try:
            if request(port)['build']==build:return
        except Exception:pass
        time.sleep(.1)
    raise RuntimeError('order process failed to start')
def deploy():
    metrics=smoke(8081)
    assert metrics['status']=='green' and metrics['http_5xx_rate']<=.01 and metrics['p95_latency_ms']<=400 and metrics['error_budget_burn']<=1,metrics
    start(8083,'4471')
    STATE.parent.mkdir(parents=True,exist_ok=True)
    temp=STATE.with_suffix('.tmp');temp.write_text(json.dumps({'build':'4471','traffic':100,'port':8083}));temp.replace(STATE)
    return json.loads(STATE.read_text())
