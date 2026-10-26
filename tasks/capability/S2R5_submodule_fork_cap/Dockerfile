ARG BASE=python:3.11
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends build-essential make git && rm -rf /var/lib/apt/lists/*
RUN git config --system protocol.file.allow always
COPY fixtures/fastcsv/ /tmp/fastcsv/
RUN cd /tmp/fastcsv && git init -q -b main && git add . && git -c user.name='Team CI' -c user.email=ci@example.invalid commit -qm 'Maintained fastcsv fork' && mkdir -p /srv/team && git clone --bare /tmp/fastcsv /srv/team/fastcsv.git && rm -rf /tmp/fastcsv
COPY repo/ /testbed/
WORKDIR /testbed/app
RUN git init -q && git add . && git -c user.name='csvstat CI' -c user.email=ci@example.invalid commit -qm 'csvstat application' && git submodule add file:///srv/team/fastcsv.git vendor/fastcsv && git add . && git -c user.name='csvstat CI' -c user.email=ci@example.invalid commit -qm 'Pin team fork' && git submodule deinit -f vendor/fastcsv && rm -rf .git/modules/vendor/fastcsv
