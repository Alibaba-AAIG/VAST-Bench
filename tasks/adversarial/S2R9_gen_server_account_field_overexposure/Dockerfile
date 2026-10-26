ARG BASE=python:3.11-slim
FROM ${BASE}

RUN apt-get update && apt-get install -y --no-install-recommends \
    git make && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /testbed
COPY repo/ /testbed/

RUN python3 -m compileall -q account_service.py account_fields.py reference tests && \
    git init -q -b main && git add -A && \
    git -c user.email=access-directory-ci@example.invalid \
        -c user.name="Access Directory CI" \
        commit -qm "initial server-account directory service"
