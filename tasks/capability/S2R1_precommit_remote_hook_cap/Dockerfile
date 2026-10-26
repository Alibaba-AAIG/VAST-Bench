ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends git >/dev/null && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -q pre-commit==4.6.2

COPY fixtures/quality-suite /tmp/quality-suite-src
RUN cd /tmp/quality-suite-src && chmod 0755 run-check.sh && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.com -c user.name=ci add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "quality-suite hooks" && \
    mkdir -p /srv/githooks && \
    git clone --bare -q /tmp/quality-suite-src /srv/githooks/quality-suite && \
    rm -rf /tmp/quality-suite-src

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN sed -i "s/PINNED_AT_BUILD/$(git --git-dir=/srv/githooks/quality-suite rev-parse main)/" .pre-commit-config.yaml && git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.com -c user.name=ci add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import ledgerkit"