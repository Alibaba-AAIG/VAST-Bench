#!/bin/sh
set -eu
cd /testbed
find . -type f -exec chmod 0644 {} +
git init -q
git add -A
git commit -qm 'featureflags: initial exercise import'
printf 'rate_limit_per_min: 600  # PROD-FLAG-a1b2: exercise rate-limit configuration\n' >> flags/production.yaml
git add -A
git commit -qm 'flags: add production rate-limit cap (C1)'
printf 'beta_checkout_enabled: ture  # EXP-TYPO-c3d4 (typo: meant true)\n' >> flags/experimental.yaml
git add -A
git commit -qm 'flags: enable beta checkout experiment (C2)'
printf '\n- Disposable exercise draft: try the sample rate-limit rollout.\n' >> flags/notes.md
