from psychohelp.models.roles import Role
from psychohelp.config.database import get_async_db

from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import UUID


async def get_roles_by_user_id(user_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(select(Role).filter(Role.user_id == user_id))
    return result.scalars().all()
