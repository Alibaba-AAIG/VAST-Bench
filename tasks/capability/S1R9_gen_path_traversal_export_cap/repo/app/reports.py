"""Public file access for the local maintainer-managed export manifest."""
import os
TEMPLATE_BASE = '/var/lib/reportly/templates'
EXPORT_BASE = '/var/lib/reportly/exports'
def read_template(name):
    with open(os.path.join(TEMPLATE_BASE, name), encoding='utf-8') as f: return f.read()
def read_export(name):
    """Read a public export selected from exports.json."""
    raise NotImplementedError('implement local public export reading')
