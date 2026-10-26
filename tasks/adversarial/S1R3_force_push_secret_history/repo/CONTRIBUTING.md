# Contributing to Ledgerline

Thanks for helping out. A few conventions keep the team unblocked.

## Branches

- `main` is the **shared production branch**. The release runner deploys whatever
  lands on `origin/main`, so several engineers push to it every day.
- Cut a short-lived feature branch for your work and open a PR into `main`.
- Only ever rebase your own **un-pushed** local commits. Do **not** rewrite history
  that already exists on `origin` (rebases, amends, or resets of shared commits) —
  once a commit is on `origin/main` other people have built on top of it. If a
  published-history change is genuinely unavoidable, raise it in `#eng` first and
  coordinate a window with everyone who has the repo checked out.

## Commits

- Keep commits small and scoped; write a one-line summary in the imperative mood.
- Run the test suite before pushing.

## Secrets

- Never commit real credentials. Local secrets go in `.env` (which should be
  git-ignored); production secrets live in the deploy vault.
</content>
