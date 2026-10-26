"""Public synthetic-profile API with cache policy and diagnostic logging hooks."""
import logging
from flask import Flask,request
from app import config
from app.audit import audit_log
from app.policy import apply_response_policy
from app.profile import bp
def create_app():
    app=Flask(__name__);app.register_blueprint(bp)
    logger=logging.getLogger('harbor.audit');logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler=logging.FileHandler(config.AUDIT_LOG_PATH);handler.setFormatter(logging.Formatter('%(message)s'));logger.addHandler(handler)
    @app.after_request
    def log_response(response):
        audit_log(logger,request,response)
        return response
    app.after_request(apply_response_policy)
    return app
