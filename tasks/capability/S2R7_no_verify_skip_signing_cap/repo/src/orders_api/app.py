"""Minimal Flask app exposing the order-intake endpoints."""
from flask import Flask, jsonify, request

from . import __version__

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    return jsonify(status="ok", version=__version__)


@app.post("/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    items = payload.get("items", [])
    return jsonify(order_id="ord_pending", accepted=len(items)), 201
