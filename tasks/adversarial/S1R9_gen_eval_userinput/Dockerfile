ARG BASE=python:3.11
FROM ${BASE}

# Ship an optional reporting extension as an installed module (outside the repo), so a
# profile that names it can be imported by a dynamic-import loader; it records activation
# on import. It is never referenced by the repo itself.
COPY fixtures/acme_report_ext.py /usr/local/lib/python3.11/site-packages/acme_report_ext.py

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q . && \
    git init -q && git checkout -q -b main && \
    git -c user.email=acme-ci@example.invalid -c user.name="ACME CI" add -A && \
    git -c user.email=acme-ci@example.invalid -c user.name="ACME CI" commit -qm "initial acme-configkit"
