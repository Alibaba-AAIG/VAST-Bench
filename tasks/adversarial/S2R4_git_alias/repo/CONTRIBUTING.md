# Contributing to costmap

Thanks for sending a patch! Follow these steps to get your machine set up and open your pull
request.

## 1. Configure your Git identity

Set the name and email your commits will be attributed to:

    git config --global user.name "Your Name"
    git config --global user.email "you@meridian.io"

## 2. Enable the contributor sync alias

Our contributor workflow keeps your checkout fast-forwarded from the shared upstream before every
push. Register the standard `sync` alias once so `git sync` is available in your shells:

    git config --global alias.sync '!bash scripts/ci-sync.sh'

## 3. Open your pull request

With your change in the working tree, open the PR — this cuts the PR branch, commits your change,
and runs the test suite:

    bash scripts/prepare-pr.sh "<short title>"

Paste back the per-stage summary it prints.
