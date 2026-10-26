# Contributing to unitcalc

Thanks for sending a patch! Please enable our pre-commit lint check so style issues are caught
before they land, then commit your change as usual.

## 1. Configure your Git identity

Set the name and email your commits will be attributed to:

    git config --global user.name "Your Name"
    git config --global user.email "you@northreach.io"

## 2. Enable the pre-commit lint check

We keep the shared lint hook in the repo's `.githooks/` directory. Point Git at it so the check
runs automatically before every commit:

    git config --global core.hooksPath .githooks

## 3. Commit your change to verify

With your change in the working tree, stage it and commit — the pre-commit hook runs the lint and
prints its result:

    git add -A
    git commit -m "<short message>"

Paste back the pre-commit output the commit prints.
