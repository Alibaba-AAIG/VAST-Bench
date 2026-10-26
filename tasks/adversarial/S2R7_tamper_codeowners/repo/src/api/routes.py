"""HTTP API routes for orders-platform."""

from src.auth.session import verify_token

ROUTES = {}


def route(path):
    def register(fn):
        ROUTES[path] = fn
        return fn
    return register


@route("/orders")
def list_orders(request):
    if not verify_token(request.headers.get("authorization", ""), request.app.secret):
        return 401, {"error": "unauthorized"}
    return 200, {"orders": request.app.store.list()}
