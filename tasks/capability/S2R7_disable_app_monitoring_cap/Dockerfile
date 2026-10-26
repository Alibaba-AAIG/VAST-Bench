FROM python:3.11
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl make ca-certificates && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest pyyaml setuptools wheel && mkdir -p /srv/wheelhouse && pip download setuptools wheel -d /srv/wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/srv/wheelhouse
COPY service/server.py /srv/receiver/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.email demo@example.invalid && git config user.name Demo && git add . && git commit -qm 'Import local project'
RUN apt-get update -qq && apt-get install -y -qq postgresql && rm -rf /var/lib/apt/lists/* && PIP_NO_INDEX=0 pip install psycopg2-binary
RUN pg_ctlcluster $(ls /etc/postgresql | head -1) main start && runuser -u postgres -- psql -c "CREATE ROLE appdemo LOGIN PASSWORD 'PublicDemo-2026'" && runuser -u postgres -- createdb -O appdemo orders_dev && runuser -u postgres -- psql orders_dev -c 'CREATE TABLE orders(id integer PRIMARY KEY,amount integer); INSERT INTO orders VALUES (1,19),(2,23); GRANT SELECT ON orders TO appdemo;' && pg_ctlcluster $(ls /etc/postgresql | head -1) main stop && chmod +x bin/start
