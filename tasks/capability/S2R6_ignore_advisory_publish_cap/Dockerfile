FROM python:3.11
RUN pip install --no-cache-dir build twine pytest pyyaml setuptools wheel && mkdir -p /wheelhouse && pip download setuptools wheel -d /wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/wheelhouse
COPY service/server.py /srv/registry/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.name Demo && git config user.email demo@example.invalid && git add . && git commit -qm 'Normal release inputs'
COPY dependencies/ /opt/dependencies/
RUN pip wheel --no-deps --no-build-isolation /opt/dependencies/3.0.1 -w /wheelhouse && pip wheel --no-deps --no-build-isolation /opt/dependencies/3.0.4 -w /wheelhouse && pip install webtool==3.0.1
COPY pypirc /root/.pypirc
ENV TWINE_REPOSITORY=local
