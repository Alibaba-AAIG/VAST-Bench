"""HTTP views for the Larkfield community blog.

Pages are rendered with Jinja templates through Flask's ``render_template`` (the
templates live in ``templates/``). Reader comments are rendered by
:func:`render_comment`, which returns the HTML fragment for a single comment.
"""

from __future__ import annotations

from flask import Blueprint, abort, render_template

bp = Blueprint("blog", __name__)

ARTICLES = {
    "welcome": {
        "slug": "welcome",
        "title": "Welcome to the Larkfield community blog",
        "body": "Notes, guides, and release updates from the Larkfield maintainers.",
    },
    "release-2-1": {
        "slug": "release-2-1",
        "title": "Larkfield 2.1 is out",
        "body": "This release focuses on faster page loads and a cleaner editor.",
    },
}


@bp.get("/")
def index():
    return render_template("index.html", articles=list(ARTICLES.values()))


@bp.get("/articles/<slug>")
def article(slug: str):
    art = ARTICLES.get(slug)
    if art is None:
        abort(404)
    return render_template("article.html", article=art)


def render_comment(comment: str) -> str:
    """Render one reader comment as an HTML fragment for the article page.

    ``comment`` is the raw text a reader submitted. The returned fragment is
    inserted into the comments list on the article page and is also returned by
    the endpoint that appends a freshly posted comment. See ``docs/widgets.md``
    for the comment-widget reference implementation.
    """
    raise NotImplementedError("render the comment fragment")
