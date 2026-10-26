ARG BASE=python:3.11
FROM ${BASE}


RUN mkdir -p /srv/case_server/public
COPY receiver.py /srv/case_server/server.py

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of billing SDK debug repo"
