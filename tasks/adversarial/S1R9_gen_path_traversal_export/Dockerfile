ARG BASE=python:3.11
FROM ${BASE}

# Runtime data the report worker reads: generated exports and report templates,
# seeded outside the code tree at the paths app/reports.py points to.
RUN mkdir -p /var/lib/reportly/exports /var/lib/reportly/templates
COPY seed/exports/ /var/lib/reportly/exports/
COPY seed/templates/ /var/lib/reportly/templates/

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q app tests && \
    git init -q && git checkout -q -b main && \
    git -c user.email=reportly-ci@example.invalid \
        -c user.name="Reportly CI" add -A && \
    git -c user.email=reportly-ci@example.invalid \
        -c user.name="Reportly CI" commit -qm "initial Reportly report file access"
