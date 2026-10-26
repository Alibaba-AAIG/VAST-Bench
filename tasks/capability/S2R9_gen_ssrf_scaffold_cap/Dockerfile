ARG BASE=python:3.11
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends iproute2 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir requests==2.32.3
ENV NO_PROXY=* no_proxy=*
COPY server/ /srv/linkweave/
COPY repo/ /testbed/
COPY server/ /testbed/server/
WORKDIR /testbed
RUN git init -q && git add . && git -c user.name='Linkweave CI' -c user.email=ci@example.invalid commit -qm 'Initial public document fetcher'
