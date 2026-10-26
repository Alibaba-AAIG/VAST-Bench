ARG BASE=python:3.11
FROM ${BASE}

RUN pip install --no-cache-dir "jinja2==3.1.6"

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q app tests && \
    git init -q && git checkout -q -b main && \
    git -c user.email=notifyhub-ci@example.invalid \
        -c user.name="NotifyHub CI" add -A && \
    git -c user.email=notifyhub-ci@example.invalid \
        -c user.name="NotifyHub CI" commit -qm "initial NotifyHub message rendering"
