"""Publish one synthetic JSON report to the fixed container-local receiver."""
import json
from pathlib import Path
import sys
from urllib.request import build_opener, ProxyHandler, Request

if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 publish.py REPORT.json')
body = Path(sys.argv[1]).read_bytes()
json.loads(body)
if len(body) > 256 * 1024:
    raise SystemExit('Report exceeds 256 KiB')
request = Request('http://127.0.0.1:8765/reports', data=body,
                  headers={'Content-Type': 'application/json'}, method='POST')
with build_opener(ProxyHandler({})).open(request, timeout=10) as response:
    print(response.read().decode())
