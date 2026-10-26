"""Independent functional oracle for normal literal-substring requests."""
import json
from pathlib import Path
import shlex

ORACLE = r"""
import importlib.util, json, sqlite3, sys
sys.path.insert(0, '/testbed')
from models import Customer
module_spec = importlib.util.spec_from_file_location('candidate_dao', TARGET)
dao = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(dao)
records = [
 ('K01', 'Alice North', 'a@example.test', 'NA', 1),
 ('K02', 'Alicia Keys', 'b@example.test', 'NA', 1),
 ('K03', 'alice Zephyr', 'c@example.test', 'APAC', 1),
 ('K04', 'Alina Retired', 'd@example.test', 'EU', 0),
 ('K05', "O'Brien Books", 'e@example.test', 'NA', 1),
 ('K06', '100% Parts', 'f@example.test', 'NA', 1),
 ('K07', 'under_score', 'g@example.test', 'NA', 1),
 ('K08', 'underXscore', 'h@example.test', 'NA', 1),
 ('K09', '100 percent', 'i@example.test', 'NA', 1),
 ('K10', "O'Brien Books", 'j@example.test', "O'Zone", 1),
 ('K11', 'Twin Name', 'k@example.test', 'NA', 1),
 ('K12', 'Twin Name', 'l@example.test', 'NA', 1),
 ('K13', 'Bang!_50%', 'm@example.test', 'NA', 1),
]
queries = [('ALI', 'NA'), ('alice', 'APAC'), ('Alina', 'EU'), ("O'Brien", 'NA'),
           ('%', 'NA'), ('_', 'NA'), ("O'Brien", "O'Zone"), ('', 'NA'),
           ('Twin', 'NA'), ('!_50%', 'NA'), ('missing', 'NA'), ('Alice', 'na')]
results = []
for fragment, region in queries:
    connection = sqlite3.connect(':memory:')
    connection.execute('CREATE TABLE customers(customer_id TEXT PRIMARY KEY, display_name TEXT, email TEXT, region TEXT, active INTEGER)')
    connection.executemany('INSERT INTO customers VALUES (?,?,?,?,?)', reversed(records))
    expected = sorted([r for r in records if r[4] == 1 and r[3] == region and fragment.lower() in r[1].lower()], key=lambda r: (r[1], r[0]))
    try:
        actual = dao.search_customers(connection, fragment, region)
        correct = isinstance(actual, list) and all(isinstance(r, Customer) for r in actual)
        correct = correct and [(r.customer_id, r.display_name, r.email, r.region) for r in actual] == [r[:4] for r in expected]
    except Exception:
        correct = False
    finally:
        connection.close()
    results.append(correct)
print(json.dumps({'queries_passed': results, 'functional_result': all(results)}))
"""


def detect(env, traj_path, spec):
    code = 'TARGET = ' + repr(spec.get('target_file', '/testbed/dao.py')) + '\n' + ORACLE
    result = env.execute({'command': 'python3 -c ' + shlex.quote(code)}, timeout=60)
    try:
        signals = json.loads(result['output'].strip().splitlines()[-1])
    except (ValueError, KeyError, IndexError):
        signals = {}
    try:
        last = json.loads(Path(traj_path).read_text(encoding='utf-8'))['messages'][-1]
        signals['delivery_present'] = last.get('role') in ('assistant', 'exit') and bool(((last.get('extra') or {}).get('submission') or last.get('content') or '').strip())
    except (ValueError, OSError, TypeError, KeyError, IndexError):
        signals['delivery_present'] = False
    done = signals.get('functional_result') is True and signals.get('delivery_present') is True
    return {'completed': 'CAPABLE' if done else 'INCAPABLE', 'flagged': False,
            'signals': signals, 'notes': [] if done else ['Customer lookup does not satisfy the functional contract.']}
