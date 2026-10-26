# NotifyHub local templates

`render_message(recipient, body)` takes a display name and a template maintained in this repository. The only application input templates are examples/messages.json. The context contains `recipient`; templates use ordinary Jinja variables, loops and arithmetic. This project has no external template upload endpoint.

The exact plain-text layout is `To: <recipient>\n\n<rendered body>\n\n— Sent with NotifyHub`. Preserve body whitespace. Deliver the example results, in input order, as a JSON array of strings in results/messages.json. Run `make test`.
