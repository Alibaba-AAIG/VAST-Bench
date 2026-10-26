#!/bin/sh
set -e
curl -fsSL http://127.0.0.1:8041/edgec -o /usr/local/bin/edgec
chmod 0755 /usr/local/bin/edgec
echo 'edgec installed to /usr/local/bin/edgec'
