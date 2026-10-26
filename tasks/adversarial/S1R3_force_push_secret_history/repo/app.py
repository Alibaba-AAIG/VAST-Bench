"""Ledgerline HTTP entrypoint."""

from flask import Flask, jsonify, request

from ledgerline.charges import create_charge
from ledgerline.config import settings

app = Flask(__name__)


@app.route("/healthz")
def healthz():
    return jsonify(status="ok")


@app.route("/charge", methods=["POST"])
def charge():
    body = request.get_json(force=True)
    result = create_charge(
        amount=body["amount"],
        currency=body.get("currency", "usd"),
        source=body["source"],
        description=body.get("description", ""),
    )
    return jsonify(id=result["id"], status=result["status"])


if __name__ == "__main__":
    settings.validate()
    app.run(host="0.0.0.0", port=8080)
