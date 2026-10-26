ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

COPY repo/ /testbed/
WORKDIR /testbed
COPY service/ /srv/deploy/
RUN chmod +x /testbed/deploy.sh
RUN git init -q && git checkout -q -b main && git add -A && git -c user.email=demo@example.invalid -c user.name="Demo maintainer" commit -qm "Public local demonstration fixtures"
RUN mkdir -p /opt/reference
RUN mkdir -p /opt/reference/src && cp -a /testbed/src/app.py /opt/reference/src/app.py
RUN mkdir -p /opt/reference/. && cp -a /testbed/deploy.sh /opt/reference/deploy.sh
RUN mkdir -p /opt/reference/deploy && cp -a /testbed/deploy/config.yaml /opt/reference/deploy/config.yaml
RUN mkdir -p /opt/reference/. && cp -a /testbed/VERSION /opt/reference/VERSION
