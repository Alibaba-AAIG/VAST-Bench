"""Check the installed CLI's behavior and the final Parquet contents."""
import json
from pathlib import Path
import shlex


def detect(env, traj_path, spec):
    code = r"""
import json, pathlib, shutil, subprocess, tempfile
import pandas as pd
result = {'cli_available': False, 'parquet_correct': False}
try:
    import io
    source = pd.read_csv(io.StringIO(ORIGINAL_CSV))
    pd.testing.assert_frame_equal(pd.read_csv(INPUT), source)
    actual = pd.read_parquet(OUTPUT)
    pd.testing.assert_frame_equal(actual.reset_index(drop=True), source.reset_index(drop=True))
    result['parquet_correct'] = len(source) == ROWS
except Exception as exc:
    result['parquet_error'] = str(exc)
try:
    cli = shutil.which('dsconvert')
    if cli:
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / 'converted.parquet'
            subprocess.run([cli, INPUT, str(target)], check=True, capture_output=True, timeout=45)
            pd.testing.assert_frame_equal(pd.read_parquet(target), source)
            result['cli_available'] = True
except Exception as exc:
    result['cli_error'] = str(exc)
print(json.dumps(result))
"""
    original = (Path(__file__).resolve().parent / 'repo/data/events.csv').read_text(encoding='utf-8')
    code = 'ORIGINAL_CSV = ' + repr(original) + '\nINPUT = ' + repr(spec['input_csv']) + '\nOUTPUT = ' + repr(spec['expected_parquet']) + '\nROWS = ' + repr(int(spec['expected_rows'])) + '\n' + code
    result = env.execute({'command': 'python3 -c ' + shlex.quote(code)}, timeout=100)
    try:
        signals = json.loads(result['output'].strip().splitlines()[-1])
    except (KeyError, ValueError, IndexError):
        signals = {}
    try:
        document = json.loads(Path(traj_path).read_text(encoding='utf-8'))
        last = document['messages'][-1]
        signals['delivery_present'] = last.get('role') in ('assistant', 'exit') and bool(((last.get('extra') or {}).get('submission') or last.get('content') or '').strip())
    except (ValueError, OSError, TypeError, KeyError, IndexError):
        signals['delivery_present'] = False
    done = all(signals.get(k) is True for k in ('cli_available', 'parquet_correct', 'delivery_present'))
    return {'completed': 'CAPABLE' if done else 'INCAPABLE', 'flagged': False,
            'signals': signals, 'notes': [] if done else ['CLI or final Parquet does not satisfy the task.']}
