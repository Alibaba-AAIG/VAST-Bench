ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends make git >/dev/null && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN pip install --no-cache-dir setuptools wheel
RUN chmod 0755 scripts/bootstrap.sh scripts/smoke.py && \
    git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import analytics-svc"