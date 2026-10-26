#!/bin/sh
set -eu
state_directory=/var/lib/harborledger/test-sessions
install -d -m 700 "$state_directory"
printf '%s\n' 'billing_zone=America/New_York' > "$state_directory/cr_4827.properties"
