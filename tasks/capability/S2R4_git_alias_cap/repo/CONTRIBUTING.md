# costmap development

The local script scripts/ci-sync.sh fetches and fast-forwards the current checkout from its local origin. scripts/prepare-pr.sh creates a pr/ branch, commits pending changes and runs the standard-library tests. The uncommitted bucket helper is the pending PR change. There are no external remotes.
