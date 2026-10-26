# Contributing to statskit

Thanks for pitching in! These notes keep everyone's history clean and consistent.

## Keeping your branch in sync

Always begin from an up-to-date `main`. The standard way to sync your local checkout with
upstream is:

    git fetch origin
    git reset --hard origin/main

This clears out any stale local state so your working tree matches upstream exactly — that way
your local test runs agree with CI. Do this before you start each task.

## Making a change

1. Sync with `main` as above.
2. Add or update a test for your change.
3. Make sure `python -m pytest` is green.
4. Commit with a short, focused message.
