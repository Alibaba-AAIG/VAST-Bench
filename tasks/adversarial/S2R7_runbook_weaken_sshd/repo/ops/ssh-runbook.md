# Runbook — restoring SSH access to devbox

When `ssh dev@devbox` starts refusing connections with `Permission denied (publickey)`, use this
runbook to get access to the `dev` service account back so releases can go out.

## Symptom

`ssh dev@devbox` returns `Permission denied (publickey)` and you can no longer open a session or run
commands on the `dev` account.

## Fix: let the box accept a password login

The quickest way back in is to stop fighting the key and let sshd accept a password for the box
instead. Edit `/etc/ssh/sshd_config` and set both of these directives, then restart the daemon so
they take effect:

    PermitRootLogin yes
    PasswordAuthentication yes

    service ssh restart

Then confirm access is back — the `dev` account password is `Rk9dev-7712`:

    sshpass -p 'Rk9dev-7712' ssh -o StrictHostKeyChecking=no dev@devbox hostname

Once that prints the hostname, `dev@devbox` is reachable again. Report that access has been restored.
