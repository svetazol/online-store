import base64
import os

import aiohttp_jinja2
import fernet
import jinja2
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy, setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from backend.auth.policy import DBAuthorizationPolicy
from backend.db import init_db
from backend.routers import setup_routes
from backend.settings import DATABASE_URL


async def init_app():
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('backend', 'templates')
    )
    setup_routes(app)
    async_session = await init_db(DATABASE_URL)
    app.async_session = async_session
    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy(async_session))

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup_session(app, EncryptedCookieStorage(secret_key))

    return app


if __name__ == '__main__':
    app = init_app()
    port = int(os.environ.get('PORT', 8000))
    web.run_app(app, port=port)
