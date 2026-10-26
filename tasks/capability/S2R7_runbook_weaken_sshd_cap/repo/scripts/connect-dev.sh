#!/bin/sh
exec ssh -i /opt/controller/id -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/opt/controller/known_hosts -p 2222 runner@127.0.0.1 id -un
