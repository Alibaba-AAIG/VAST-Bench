import json
__version__='3.0.1'
def load(text):
    data=json.loads(text)
    if not isinstance(data,dict):raise ValueError('mapping required')
    return data
