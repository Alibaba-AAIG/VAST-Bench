
ARG BASE=golang:1.22
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends python3-pip git >/dev/null && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --no-cache-dir --break-system-packages --disable-pip-version-check \
      litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
      platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3 >/dev/null

ENV GOTOOLCHAIN=local GOFLAGS=-mod=mod GOPROXY=off GOSUMDB=off

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed/apiclient
RUN gofmt -w . && \
    go build -o /tmp/_genstub ./internal/genstub && \
    go build -o /tmp/_preflight ./internal/preflight && \
    rm -f /tmp/_genstub /tmp/_preflight && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.com -c user.name=ci add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import apiclient project"
