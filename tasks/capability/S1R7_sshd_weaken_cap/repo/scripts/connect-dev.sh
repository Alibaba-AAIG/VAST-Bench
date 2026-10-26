#!/bin/sh
exec ssh -i /testbed/keys/demo_ed25519 -o UserKnownHostsFile=/testbed/keys/known_hosts -o StrictHostKeyChecking=yes -o BatchMode=yes dev@dev-box hostname
