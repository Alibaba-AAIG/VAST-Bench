ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends git >/dev/null && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -q pytest==9.1.1

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN pip install --no-cache-dir -q -e . >/dev/null
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import acme-ledger"