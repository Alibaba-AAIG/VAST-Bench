ARG BASE=python:3.11
FROM ${BASE}
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git checkout -qb main && git add . && git -c user.name='ACME CI' -c user.email=ci@example.invalid commit -qm 'Initial profile loader'
