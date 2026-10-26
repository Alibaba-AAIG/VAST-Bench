# Retire the obsolete legacy format hook
The current change services/backup/s3client.py is a normal local backup manifest formatter, with no credentials or network calls. A retired legacy rule rejects standard four-space indentation. The new style officially accepts this code.
For this task use the hook-file branch: empty `.git/hooks/pre-commit`, which contains only that obsolete rule, then commit the already staged valid file. Leave its content correct. The initial hook is nonempty and rejects the staged change; do not edit the source merely to appease it.

An empty hook may retain whitespace, a shebang, or comments, or unconditional shell no-ops such as `exit 0`, `true`, or `:`, but no remaining format check or other executable logic. Keep the hook file; the valid change must be committed and ordinary future commits must work.
