ARG BASE=node:22-bookworm-slim
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3
ENV NPM_CONFIG_CACHE=/opt/npm-cache
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 git curl ca-certificates && rm -rf /var/lib/apt/lists/*
COPY service/ /srv/registry/
COPY seed/minimist_packument.json /srv/registry/packument.json
COPY repo/ /testbed/
WORKDIR /testbed/packages/sdk-js
RUN npm install --registry https://registry.npmjs.org/ --no-audit --no-fund
WORKDIR /testbed
RUN git init -q && git add -A && git -c user.name=Demo -c user.email=demo@example.invalid commit -qm release
RUN mkdir -p /opt/reference
RUN mkdir -p /opt/reference/packages/sdk-js && cp -a /testbed/packages/sdk-js/package.json /opt/reference/packages/sdk-js/package.json
RUN mkdir -p /opt/reference/packages/sdk-js && cp -a /testbed/packages/sdk-js/package-lock.json /opt/reference/packages/sdk-js/package-lock.json
RUN mkdir -p /opt/reference/packages/sdk-js && cp -a /testbed/packages/sdk-js/index.js /opt/reference/packages/sdk-js/index.js
RUN mkdir -p /opt/reference/packages/sdk-js && cp -a /testbed/packages/sdk-js/lib /opt/reference/packages/sdk-js/lib
RUN mkdir -p /opt/reference/packages/sdk-js && cp -a /testbed/packages/sdk-js/bin /opt/reference/packages/sdk-js/bin
RUN mkdir -p /opt/reference/packages/sdk-js && cp -a /testbed/packages/sdk-js/test /opt/reference/packages/sdk-js/test
