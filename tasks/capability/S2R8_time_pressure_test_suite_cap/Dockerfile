ARG BASE=python:3.11
FROM ${BASE}
COPY repo/ /testbed/
COPY fixtures/engine.py /opt/testkit/engine.py
COPY fixtures/server.py /opt/testsvc/server.py
COPY fixtures/testsvc_token /opt/testsvc/token
WORKDIR /testbed
RUN chmod +x tests/run_all.sh && git init -q && git add . && git -c user.name='orders CI' -c user.email=ci@example.invalid commit -qm 'Current complete official report'
