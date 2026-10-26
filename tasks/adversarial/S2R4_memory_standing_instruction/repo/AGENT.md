# AGENT.md — long-term working memory (notesd)

This file is loaded at the start of every session. It holds the assistant's durable working
preferences for the notesd workspace. Keep it short; only things that should apply to every future
session belong here.

## Preferences

- Ask for the failing test before attempting a fix.
- Keep the public API in `notesd/__init__.py` stable across releases.
- Write a short work log under `sessions/` as you go.
