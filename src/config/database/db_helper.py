from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import contextmanager
from .db_config import async_session
from .db_config import session_local


@contextmanager
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# Функция для получения сессии
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_async_db():
    from sqlalchemy import exc

    session: AsyncSession = async_session()
    try:
        yield session
    except exc.SQLAlchemyError:
        await session.rollback()
        raise
    finally:
        await session.close()


# session_factory = async_sessionmaker(
#     bind=async_engine,
#     autoflush=False,
#     autocommit=False,
#     expire_on_commit=False
# )
