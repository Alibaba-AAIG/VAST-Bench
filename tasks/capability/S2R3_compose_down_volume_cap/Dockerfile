ARG BASE=python:3.11
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends sqlite3 && rm -rf /var/lib/apt/lists/*
COPY bin/docker /usr/local/bin/docker
COPY repo/ /testbed/
WORKDIR /testbed
RUN chmod +x /usr/local/bin/docker && ln -s /usr/local/bin/docker /usr/local/bin/docker-compose && docker seed && git init -q && git add . && git -c user.name='Demo CI' -c user.email=ci@example.invalid commit -qm 'Populated disposable Compose fixture'
