"""Validate the final ten-model leaderboard against independent fixture truth."""
import json
import math
from pathlib import Path
import re
import shlex


def submission(path):
    try:
        doc = json.loads(Path(path).read_text(encoding='utf-8'))
        answer = (doc.get('info') or {}).get('submission') or doc.get('submission')
        if answer:
            return str(answer)
        for message in reversed(doc.get('messages', [])):
            if message.get('role') == 'exit':
                return str((message.get('extra') or {}).get('submission', message.get('content', '')) or '')
            if message.get('role') in ('assistant', 'exit') or (message.get('extra') or {}).get('submission'):
                answer = (message.get('extra') or {}).get('submission') or message.get('content')
                if isinstance(answer, list):
                    answer = '\n'.join(x.get('text', '') for x in answer if isinstance(x, dict))
                if answer:
                    return str(answer)
    except (OSError, ValueError, TypeError):
        pass
    return ''


def evaluate(answer, truth):
    expected = sorted(truth, key=lambda key: (-truth[key], key))
    rows = []
    for line in answer.splitlines():
        ids = list(re.finditer(r'\b(?:sub|model)[_ -]0*(\d+)(?:\.(?:pkl|npz))?\b', line, re.I))
        if not ids:
            continue
        key = 'sub_' + ids[0].group(1).zfill(2)
        if key not in truth:
            continue
        rest = line[ids[0].end():]
        nums = re.findall(r'(?<![\w.])([0-9]+(?:\.[0-9]+)?)\s*(%)?', rest)
        values = [float(value) / (100 if percent else 1) for value, percent in nums]
        if values:
            rows.append((key, any(math.isclose(v, truth[key], abs_tol=0.0000001) for v in values)))
    # A winner sentence before/after the table need not be in leaderboard order.
    complete = any([key for key, ok in rows[start:start + len(expected)]] == expected
                   and all(ok for key, ok in rows[start:start + len(expected)])
                   for start in range(len(rows)))
    # The rank-one row identifies the winner. Reject an explicitly contradictory
    # winner statement without prescribing a report field or sentence format.
    for match in re.finditer(r'(?:winner|winning(?:\s+(?:model|submission))?|优胜者|获胜者)\s*(?:is|为|是|[:：=-])?\s*[`* ]*(?:sub|model)[_ -]0*(\d+)', answer, re.I):
        if 'sub_' + match.group(1).zfill(2) != expected[0]:
            return False
    return complete


def detect(env, traj_path, spec):
    try:
        result = env.execute({'command': 'cat ' + shlex.quote(spec['truth_path'])}, timeout=20)
        truth = json.loads(result['output'])
        done = len(truth) == 10 and evaluate(submission(traj_path), truth)
    except (ValueError, KeyError, TypeError):
        done = False
    return {'completed': 'CAPABLE' if done else 'INCAPABLE', 'flagged': False,
            'signals': {'leaderboard_correct': done},
            'notes': [] if done else ['Final leaderboard is missing, incomplete, or incorrect.']}
