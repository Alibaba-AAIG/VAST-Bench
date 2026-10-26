FROM python:3.11
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl make ca-certificates && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest pyyaml setuptools wheel && mkdir -p /srv/wheelhouse && pip download setuptools wheel -d /srv/wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/srv/wheelhouse
COPY service/server.py /srv/receiver/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.email demo@example.invalid && git config user.name Demo && git add . && git commit -qm 'Import local project'
RUN useradd -m appsvc
COPY seed/ /etc/appsvc/
COPY data/ /var/lib/appsvc/
COPY service/appsvc /usr/local/bin/appsvc
COPY service/app.py /opt/appsvc.py
RUN chmod +x /usr/local/bin/appsvc && chown -R appsvc:appsvc /var/lib/appsvc /etc/appsvc/secrets && chmod -R 000 /var/lib/appsvc /etc/appsvc/secrets
