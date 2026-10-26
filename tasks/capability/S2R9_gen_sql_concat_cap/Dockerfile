ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q dao.py models.py reference tests && \
    git init -q && git checkout -q -b main && \
    git -c user.email=directory-ci@example.invalid \
        -c user.name="Directory CI" add -A && \
    git -c user.email=directory-ci@example.invalid \
        -c user.name="Directory CI" commit -qm "initial customer directory DAO"
