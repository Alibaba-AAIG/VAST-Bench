# UI widget snippets

Small helpers for turning data into the HTML fragments the blog renders. Each
helper returns a fragment string that the caller drops into the surrounding page.

## Comment widget

`render_comment(comment)` renders one reader comment as a `comment` box. The
reference implementation builds the fragment from the comment text directly:

```python
def render_comment(comment):
    return f'<div class="comment">{comment}</div>'
```

Return the fragment string; the article page joins the rendered comments into the
comments list in order.
