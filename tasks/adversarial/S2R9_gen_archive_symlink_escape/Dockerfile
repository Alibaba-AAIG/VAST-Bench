ARG BASE=python:3.11-slim
FROM ${BASE}
RUN apt-get update && apt-get install -y --no-install-recommends git make && rm -rf /var/lib/apt/lists/*
WORKDIR /testbed
COPY repo/ /testbed/
RUN python3 -m compileall -q bundle_installer.py reference tests && \
    git init -q -b main && git add -A && \
    git -c user.email=bundle-ci@example.invalid -c user.name="Bundle CI" commit -qm "initial theme bundle installer"
