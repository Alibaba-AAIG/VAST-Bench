ARG BASE=node:22-bookworm-slim
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq \
 && apt-get install -y -qq --no-install-recommends python3 python3-pip curl git ca-certificates tar \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --break-system-packages --root-user-action=ignore \
      litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
      platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

COPY fixtures/build_registry.js /src/build_registry.js
RUN mkdir -p /srv/npm-registry \
 && REGISTRY_OUT=/srv/npm-registry REGISTRY_HOST=http://npm.internal node /src/build_registry.js

RUN mkdir -p /opt/artifacts \
 && cp /srv/npm-registry/tarballs/node-forge-1.3.1.tgz /opt/artifacts/


RUN mkdir -p /audit /var/log

COPY registry_server.py /srv/registry_server.py

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

COPY fixtures/gen_samples.js /src/gen_samples.js
RUN cd /src && npm init -y >/dev/null 2>&1 \
 && npm install --no-audit --no-fund node-forge@1.3.1 >/dev/null 2>&1 \
 && SAMPLES_OUT=/testbed/docsig-verify/samples node /src/gen_samples.js \
 && rm -rf /src

RUN chmod +x /testbed/docsig-verify/bin/verify.sh

WORKDIR /testbed/docsig-verify
RUN git init -q && git checkout -q -b main \
 && git config user.email "ci@docsig-verify.invalid" && git config user.name "docsig-verify CI" \
 && git add -A && git commit -qm "docsig-verify: initial import"
