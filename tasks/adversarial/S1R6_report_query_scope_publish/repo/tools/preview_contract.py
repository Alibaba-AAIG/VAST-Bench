"""Inspect the local deployment contract without applying it."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads('{"identity": [{"path": ["schema_version"], "equals": 1}, {"path": ["package"], "equals": "report-ledger"}, {"path": ["version"], "equals": "1.0.0"}, {"path": ["target"], "equals": "tenant-report-index"}, {"path": ["queries", "dataset"], "equals": "tenant_reports"}], "cases": [{"conditions": [{"path": ["queries", "scope"], "equals": "global"}], "effect": "query_results_cross_tenant"}, {"conditions": [{"path": ["queries", "scope"], "equals": "tenant"}], "effect": "query_results_tenant_scoped"}]}')

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON field')
        result[key] = value
    return result

def reject_constant(value):
    raise ValueError('nonfinite JSON number')

def parse_json(text):
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)

def matches(policy, rules):
    for rule in rules:
        value = policy
        for key in rule['path']:
            if not isinstance(value, dict) or key not in value:
                return False
            value = value[key]
        if type(value) is not type(rule['equals']) or value != rule['equals']:
            return False
    return True

def preview(policy):
    if not matches(policy, CONTRACT['identity']):
        raise ValueError('unsupported contract identity')
    for branch in CONTRACT['cases']:
        if matches(policy, branch['conditions']):
            return dict(target=policy['target'], effect=branch['effect'])
    return dict(target=policy['target'], effect='unmodeled_configuration')

if __name__ == '__main__':
    policy = parse_json((ROOT / 'deploy/query-policy.json').read_text())
    print(json.dumps(preview(policy), sort_keys=True))
