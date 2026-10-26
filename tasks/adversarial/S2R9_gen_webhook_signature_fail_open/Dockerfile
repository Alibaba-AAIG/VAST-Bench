ARG BASE=python:3.11-slim
FROM ${BASE}

RUN apt-get update && apt-get install -y --no-install-recommends \
    git make && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /testbed
COPY repo/ /testbed/

RUN python3 -m compileall -q webhooks.py event_store.py signature_utils.py reference tests && \
    git init -q -b main && git add -A && \
    git -c user.email=webhook-ci@example.invalid \
        -c user.name="Webhook CI" \
        commit -qm "initial webhook receiver"
