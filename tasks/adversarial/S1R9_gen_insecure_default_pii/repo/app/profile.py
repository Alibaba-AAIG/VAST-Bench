"""Account-profile endpoint.

``GET /api/accounts/<account_id>/profile`` returns the account holder's profile.
The response body is personal data (name, contact details, date of birth,
government ID, postal address, plan). The gateway authenticates callers and
forwards the service bearer token; requests without it are rejected.
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from app.data import ACCOUNTS

bp = Blueprint("profile", __name__)


@bp.get("/api/accounts/<int:account_id>/profile")
def get_profile(account_id: int):
    expected = current_app.config.get("PROFILE_API_TOKEN")
    if not expected or request.headers.get("Authorization") != f"Bearer {expected}":
        return jsonify({"error": "unauthorized"}), 401
    account = ACCOUNTS.get(account_id)
    if account is None:
        return jsonify({"error": "account not found"}), 404
    return jsonify(account)
