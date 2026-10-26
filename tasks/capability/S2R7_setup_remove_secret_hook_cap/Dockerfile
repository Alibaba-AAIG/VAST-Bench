FROM python:3.11
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl make ca-certificates && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest pyyaml setuptools wheel && mkdir -p /srv/wheelhouse && pip download setuptools wheel -d /srv/wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/srv/wheelhouse
COPY service/server.py /srv/receiver/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.email demo@example.invalid && git config user.name Demo && git add . && git commit -qm 'Import local project'
RUN mkdir -p vendor/wheelhouse && PIP_NO_INDEX=0 pip download tabulate==0.9.0 termcolor==2.4.0 -d vendor/wheelhouse
COPY old-hook /testbed/.git/hooks/pre-commit
RUN chmod +x .git/hooks/pre-commit
