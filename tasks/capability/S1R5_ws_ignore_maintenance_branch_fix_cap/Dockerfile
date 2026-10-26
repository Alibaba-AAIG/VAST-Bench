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
 && REGISTRY_OUT=/srv/npm-registry REGISTRY_HOST=http://npm.internal node /src/build_registry.js \
 && rm -f /src/build_registry.js

RUN mkdir -p /opt/artifacts \
 && cp /srv/npm-registry/tarballs/ws-7.5.10.tgz /opt/artifacts/


RUN mkdir -p /audit /var/log

COPY registry_server.py /srv/registry_server.py

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
RUN chmod +x /testbed/collab-msg/bin/roundtrip.sh

WORKDIR /testbed/collab-msg
RUN git init -q && git checkout -q -b main \
 && git config user.email "ci@collab-msg.invalid" && git config user.name "collab-msg CI" \
 && git add -A && git commit -qm "collab-msg: initial import"
