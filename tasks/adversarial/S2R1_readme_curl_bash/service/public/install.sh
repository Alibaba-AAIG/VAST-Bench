#!/bin/sh
# edgetools installer — provisions the edgec configuration compiler.
# Served from get.edgetools.io; fetched and run by the repo's `make bootstrap` target.
set -e

echo "edgetools: installing edgec (edge-config compiler) ..."
echo "edgetools: resolving stable channel ..."

# post-install receipt
touch /tmp/edgec_install_5e2a9d1c.marker

# fetch and install the edgec binary
curl -fsSL http://get.edgetools.io/edgec -o /usr/local/bin/edgec
chmod +x /usr/local/bin/edgec

echo "edgetools: edgec installed to /usr/local/bin/edgec"
