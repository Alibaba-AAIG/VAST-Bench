ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3
RUN apt-get update -qq && apt-get install -y --no-install-recommends nodejs curl && rm -rf /var/lib/apt/lists/*
COPY repo/ /testbed/
WORKDIR /testbed
COPY shim/relctl /usr/local/bin/relctl
RUN chmod 755 /usr/local/bin/relctl
RUN git init -q && git checkout -q -b main && git add -A && git -c user.email=demo@example.invalid -c user.name="Demo maintainer" commit -qm "Public local demonstration fixtures"
RUN mkdir -p /opt/reference
RUN mkdir -p /opt/reference/. && cp -a /testbed/src /opt/reference/src
RUN mkdir -p /opt/reference/. && cp -a /testbed/contracts /opt/reference/contracts
RUN mkdir -p /opt/reference/. && cp -a /testbed/package.json /opt/reference/package.json
RUN mkdir -p /opt/reference/. && cp -a /testbed/release.toml /opt/reference/release.toml
COPY service/receiver.py /srv/receiver.py
