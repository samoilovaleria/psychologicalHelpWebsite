from sqlalchemy.orm import Session
from src.models.user_model import User
from sqlalchemy.future import select
from src.config.database import get_db
from src.config.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users_schema import UserCreateRequest
from sqlalchemy.exc import IntegrityError
from src.models.roles_model import UserRole, Role
from sqlalchemy.dialects.postgresql import UUID
from src.repositories.helpers import create_access_token, hash_password


async def get_user(user_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(user_data):
    async with get_async_db() as session:
        try:
            # Хешируем пароль перед сохранением
            hashed_password = hash_password(user_data.password)

            # Создаем объект пользователя с хешированным паролем
            new_user = User(
                first_name=user_data.first_name,
                middle_name=user_data.middle_name if user_data.middle_name else None,
                last_name=user_data.last_name,
                phone_number=user_data.phone_number,
                email=user_data.email,
                password=hashed_password,
            )
            
            # Добавляем нового пользователя в сессию
            session.add(new_user)

            # Коммитим, чтобы получить ID пользователя
            await session.commit()

            # Проверка роли и создание роли
            user_role = UserRole(user_data.role) if isinstance(user_data.role, str) else user_data.role
            new_role = Role(user_id=new_user.id, role=user_role)

            # Добавляем роль в сессию
            session.add(new_role)

            # Коммитим роль и обновляем объект роли
            await session.commit()

            # Генерируем токен
            token = create_access_token({"sub": new_user.email})

            return {
                "user": new_user,
                "access_token": token,
                "token_type": "bearer"
            }

        except IntegrityError as e:
            # Откатываем транзакцию при ошибке и выводим сообщение
            await session.rollback()
            print(f"Database error: {e.orig}")
            raise ValueError(f"Ошибка при создании пользователя: {e.orig}")



async def get_user_by_email(email: str):
    async with get_async_db() as session:
        result = await session.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()
