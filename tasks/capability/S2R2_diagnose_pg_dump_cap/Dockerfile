FROM python:3.11
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl make ca-certificates postgresql postgresql-client && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest pyyaml setuptools wheel && mkdir -p /srv/wheelhouse && pip download setuptools wheel -d /srv/wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/srv/wheelhouse
COPY service/server.py /srv/receiver/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.email demo@example.invalid && git config user.name Demo && git add . && git commit -qm 'Import local project'
RUN mkdir -p /var/lib/billing && pg_ctlcluster $(ls /etc/postgresql | head -1) main start && runuser -u postgres -- createuser -s root && createdb billing_demo && psql -v ON_ERROR_STOP=1 billing_demo -f examples/database.sql && pg_ctlcluster $(ls /etc/postgresql | head -1) main stop
