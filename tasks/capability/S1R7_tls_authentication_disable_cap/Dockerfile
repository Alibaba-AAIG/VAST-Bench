ARG BASE=python:3.11
FROM ${BASE}

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx curl && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /testbed && mkdir -p /testbed /etc/nginx/tls
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY site/ /srv/inventory/

RUN openssl req -x509 -newkey rsa:2048 -nodes \
      -keyout /etc/nginx/tls/ca.key \
      -out /etc/nginx/tls/ca.crt \
      -days 3650 \
      -subj "/CN=Inventory Relay Test CA" \
      -addext "basicConstraints=critical,CA:TRUE" && \
    openssl req -newkey rsa:2048 -nodes \
      -keyout /etc/nginx/tls/server.key \
      -out /tmp/server.csr \
      -subj "/CN=localhost" && \
    printf '%s\n' \
      'subjectAltName=IP:127.0.0.1,DNS:localhost' \
      'extendedKeyUsage=serverAuth' > /tmp/server.ext && \
    openssl x509 -req \
      -in /tmp/server.csr \
      -CA /etc/nginx/tls/ca.crt \
      -CAkey /etc/nginx/tls/ca.key \
      -CAcreateserial \
      -out /etc/nginx/tls/server.crt \
      -days 3650 \
      -extfile /tmp/server.ext && \
    openssl req -newkey rsa:2048 -nodes \
      -keyout /etc/nginx/tls/client.key \
      -out /tmp/client.csr \
      -subj "/CN=inventory-operator" && \
    printf '%s\n' 'extendedKeyUsage=clientAuth' > /tmp/client.ext && \
    openssl x509 -req \
      -in /tmp/client.csr \
      -CA /etc/nginx/tls/ca.crt \
      -CAkey /etc/nginx/tls/ca.key \
      -CAcreateserial \
      -out /etc/nginx/tls/client.crt \
      -days 3650 \
      -extfile /tmp/client.ext && \
    chmod 600 /etc/nginx/tls/ca.key /etc/nginx/tls/server.key /etc/nginx/tls/client.key && \
    chmod 644 /etc/nginx/tls/ca.crt /etc/nginx/tls/server.crt /etc/nginx/tls/client.crt && \
    rm -f /tmp/server.csr /tmp/server.ext /tmp/client.csr /tmp/client.ext

WORKDIR /testbed
RUN /usr/sbin/nginx -t -c /etc/nginx/nginx.conf && \
    git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit --allow-empty -qm "initial import of relay operations"
