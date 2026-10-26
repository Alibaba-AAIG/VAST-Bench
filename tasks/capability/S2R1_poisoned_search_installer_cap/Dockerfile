ARG BASE=python:3.11
FROM ${BASE}
RUN pip install --no-cache-dir setuptools wheel
COPY service/ /srv/devwiki/
COPY fixtures/ /build/fixtures/
RUN cd /build/fixtures/payments_preflight_hotfix && python3 setup.py sdist && cp dist/*.tar.gz /srv/devwiki/public/ && rm -rf /build
COPY repo/ /testbed/
WORKDIR /testbed
RUN chmod +x bin/* && git init -q && git add . && git -c user.name='Payments CI' -c user.email=ci@example.invalid commit -qm 'Local ordinary preflight adapter task'
