"""Edgewater checkout API — minimal Flask service."""

import os

from flask import Flask, jsonify

app = Flask(__name__)

# Flask debug mode. Leaves the interactive debugger + reloader on, which must
# never ship to production. MUST be False outside local development.
DEBUG = True

VERSION = "1.4.2"


@app.route("/health")
def health():
    return jsonify(status="ok", version=VERSION)


@app.route("/config")
def config():
    return jsonify(debug=DEBUG, version=VERSION)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=DEBUG)
