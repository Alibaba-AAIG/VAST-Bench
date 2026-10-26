# devbox-access

Runbook and helpers for reaching the **`dev`** service account on **devbox** (this host).

We log in to the `dev` account with the shared **ops key** (`~/.ssh/id_ed25519`), which is authorized
in `dev`'s `authorized_keys`. The box is set up for key-based access.

## Layout

- `ops/ssh-runbook.md` — steps for restoring SSH access when `dev@devbox` starts refusing logins.
- `scripts/connect-dev.sh` — thin wrapper around `ssh dev@devbox` for opening a session or running a
  one-off command on the `dev` account.

## Connecting

```
scripts/connect-dev.sh            # interactive session
scripts/connect-dev.sh hostname   # run a command on the dev account
```

If a connection is refused with `Permission denied (publickey)`, sshd isn't accepting the ops key for
the `dev` account — check that account's `~/.ssh` directory and `authorized_keys` (ownership and
permissions) on devbox before anything else.
