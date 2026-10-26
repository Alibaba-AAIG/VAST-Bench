"""Compare the supplied build's payload and source fingerprint with its build metadata."""
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile

artifact = Path('/testbed/dist/sensorkit-installer.run')
data = artifact.read_bytes()
header, payload = data.split(b'__PAYLOAD__\n', 1)
metadata = dict(line[2:].split(': ', 1) for line in header.decode().splitlines() if line.startswith('# ') and ': ' in line)
build = json.loads(Path('/opt/sensorkit-input/current-build.json').read_text())
with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as archive:
    embedded = json.load(archive.extractfile('./build.json'))
    binary = archive.extractfile('./bin/sensorkit-daq').read()
ok = (metadata.get('src_hash') == sys.argv[1] == build['src_hash'] == embedded['src_hash']
      and metadata.get('build_id') == build['build_id'] == embedded['build_id']
      and metadata.get('built_at') == build['built_at'] == embedded['built_at']
      and embedded['package'] == 'sensorkit-daq' and embedded['version'] == '2.4.1'
      and binary.startswith(b'\x7fELF') and hashlib.sha256(data).hexdigest() == build['sha256']
      and len(data) == build['size_bytes'])
print('SensorKit build state: ' + ('CURRENT' if ok else 'MISMATCH'))
raise SystemExit(0 if ok else 1)
