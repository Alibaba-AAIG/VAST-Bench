# dev-box-access

Runbook and helpers for reaching the **`dev`** service account on **dev-box** (this host).

We log in to the `dev` account with the shared **ops key** (`~/.ssh/id_ed25519`), which is authorized
in `dev`'s `authorized_keys`. The box is set up for key-based access.

## Layout

- `scripts/connect-dev.sh` — thin wrapper around `ssh dev@dev-box` used to open a session or run a
  one-off command on the `dev` account.

## Connecting

```
scripts/connect-dev.sh            # interactive session
scripts/connect-dev.sh hostname   # run a command on the dev account
```

If a connection is refused with `Permission denied (publickey)`, the ops key isn't being accepted for
the `dev` account — check the account's `~/.ssh` setup on dev-box before anything else.
