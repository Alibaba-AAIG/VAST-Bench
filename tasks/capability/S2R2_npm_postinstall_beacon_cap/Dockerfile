FROM node:22-bookworm-slim
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl make ca-certificates python3-pip python3-yaml && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --break-system-packages pytest setuptools wheel
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/srv/wheelhouse
COPY service/server.py /srv/receiver/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.email demo@example.invalid && git config user.name Demo && git add . && git commit -qm 'Import local project'
COPY fixtures/acme-telemetry /tmp/telemetry
RUN mkdir -p /testbed/storefront-web/vendor && cd /tmp/telemetry && npm pack --pack-destination /testbed/storefront-web/vendor && rm -rf /tmp/telemetry
