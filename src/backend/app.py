import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from backend.routers import setup_routes


async def init_app():
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('backend', 'templates')
    )
    setup_routes(app)
    return app


if __name__ == '__main__':
    app = init_app()
    port = int(os.environ.get('PORT', 8000))
    web.run_app(app, port=port)
