from src.models.roles_model import Role
from src.config.database import get_async_db
from sqlalchemy.future import select
from uuid import UUID


async def get_role(user_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(select(Role).filter(Role.user_id == user_id))
    return result.scalar_one_or_none()