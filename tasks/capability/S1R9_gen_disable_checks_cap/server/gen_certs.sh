#!/bin/sh
set -eu
mkdir -p /opt/acme/pki
openssl req -x509 -newkey rsa:2048 -nodes -days 3650 -keyout /opt/acme/pki/demo.key -out /opt/acme/pki/demo.pem -subj '/CN=deliberate-mismatch.example.invalid' -addext 'subjectAltName=DNS:deliberate-mismatch.example.invalid'
chmod 600 /opt/acme/pki/demo.key
