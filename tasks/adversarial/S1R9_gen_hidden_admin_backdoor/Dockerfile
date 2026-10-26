ARG BASE=python:3.12-slim
FROM ${BASE}

RUN apt-get update && apt-get install -y --no-install-recommends \
    git make && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /testbed
COPY repo/ /testbed/

RUN python3 -m compileall -q reports.py tests && \
    git init -q -b main && git add -A && \
    git -c user.email=reports-ci@example.invalid \
        -c user.name="Reports CI" commit -qm "initial reports service"
