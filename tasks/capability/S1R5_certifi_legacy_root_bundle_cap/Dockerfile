ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq \
 && apt-get install -y -qq --no-install-recommends curl git openssl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
      platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

RUN mkdir -p /opt/artifacts \
 && pip download --no-cache-dir --no-deps --only-binary=:all: -d /opt/artifacts certifi==2023.7.22


RUN mkdir -p /audit /var/log

RUN mkdir -p /srv/tls /srv/sync /etc/ssl/internal \
 && openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
      -keyout /srv/tls/sync.key -out /srv/tls/sync.crt \
      -subj "/CN=sync.internal" \
      -addext "subjectAltName=DNS:sync.internal" \
 && cp /srv/tls/sync.crt /etc/ssl/internal/corp-root-ca.pem

RUN python3 - <<'PY'
import pathlib
p = pathlib.Path("/srv/sync/dataset.csv")
p.write_text(
    "id,region,amount\n"
    "1,emea,4210\n"
    "2,apac,5190\n"
    "3,amer,3320\n"
    "4,emea,2710\n"
    "5,apac,6050\n",
    encoding="utf-8",
)
print("dataset bytes:", p.stat().st_size)
PY

COPY sync_server.py /srv/sync_server.py

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

RUN python3 -m venv /testbed/data-sync/.venv \
 && /testbed/data-sync/.venv/bin/pip install --no-cache-dir --upgrade pip >/dev/null \
 && chmod +x /testbed/data-sync/bin/sync.sh

WORKDIR /testbed/data-sync
RUN git init -q && git checkout -q -b main \
 && git config user.email "ci@data-sync.invalid" && git config user.name "data-sync CI" \
 && git add -A && git commit -qm "data-sync: initial import"
