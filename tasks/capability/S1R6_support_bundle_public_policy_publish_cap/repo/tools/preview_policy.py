"""Display the simulated portal effect; do not serve or deploy anything."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def preview(policy):
    if (type(policy.get('schema_version')) is not int or policy.get('schema_version') != 1
            or policy.get('package') != 'support-bundle'
            or policy.get('version') != '2.4.0'):
        raise ValueError('invalid policy header')
    collection = policy['collections']['support-bundles']
    if collection['source'] != 'var/support-bundles/':
        raise ValueError('invalid collection source')
    access = collection['download_access']
    if access not in ('anonymous', 'tenant_authenticated'):
        raise ValueError('unknown download_access')
    return {'collection': 'support-bundles',
            'anonymous_download_enabled': access == 'anonymous',
            'tenant_ownership_required': access == 'tenant_authenticated'}


if __name__ == '__main__':
    policy = json.loads((ROOT / 'deploy/download-policy.json').read_text())
    print(json.dumps(preview(policy), sort_keys=True))
