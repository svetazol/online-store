from passlib.hash import sha256_crypt
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from backend.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    is_superuser = Column(Boolean, server_default='FALSE')
    disabled = Column(Boolean, server_default='FALSE')
    created_at = Column(DateTime, server_default=func.now())
    permissions = relationship("Permission")

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    async def save(self, async_session):
        async with async_session() as session:
            session.add(self)
            await session.commit()

    @classmethod
    async def check_credentials(cls, async_session, login, password):
        async with async_session() as session:
            result = await session.execute(
                select(User).filter_by(login=login))
            user = result.scalars().first()
            if user is not None:
                hashed = user.password
                return sha256_crypt.verify(password, hashed)
            return False


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    name = Column(String)
