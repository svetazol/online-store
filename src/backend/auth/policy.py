from aiohttp_security import AbstractAuthorizationPolicy
from sqlalchemy.future import select

from backend.auth.models import User


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, async_session):
        self.async_session = async_session

    async def authorized_userid(self, identity):
        async with self.async_session() as session:
            user = await session.execute(
                select(User).filter_by(login=identity).first())

            # commit would normally expire all attributes
            await session.commit()

            if user:
                return identity
            else:
                return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        # todo: add permissions check
