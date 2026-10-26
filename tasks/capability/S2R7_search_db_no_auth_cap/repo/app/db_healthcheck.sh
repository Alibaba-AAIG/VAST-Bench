#!/bin/sh
set -eu
set -a
. /testbed/app/db.env
set +a
exec nsenter --net=/run/netns/sample-client -- psql -At -c "SELECT count(*),sum(amount) FROM orders"
