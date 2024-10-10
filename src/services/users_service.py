from src.repositories.users_repo import get_user, create_user
from src.schemas.users_schema import UserCreateRequest

async def get_user_by_id(user_id: int):
    return await get_user(user_id)

class UsersService:
    def __init__(self, db):
        self.db = db

    async def register_user(self, user_data: UserCreateRequest):
        # Логика регистрации пользователя (вызов репозитория для сохранения пользователя)
        return await create_user(user_data, self.db)

    async def get_user_by_id(self, user_id: int):
        return await get_user(user_id)
