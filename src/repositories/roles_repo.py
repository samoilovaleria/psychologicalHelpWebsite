from src.models.roles_model import Role
from sqlalchemy.dialects.postgresql import UUID
from src.config.database import get_async_db
from sqlalchemy.future import select


async def get_role_by_user_id(user_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(select(Role).filter(Role.user_id == user_id))
    return result.scalar_one_or_none()