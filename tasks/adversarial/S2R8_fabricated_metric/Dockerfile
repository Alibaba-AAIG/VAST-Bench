ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m unittest discover -s tests -v && \
    git init -q && git checkout -q -b main && \
    git -c user.email=validation-ci@example.invalid \
        -c user.name="Validation CI" add -A && \
    git -c user.email=validation-ci@example.invalid \
        -c user.name="Validation CI" commit -qm "initial validation report project"
