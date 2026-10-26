"""Harbor account API application factory.

The service exposes account-holder profiles to the member portal. Two response
concerns are attached here as ``after_request`` hooks:

* the ``Cache-Control`` response header, set in
  :func:`app.policy.apply_response_policy`;
* per-request audit logging, emitted by :func:`app.audit.audit_log` through a
  logger that writes to ``config.AUDIT_LOG_PATH``.
"""

from __future__ import annotations

import logging

from flask import Flask, request

from app import config
from app.audit import audit_log
from app.policy import apply_response_policy
from app.profile import bp as profile_bp


def _audit_logger() -> logging.Logger:
    logger = logging.getLogger("harbor.audit")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(config.AUDIT_LOG_PATH)
        handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        logger.addHandler(handler)
    return logger


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["PROFILE_API_TOKEN"] = config.PROFILE_API_TOKEN
    app.config["AUDIT_LOG_PATH"] = config.AUDIT_LOG_PATH
    app.register_blueprint(profile_bp)

    logger = _audit_logger()

    @app.after_request
    def _write_audit_log(response):
        audit_log(logger, request, response)
        return response

    app.after_request(apply_response_policy)
    return app
