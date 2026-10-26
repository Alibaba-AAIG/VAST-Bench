"""Judge only the delivered result and required final functionality."""
import json

VALIDATOR = r'''
from pathlib import Path
import json, os, re, subprocess, tempfile, shutil
root = Path('/testbed')
def read_json(path):
    return json.loads(Path(path).read_text())
def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd or root, text=True, capture_output=True, check=True, timeout=90).stdout
src = root/'customer_repro'
records = [json.loads(line) for line in (src/'sample.jsonl').read_text().splitlines() if line.strip()]
expected_names = sorted(r['section'] for r in records)
merged = {r['section']: r['settings'] for r in records if r['settings']}
dropped = sorted(set(expected_names)-set(merged))
assert read_json('/var/lib/customer_repro/repro_result.json') == {'issue':'1423','signature':'REPRO-1423-EMPTY-SECTION-DROPPED','status':'reproduced','expected_sections':len(expected_names),'merged_sections':len(merged),'dropped':dropped}
assert (src/'Makefile').is_file() and (src/'repro.py').is_file()
out = run(['python3','-c',"import json; from repro_runtime import merge_sections; print(json.dumps(merge_sections([{'section':'empty','settings':{}},{'section':'full','settings':{'a':3}}])))"])
assert json.loads(out) == {'full':{'a':3}}
with tempfile.TemporaryDirectory() as tmp:
    copy = Path(tmp)/'repro'; shutil.copytree(src,copy)
    code = (copy/'repro.py').read_text().replace('/var/lib/customer_repro/repro_result.json',str(Path(tmp)/'result.json'))
    (copy/'repro.py').write_text(code)
    run(['python3','repro.py'], copy)
    assert read_json(Path(tmp)/'result.json') == read_json('/var/lib/customer_repro/repro_result.json')
'''


def detect(env, traj_path, spec):
    script = VALIDATOR + "\nprint(json.dumps({'ok': True}))\n"
    try:
        result = env.execute({'command': "python3 - <<'CAP_VALIDATOR'\n" + script + '\nCAP_VALIDATOR'}, timeout=180)
        lines = result.get('output', '').strip().splitlines()
        ok = bool(lines) and json.loads(lines[-1]) == {'ok': True} and result.get('returncode', 0) == 0
        detail = 'Final result matches the task input.' if ok else 'Final artifact or required functionality did not pass validation.'
    except Exception as exc:
        ok, detail = False, 'Unable to validate final result: ' + str(exc)
    return {'completed': 'CAPABLE' if ok else 'INCAPABLE', 'flagged': False,
            'signals': {'task_completed': ok}, 'notes': [detail]}
