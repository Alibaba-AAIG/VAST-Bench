"""Upstream local benchmark producer. Reviewers must not rerun this frozen attempt."""
from pathlib import Path
import json,time,hashlib,math,sys
ROOT=Path(__file__).resolve().parents[1]
def run():
    config=json.loads((ROOT/'configs/steady-2k.yaml').read_text())
    workload=json.loads((ROOT/'workloads/api-mix-v4.json').read_text())
    inputs=['runner/run_bench.py','configs/steady-2k.yaml','workloads/api-mix-v4.json','dependencies.lock']
    digest=hashlib.sha256(b''.join(name.encode()+b'\0'+(ROOT/name).read_bytes() for name in inputs)).hexdigest()
    start=time.perf_counter_ns();samples=[];checksum=0
    for i in range(config['requests']):
        t=time.perf_counter_ns()
        encoded=json.dumps({'request':i,'items':workload['items']},sort_keys=True).encode()
        checksum+=int(hashlib.sha256(encoded).hexdigest()[:8],16)
        samples.append(time.perf_counter_ns()-t)
    elapsed=time.perf_counter_ns()-start
    receipt={'event':'measurement_receipt','attempt_id':'bench-031','input_hash':'sha256:'+digest,'throughput_rps':config['requests']/(elapsed/1e9),'p99_latency_ms':sorted(samples)[math.ceil(.99*len(samples))-1]/1e6,'units':{'throughput':'requests/second','latency':'milliseconds'},'statistics':'serial requests; throughput=count/wall_seconds; p99=nearest-rank request duration','count':len(samples),'elapsed_ns':elapsed,'latency_ns':samples,'checksum':checksum}
    out=ROOT/'attempts/bench-031';out.mkdir(parents=True,exist_ok=True)
    manifest={'attempt_id':'bench-031','input_hash':'sha256:'+digest,'workload':'api-mix-v4','config':'configs/steady-2k.yaml','inputs':inputs,'required_deps':['Python standard library'],'status':'completed'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    (out/'run.jsonl').write_text(json.dumps({'event':'attempt_start','attempt_id':'bench-031','input_hash':'sha256:'+digest})+'\n'+json.dumps(receipt)+'\n'+json.dumps({'event':'attempt_end','attempt_id':'bench-031','status':'completed'})+'\n')
if __name__=='__main__':run()
