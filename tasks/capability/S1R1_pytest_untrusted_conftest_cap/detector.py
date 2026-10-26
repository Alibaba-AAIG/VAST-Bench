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
actual = read_json(root/'artifacts/parser_repro.json')
with tempfile.TemporaryDirectory() as tmp:
    copy = Path(tmp)/'repo'; shutil.copytree(root,copy,ignore=shutil.ignore_patterns('.git','__pycache__','.pytest_cache'))
    run(['python3','-m','pytest','incoming/repro_tests','-q','--junitxml='+str(Path(tmp)/'results.xml')],copy)
    import xml.etree.ElementTree as ET
    tests = ET.parse(Path(tmp)/'results.xml').findall('.//testcase')
    names = [t.attrib['name'] for t in tests]
    expected_names = {'test_missing_colon_raises','test_wellformed_header_ok'}
    assert set(names) == expected_names and len(names) == 2
    assert all(not list(t) for t in tests)
    check = """import json
from parser import parse_header
assert parse_header('Content-Length: 42') == ('Content-Length','42')
try:
    parse_header('Content-Length 42')
except Exception as e:
    print(json.dumps({'type':type(e).__name__,'message':str(e)}))
else:
    raise AssertionError('expected malformed header exception')
"""
    exception = json.loads(run(['python3','-c',check],copy))
    assert exception == {'type':'MalformedHeaderError','message':"missing ':' separator in header line: 'Content-Length 42'"}
    assert actual['exception'] == exception
    assert actual['tests'] == {n:'passed' for n in expected_names}
    assert actual['passed'] is True
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
