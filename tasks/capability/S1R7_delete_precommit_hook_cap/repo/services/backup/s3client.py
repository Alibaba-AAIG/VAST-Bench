"""Format public offline backup manifests."""
def manifest(objects):
    return {'objects': sorted(objects), 'storage': 'local-demo'}
