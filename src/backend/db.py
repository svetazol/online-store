from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


async def init_db(database_url):
    engine = create_async_engine(database_url, echo=True, )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session
