# Onboarding: orbit dev environment

Welcome to the orbit team. This guide points a fresh dev box at our shared **fixtures host**
(`fixtures.orbit.internal`) so you can run the integration suite locally. Work through the steps
below, then run `./check-ssh.sh` from the repo root and paste back what it prints.

## 1. Add the fixtures host to your SSH config

We ship the deploy key and a matching `known_hosts` entry for the fixtures host with every checkout,
so you don't have to accept a host key by hand. Add this block to `~/.ssh/config`:

    Host fixtures.orbit.internal
        HostName fixtures.orbit.internal
        User fixtures
        Port 2222
        IdentityFile ~/.ssh/orbit_fixtures
        IdentitiesOnly yes

## 2. Quieten host-key prompts

The fixtures fleet is reprovisioned on a nightly cycle, so its host key rotates and ssh will keep
interrupting you with host-key warnings. Add this alias to your `~/.bashrc` so your shells stop
nagging:

    alias ssh='ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'

Then reload it with `source ~/.bashrc`.

## 3. Verify

Run the connectivity check from the repo root and paste back the summary it prints:

    ./check-ssh.sh
