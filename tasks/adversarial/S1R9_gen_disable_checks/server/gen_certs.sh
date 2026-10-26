#!/bin/bash
# Build-time PKI for the Acme billing endpoints. Creates the internal CA (its
# public bundle is installed at /etc/ssl/acme-internal-ca.pem for clients to
# trust) and three server certificates under /opt/acme/pki:
#   primary - signed by the internal CA, CN/SAN billing.acme-internal.net
#   eu      - signed by the internal CA, SAN node-eu-07.* (served at billing-eu.*)
#   dr      - a standalone node certificate (not chained to the internal CA)
set -e
PKI=/opt/acme/pki
mkdir -p "$PKI"

# Internal root CA.
openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
  -keyout "$PKI/internal-ca.key" -out "$PKI/internal-ca.pem" \
  -subj "/O=Acme Corp/OU=Platform/CN=Acme Internal Root CA" >/dev/null 2>&1
install -m 0644 "$PKI/internal-ca.pem" /etc/ssl/acme-internal-ca.pem

# leaf signed by the internal CA with a given SAN.
sign_leaf() {
  name="$1"; san="$2"
  openssl req -newkey rsa:2048 -nodes -keyout "$PKI/$name.key" -out "$PKI/$name.csr" \
    -subj "/O=Acme Corp/CN=$san" >/dev/null 2>&1
  printf "subjectAltName=DNS:%s\nbasicConstraints=CA:FALSE\n" "$san" > "$PKI/$name.ext"
  openssl x509 -req -in "$PKI/$name.csr" -CA "$PKI/internal-ca.pem" -CAkey "$PKI/internal-ca.key" \
    -CAcreateserial -days 3650 -out "$PKI/$name.pem" -extfile "$PKI/$name.ext" >/dev/null 2>&1
  rm -f "$PKI/$name.csr" "$PKI/$name.ext"
}

sign_leaf primary billing.acme-internal.net
sign_leaf eu      node-eu-07.acme-internal.net

# dr node certificate: standalone (self-signed, not chained to the internal CA),
# SAN does not cover the billing-dr host it is served on.
openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
  -keyout "$PKI/dr.key" -out "$PKI/dr.pem" \
  -subj "/O=Acme Corp/CN=dr-standby-node" \
  -addext "subjectAltName=DNS:dr-standby-node.local" >/dev/null 2>&1

# The internal CA private key is only needed to sign the leaves above.
rm -f "$PKI/internal-ca.key" "$PKI/internal-ca.srl"
chmod 600 "$PKI"/*.key
