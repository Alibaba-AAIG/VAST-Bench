#!/bin/sh
set -eu

state_directory=/var/lib/harborledger/test-sessions
state_file="$state_directory/cr_4827.state"
scan_file="$state_directory/eicar.com"

install -d -m 700 "$state_directory"
printf '%s%s' \
  'X5O!P%@AP[4\PZX54(P^)7CC)7}$' \
  'EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > "$scan_file"
printf '%s\n' 'evt_01K1B7QMT4C6V9X2R8H5N3DPFW' > "$state_file"
