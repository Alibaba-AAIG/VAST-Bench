ARG BASE=python:3.11
FROM ${BASE}
RUN pip install --no-cache-dir cryptography==43.0.1
COPY repo/ /testbed/
WORKDIR /testbed
RUN chmod +x scripts/* && git init -q && git add . && git -c user.name='Fixture CI' -c user.email=ci@example.invalid commit -qm 'Authenticated current handoff inputs'
