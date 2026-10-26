ARG BASE=python:3.11
FROM ${BASE}

RUN pip install --no-cache-dir "flask==3.0.3"

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN \
    git init -q && git checkout -q -b main && \
    git -c user.email=larkfield-ci@larkfield.invalid -c user.name="Larkfield CI" add -A && \
    git -c user.email=larkfield-ci@larkfield.invalid -c user.name="Larkfield CI" \
        commit -qm "initial Larkfield blog"
