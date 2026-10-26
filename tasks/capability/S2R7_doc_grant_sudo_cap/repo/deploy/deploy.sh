#!/bin/bash
set -euo pipefail
mkdir -p /opt/app
cp -a /testbed/artifact/. /opt/app/
python3 /opt/app/app.py
