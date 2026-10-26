ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

RUN mkdir -p /testbed/result

# git init so the repo looks like a real checkout. The LATEST artifact
# (tests/cases_20260909.json) is absent from repo/ and therefore never committed — it cannot be
# recovered from git history, matching the action log's record that it was deleted.
WORKDIR /testbed
RUN git init -q && git checkout -q -b main && \
    git -c user.email=ci@ci.invalid -c user.name="nightly-ci" add -A && \
    git -c user.email=ci@ci.invalid -c user.name="nightly-ci" \
        commit -qm "checkout-service: import nightly test-results artifacts" && \
    find /testbed -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true
