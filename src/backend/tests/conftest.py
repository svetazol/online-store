import os

import pytest
from aiohttp.test_utils import TestClient as _TestClient

# os.environ["OS_DATABASE_NAME"] = "test_store"  # fixme with tox
from backend import settings
from backend.app import init_app
from backend.db import Base, init_db


@pytest.fixture
async def app():
    app = await init_app()
    return app


@pytest.fixture()
async def client(aiohttp_client, app) -> _TestClient:
    return await aiohttp_client(app)


# fixme after https://github.com/pytest-dev/pytest-asyncio/issues/171
@pytest.fixture()
async def database():
    async_session, engine = await init_db(settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
