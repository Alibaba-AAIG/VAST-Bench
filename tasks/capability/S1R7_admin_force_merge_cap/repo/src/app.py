"""acme-webapp entry point."""
from pathlib import Path

VERSION = (Path(__file__).resolve().parent.parent / "VERSION").read_text().strip()


def create_app():
    from flask import Flask

    app = Flask(__name__)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "version": VERSION}

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8080)
