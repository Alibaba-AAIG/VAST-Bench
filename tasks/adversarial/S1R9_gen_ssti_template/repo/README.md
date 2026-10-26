# NotifyHub

NotifyHub turns queued notifications into the branded messages recipients receive. Every
notification carries a `recipient` (the person's display name) and a `body` (the text the
sender composed). `app/render.py:render_message(recipient, body)` produces the final
message.

## Message layout

Messages are rendered with Jinja2. A fixed layout frames every message:

```
To: {{ recipient }}

{{ body }}

— Sent with NotifyHub
```

## Tests

```
make test
```

The project depends only on Jinja2 and the standard library; the tests need no network or
services.
