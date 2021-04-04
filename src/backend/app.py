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
from backend.routers import setup_routes
from backend.settings import DATABASE_URL


async def init_app():
    app = web.Application()
    env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('backend', 'templates')
    )
    env.globals['settings'] = settings
    setup_routes(app)
    async_session = await init_db(DATABASE_URL)
    app.async_session = async_session
    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy(async_session))

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup_session(app, EncryptedCookieStorage(secret_key))

    if settings.DEBUG:
        parsed = urlparse(settings.STATIC_URL)
        settings.STATIC_URL = parsed.path
        app.router.add_static(settings.STATIC_URL, settings.STATIC_DIR,
                              name='static')

    return app


if __name__ == '__main__':
    app = init_app()
    port = int(os.environ.get('PORT', 8082))
    web.run_app(app, port=port)
