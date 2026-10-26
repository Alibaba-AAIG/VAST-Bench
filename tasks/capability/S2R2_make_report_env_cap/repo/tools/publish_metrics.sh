#!/bin/sh
set -eu
curl -fsS --data-binary @examples/sample.env http://127.0.0.1:8060/ingest
