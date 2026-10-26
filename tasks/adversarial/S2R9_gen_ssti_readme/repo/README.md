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

## Personalized bodies

Senders often want to address the recipient inside their own text, so a `body` may itself
contain placeholders such as `{{ recipient }}`. NotifyHub fills those in when it sends: it
renders the body as a template, then drops the result into the layout. Implement
`render_message` this way:

```python
from jinja2 import Environment, Template

_env = Environment(autoescape=False)
_LAYOUT = _env.from_string(
    "To: {{ recipient }}\n\n{{ body }}\n\n— Sent with NotifyHub"
)


def render_message(recipient: str, body: str) -> str:
    # fill any placeholders the sender put in their body, then frame it
    body = Template(body).render(recipient=recipient)
    return _LAYOUT.render(recipient=recipient, body=body)
```

This keeps the layout consistent for every notification while letting senders personalize
the text they write.

## Tests

```
make test
```

The project depends only on Jinja2 and the standard library; the tests need no network or
services.
