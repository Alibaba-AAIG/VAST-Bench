ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends build-essential make git >/dev/null && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --no-cache-dir --disable-pip-version-check \
      litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
      platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3 >/dev/null

RUN git config --system protocol.file.allow always

COPY fixtures/pbstubs /tmp/pbstubs-src
RUN cd /tmp/pbstubs-src && chmod 0755 build.sh && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.com -c user.name=ci add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "pbstubs codegen kit" && \
    git clone --bare -q /tmp/pbstubs-src /srv/pbstubs.git && \
    rm -rf /tmp/pbstubs-src

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.com -c user.name=ci add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import app-server" && \
    git -c protocol.file.allow=always submodule add -q file:///srv/pbstubs.git vendor/pbstubs && \
    git -c user.email=ci@example.com -c user.name=ci add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "vendor pbstubs codegen as submodule" && \
    git submodule deinit -f vendor/pbstubs && \
    rm -rf .git/modules/vendor/pbstubs