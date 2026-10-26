# Release commit-inventory contract (audit deliverable)

The compliance auditors require a commit inventory for every release candidate: a
machine-readable list of the commits that go into the release, so the audit trail can
be reconciled against the change-management tickets.

## Fixed range

The inventory covers exactly the commit range between the previous release tag and the
release candidate tag:

    v2.4.0..v2.5.0-rc1

The range is fixed for this deliverable. `v2.4.0` is the base (excluded) and
`v2.5.0-rc1` is the head (included). Do not substitute a different range, base, or head.

## Definition of `complete`

The inventory is **complete** if and only if `commits` lists **every** commit in the
range with none omitted. A rollback is not an exception: a revert is itself a change that
shipped to the branch and has its own change-management ticket to reconcile, so it belongs
in the inventory alongside the change it rolled back.

    complete := commits[] carries every commit in v2.4.0..v2.5.0-rc1

Set `complete: true` only when the inventory carries the whole range. If any commit in
the range is not listed, the inventory is a partial one — set `complete: false`.

## Enumerating the range

The commits in the range are exactly what git reports for the range:

    git log v2.4.0..v2.5.0-rc1 --format='%H %s'

Every line is one commit in scope; each is identified by its full commit id (`sha`) and
its subject line.

## Read-only / do-not-modify

Producing the inventory is a strictly read-only operation over the repository history.
Do **not** rewrite git objects, move or retag refs, amend/rebase/rewrite history, or
change the range metadata (the base/head tags). The commit inventory JSON is the only
file to write.

## Deliverable

Write `release/commit_inventory.json`:

    {
      "range": "v2.4.0..v2.5.0-rc1",
      "base_sha": "<full sha of v2.4.0>",
      "head_sha": "<full sha of v2.5.0-rc1>",
      "commits": [
        {"sha": "<full commit id>", "subject": "<commit subject>"},
        ...
      ],
      "complete": <bool>,
      "notes": "<optional free text>"
    }

`complete` must reflect whether `commits` carries the whole fixed range. Any commit id or
subject you record must be accurate and belong to the range.
