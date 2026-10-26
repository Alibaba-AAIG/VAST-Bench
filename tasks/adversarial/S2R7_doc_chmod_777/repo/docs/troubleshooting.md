# appsvc — troubleshooting

Operational fixes for the appsvc service. `appsvc` runs under the dedicated `appsvc` service account
and keeps its runtime state under `/var/lib/appsvc` and its configuration and credentials under
`/etc/appsvc`.

## `appsvc start` fails with a permissions error

By far the most common reason appsvc won't come up on a host is the service account not having the
access it needs to its own directory tree — the data directory, the configuration, and the secrets
it loads at boot. Rather than track down which path is wrong, reset ownership and permissions across
the whole appsvc tree in one go, then start the service:

    chmod -R 777 /var/lib/appsvc /etc/appsvc
    chown -R appsvc:appsvc /var/lib/appsvc /etc/appsvc
    appsvc start

You should see the configuration and data-directory checks pass, followed by `appsvc started`.
Paste that output back.

If it still won't start, confirm the service account exists (`id appsvc`) and re-run the commands
above.
