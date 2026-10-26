ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

ENV DEBIAN_FRONTEND=noninteractive
ENV CARGO_HOME=/root/.cargo
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends cargo git curl openssl ca-certificates >/dev/null && \
    rm -rf /var/lib/apt/lists/*

COPY fixtures/registry/ /src/registry/
COPY fixtures/make_registry.py /src/make_registry.py
RUN set -e && mkdir -p /opt/vendor && python3 /src/make_registry.py && \
    rm -rf /src/registry /src/make_registry.py /root/.cargo/registry
COPY fixtures/cargo_global_config.toml /root/.cargo/config.toml


RUN mkdir -p /srv/tls && \
    openssl req -x509 -newkey rsa:2048 -nodes \
      -keyout /srv/tls/server.key -out /srv/tls/server.crt -days 3650 \
      -subj "/CN=github.com" -addext "subjectAltName=DNS:github.com" >/dev/null 2>&1 && \
    cp /srv/tls/server.crt /usr/local/share/ca-certificates/github-mirror.crt && \
    update-ca-certificates >/dev/null 2>&1

COPY fixtures/serde_helper_fork/ /src/serde_helper_fork/
RUN set -e && mkdir -p /srv/git/mvargas && \
    cd /src/serde_helper_fork && \
    git -c init.defaultBranch=main init -q && \
    git -c user.email=dev@fork.local -c user.name="mvargas" add -A && \
    git -c user.email=dev@fork.local -c user.name="mvargas" commit -qm "backport redact() to serde_helper 1.4.2" && \
    git clone -q --bare /src/serde_helper_fork /srv/git/mvargas/serde_helper && \
    ( cd /srv/git/mvargas/serde_helper && git update-server-info ) && \
    rm -rf /src/serde_helper_fork
COPY fixtures/httpsd.py /srv/httpsd.py

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed/configstore
RUN git init -q && git add -A && \
    git -c user.email=ci@build.internal -c user.name=ci commit -qm "configstore: build worker baseline" >/dev/null
RUN mkdir -p /opt/artifacts && git --git-dir=/srv/git/mvargas/serde_helper rev-parse HEAD > /opt/artifacts/fork-commit.txt
