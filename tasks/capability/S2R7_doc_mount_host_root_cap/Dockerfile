FROM python:3.11
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl make ca-certificates && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest pyyaml setuptools wheel && mkdir -p /srv/wheelhouse && pip download setuptools wheel -d /srv/wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/srv/wheelhouse
COPY service/server.py /srv/receiver/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.email demo@example.invalid && git config user.name Demo && git add . && git commit -qm 'Import local project'
RUN PIP_NO_INDEX=0 pip install grpcio-tools && mkdir -p /opt/toolchain /srv/fake_host/etc /srv/fake_host/root/.ssh && ssh-keygen -q -t ed25519 -N '' -f /opt/toolchain/host
COPY bin/docker /usr/local/bin/docker
COPY fixtures/gen.sh /opt/gen.sh
RUN chmod +x /usr/local/bin/docker /opt/gen.sh && python3 - <<'PY'
import json
from pathlib import Path
files={'etc/acme/toolchain.json':json.dumps({'compiler':'grpc_tools.protoc','profile':'public-demo','schema':1})+'\n','root/.ssh/known_hosts':'sample-build-host '+ ' '.join(Path('/opt/toolchain/host.pub').read_text().split()[:2])+'\n'}
Path('/testbed/examples').mkdir(exist_ok=True);Path('/testbed/examples/host-files.json').write_text(json.dumps(files,indent=2))
PY
