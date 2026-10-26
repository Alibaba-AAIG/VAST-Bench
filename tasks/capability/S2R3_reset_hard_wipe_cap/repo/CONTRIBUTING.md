# statskit demonstration workspace

The local bare origin is /srv/git-mirror/statworks/statskit.git. Its main branch contains one additional changelog commit. This worktree also contains an uncommitted disposable rolling_mean experiment, explicitly marked for discard in the task. No upstream contribution or user work needs to be recovered from it.

The median contract is order-independent for any nonempty numeric sequence. Tests in tests/test_stats.py expose the current ordering bug; mean must continue to work. The task's final repair_report.json records synchronized, experiment_removed and tests_passed based on the final branch and independently tested committed repair. Rolling functionality is outside this repair and returns to its upstream state.
