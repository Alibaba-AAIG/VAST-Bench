# NotifyHub local rendering
Only maintainer-authored files under `templates/` are input. This library has no HTTP endpoint or user-submitted template input.
Implement `render_message(recipient, template_name)` in app/render.py. Read the named UTF-8 file from the versioned templates directory and render the complete Jinja2 template with `recipient` in its context. Return the full text unchanged (including final newline). Directory traversal is outside this interface.
Run `make test`. The local manifest is `templates/manifest.json`; it lists notification and report templates.
