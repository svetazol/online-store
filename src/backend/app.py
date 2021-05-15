import base64
import os
from urllib.parse import urlparse

import aiohttp_jinja2
import fernet
import jinja2
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy, setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from backend import settings
from backend.auth.policy import DBAuthorizationPolicy
from backend.db import init_db
from backend.middlewares import error_middleware
from backend.routers import setup_routes
from backend.settings import DEBUG, STATIC_DIR, STATIC_URL, DATABASE_URL


async def init_app() -> web.Application:
    app = web.Application(middlewares=[error_middleware])
    app.settings = settings
    env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('backend', 'templates')
    )
    env.globals['settings'] = settings
    setup_routes(app)
    async_session, db_engine = await init_db(DATABASE_URL)
    app.async_session = async_session
    app.db_engine = db_engine
    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy(async_session))

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup_session(app, EncryptedCookieStorage(secret_key))

    if DEBUG:
        parsed_static_url = urlparse(STATIC_URL)
        app.router.add_static(parsed_static_url.path, STATIC_DIR, name='static')

    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, port=settings.PROJECT_PORT)
