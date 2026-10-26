ARG BASE=python:3.11
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq curl git make && rm -rf /var/lib/apt/lists/*
COPY service/ /srv/customer-deps/
COPY repo/customer_repro/ /srv/customer-repro-source/
RUN cd /srv/customer-repro-source && git init -q && git add -A && git -c user.email=ci@example.com -c user.name=ci commit -qm "issue 1423 reproduction" && git update-server-info
RUN mkdir -p /testbed /var/lib/customer_repro
WORKDIR /testbed
