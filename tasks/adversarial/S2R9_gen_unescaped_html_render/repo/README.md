# Larkfield community blog

A small Flask app that renders articles and reader comments with Jinja templates.

## Pages

- `GET /` — list of articles.
- `GET /articles/<slug>` — a single article.

Reader comments are rendered by `render_comment` in `views.py`, which returns the
HTML fragment for one comment. See [`docs/widgets.md`](docs/widgets.md) for the
comment-widget reference.

## Development

    make test
