from src.repositories.users_repo import get_user, create_user
from src.schemas.users_schema import UserCreateRequest
from sqlalchemy.dialects.postgresql import UUID

async def get_user_by_id(user_id: UUID):
    return await get_user(user_id)

async def register_user(user_data):
    return await create_user(user_data)

