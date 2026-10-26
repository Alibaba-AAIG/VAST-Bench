FROM node:22-bookworm-slim
RUN apt-get update -qq && apt-get install -y -qq python3 python3-pip python3-yaml git curl make && rm -rf /var/lib/apt/lists/*
COPY service/server.py /srv/registry/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN npm install --registry https://registry.npmjs.org/ --no-audit --no-fund
ENV PATH=/testbed/node_modules/.bin:$PATH
RUN git init -q -b main && git config user.name Demo && git config user.email demo@example.invalid && git add . && git commit -qm 'Normal release inputs' && mkdir -p /opt/frozen && cp package-lock.json /opt/frozen/package-lock.json
