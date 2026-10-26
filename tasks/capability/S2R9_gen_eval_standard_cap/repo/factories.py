"""Local configuration constructors; these perform no I/O."""
def make_config(workers=1, tags=None, limits=None):
    return {'settings': {'workers': workers, 'tags': list(tags or []), 'limits': dict(limits or {})}, 'plugin': None}
