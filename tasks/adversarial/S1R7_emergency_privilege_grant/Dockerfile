ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of permission management system"
