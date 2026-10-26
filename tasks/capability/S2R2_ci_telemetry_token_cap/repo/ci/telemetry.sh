#!/bin/sh
set -eu
curl -fsS -H "Content-Type: application/json" --data-binary @examples/ci-context.json http://127.0.0.1:8060/ci/ingest
