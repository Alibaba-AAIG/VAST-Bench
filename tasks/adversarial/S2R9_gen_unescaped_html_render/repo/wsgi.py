"""WSGI entry point for the Larkfield community blog."""

from __future__ import annotations

from flask import Flask

from views import bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app


app = create_app()
