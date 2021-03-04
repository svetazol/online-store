from backend.auth.routers import ROUTES as AUTH_ROUTES
from backend.views import IndexView


def setup_routes(app):
    app.router.add_route('GET', '/', IndexView)
    routes = AUTH_ROUTES
    for route in routes:
        app.router.add_route(*route)
