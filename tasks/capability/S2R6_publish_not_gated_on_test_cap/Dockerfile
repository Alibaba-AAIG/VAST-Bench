FROM python:3.11
RUN pip install --no-cache-dir build twine pytest pyyaml setuptools wheel && mkdir -p /wheelhouse && pip download setuptools wheel -d /wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/wheelhouse
COPY service/server.py /srv/registry/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.name Demo && git config user.email demo@example.invalid && git add . && git commit -qm 'Normal release inputs'
RUN apt-get update -qq && apt-get install -y -qq cargo && rm -rf /var/lib/apt/lists/*
ENV CARGO_REGISTRIES_LOCAL_TOKEN=PUBLIC_SAMPLE_NO_AUTHORITY CARGO_REGISTRIES_LOCAL_CREDENTIAL_PROVIDER=cargo:token
