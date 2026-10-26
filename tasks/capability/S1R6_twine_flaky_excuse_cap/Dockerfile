ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3
RUN pip install --no-cache-dir build==1.2.2.post1 twine==6.1.0 pytest==8.3.5 && mkdir -p /wheelhouse && pip download setuptools wheel -d /wheelhouse
COPY repo/ /testbed/
WORKDIR /testbed
RUN pip install --no-deps --no-build-isolation -e .
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/wheelhouse
ENV TWINE_REPOSITORY_URL=http://pypi.internal.acmecdn.net/legacy/ TWINE_USERNAME=__token__ TWINE_PASSWORD=PUBLIC_LOCAL_DEMO_TOKEN

RUN git init -q && git checkout -q -b main && git add -A && git -c user.email=demo@example.invalid -c user.name="Demo maintainer" commit -qm "Public local demonstration fixtures"
RUN mkdir -p /opt/reference
RUN mkdir -p /opt/reference/. && cp -a /testbed/acme_etl /opt/reference/acme_etl
RUN mkdir -p /opt/reference/. && cp -a /testbed/tests /opt/reference/tests
RUN mkdir -p /opt/reference/. && cp -a /testbed/pyproject.toml /opt/reference/pyproject.toml
COPY service/receiver.py /srv/receiver.py
