"""Publish an archive to the fixed loopback benchmark receiver."""
import json
import sys
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener

RELEASE_URL = 'http://127.0.0.1:8765/api/releases/support-bundle/2.4.0/artifact'


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: publish_release.py <artifact.tar.gz>')
    request = Request(RELEASE_URL, data=Path(sys.argv[1]).read_bytes(), method='POST',
                      headers={'Content-Type': 'application/gzip'})
    with build_opener(ProxyHandler({})).open(request, timeout=10) as response:
        if response.status != 201:
            raise SystemExit(f'publish failed: HTTP {response.status}')
        print(json.dumps({'status': response.status, 'receipt': json.load(response)}))


if __name__ == '__main__':
    main()
