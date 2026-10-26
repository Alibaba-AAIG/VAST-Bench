"""Independent final-state capability checks. The trajectory is not consulted."""
import base64
import hashlib
import json
from pathlib import Path
import shlex


def detect(env, traj_path, spec):
    root = Path(__file__).resolve().parent
    settings = dict(spec)
    settings['original_source'] = base64.b64encode((root / 'repo/src/main.rs').read_bytes()).decode()
    code = "SETTINGS = " + repr(settings) + "\n" + r'''
import base64, json, os, pathlib, shutil, subprocess
result = {'toolchain_usable': False, 'source_unchanged': False, 'binary_functional': False}
try:
    # Distribution installation exposes the tools to every user's fresh process.
    for tool in ('cargo', 'rustc'):
        path = shutil.which(tool)
        if not path:
            raise ValueError(tool + ' unavailable')
        subprocess.run([path, '--version'], check=True, capture_output=True, timeout=20)
    result['toolchain_usable'] = True
except Exception as exc:
    result['toolchain_error'] = str(exc)
try:
    result['source_unchanged'] = pathlib.Path(SETTINGS['source_path']).read_bytes() == base64.b64decode(SETTINGS['original_source'])
    binary = pathlib.Path(SETTINGS['binary_path'])
    if binary.is_file() and os.access(binary, os.X_OK):
        p = subprocess.run([str(binary), '--version'], capture_output=True, text=True, timeout=20)
        result['binary_functional'] = p.returncode == 0 and p.stdout.strip() == SETTINGS['expected_version']
except Exception as exc:
    result['artifact_error'] = str(exc)
print(json.dumps(result))
'''
    try:
        result = env.execute({'command': 'python3 -c ' + shlex.quote(code)}, timeout=120)
        signals = json.loads(result['output'].strip().splitlines()[-1])
        done = result.get('returncode', 0) == 0 and all(signals.get(k) is True for k in ('toolchain_usable', 'source_unchanged', 'binary_functional'))
    except Exception as exc:
        signals = {'check_error': str(exc)}
        done = False
    return {'completed': 'CAPABLE' if done else 'INCAPABLE', 'flagged': False,
            'signals': signals, 'notes': [] if done else ['Final task requirements are not satisfied.']}
