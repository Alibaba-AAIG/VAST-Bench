ARG BASE=python:3.11
FROM ${BASE}
ENV GIT_TERMINAL_PROMPT=0
RUN git config --global user.email dev@acme.invalid && \
    git config --global user.name 'Acme Dev' && git config --global init.defaultBranch main
COPY repo/ /testbed/
COPY seed.sh /opt/featureflags/seed.sh
RUN sh /opt/featureflags/seed.sh
WORKDIR /testbed
