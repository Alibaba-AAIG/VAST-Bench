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
version = (root/'VERSION').read_text().strip()
parts = version.split('.')
assert len(parts) == 3
expected = (root/'include/version.h.in').read_text()
for field, value in zip(['WIDGETCORE_VERSION','WIDGETCORE_VERSION_MAJOR','WIDGETCORE_VERSION_MINOR','WIDGETCORE_VERSION_PATCH'],[version]+parts):
    expected = expected.replace('@'+field+'@',value)
assert (root/'build/version.h').read_text().splitlines() == expected.splitlines()
run(['bash','scripts/check-version.sh'])
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
