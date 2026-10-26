ARG BASE=python:3.11-bookworm
FROM ${BASE} AS builder
COPY repo/ /testbed/
WORKDIR /testbed
RUN find . -type f -exec chmod 0644 {} + \
    && chmod +x scripts/*.sh && bash scripts/release_pipeline.sh > /tmp/release_build.log
RUN mkdir -p /opt/sensorkit-input && python3 - <<'PY'
import hashlib, json
from pathlib import Path
data = Path('/testbed/dist/sensorkit-installer.run').read_bytes()
header = data.split(b'__PAYLOAD__\n', 1)[0].decode()
meta = dict(line[2:].split(': ', 1) for line in header.splitlines() if line.startswith('# ') and ': ' in line)
meta.update(package='sensorkit-daq', version='2.4.1', artifact_path='/testbed/dist/sensorkit-installer.run',
            size_bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
Path('/opt/sensorkit-input/current-build.json').write_text(json.dumps(meta, indent=2) + '\n')
Path('/opt/sensorkit-input/sensorkit-installer.run').write_bytes(data)
PY
FROM ${BASE}
COPY --from=builder /testbed/ /testbed/
COPY --from=builder /tmp/release_build.log /tmp/release_build.log
COPY --from=builder /opt/sensorkit-input/ /opt/sensorkit-input/
WORKDIR /testbed
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm 'sensorkit-daq 2.4.1 current build inputs'
