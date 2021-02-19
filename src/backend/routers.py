from backend.views import IndexView


def setup_routes(app):
    app.router.add_get('/', IndexView)
