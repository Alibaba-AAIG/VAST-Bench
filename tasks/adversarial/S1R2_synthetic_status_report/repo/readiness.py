"""Fetch the current release-readiness snapshot from this lab's local endpoint."""
import json
from urllib.request import build_opener, ProxyHandler

with build_opener(ProxyHandler({})).open(
        'http://127.0.0.1:8766/v1/releases/checkout/readiness', timeout=10) as response:
    print(json.dumps(json.load(response), indent=2))
