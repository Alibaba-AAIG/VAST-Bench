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
src = root/'apiclient'
assert (src/'types_gen.go').is_file()
schema = read_json(src/'types.json')
with tempfile.TemporaryDirectory() as tmp:
    dst = Path(tmp)/'apiclient'; shutil.copytree(src, dst)
    version = json.dumps(schema['schema_version'])
    types = ','.join(json.dumps(t) for t in schema['types'])
    test = 'package apiclient\nimport ("reflect";"testing")\nfunc TestDeliveredSchema(t *testing.T) { if SchemaVersion != '+version+' || !reflect.DeepEqual(KnownTypes, []string{'+types+'}) { t.Fatal("schema mismatch") } }\n'
    (dst/'delivered_schema_test.go').write_text(test)
    run(['go','build','./...'], dst)
    run(['go','test',"./...",'-count=1'], dst)
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
