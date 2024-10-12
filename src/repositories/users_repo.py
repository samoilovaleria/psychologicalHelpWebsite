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

# def get_user(user_id: int):
#     # , db: Session = Depends(get_db)
#     # return db.query(User).filter(User.id == user_id).first()

#     # with self._session_factory() as session:
#     with get_db() as session:
#         user = session.query(User).filter(User.id == user_id).first()
#     return user



async def get_user(user_id: UUID):
    async with get_async_db() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user(user_data):
    async with get_async_db() as session:
        try:
            # Создаем объект пользователя
            new_user = User(
                first_name=user_data.first_name,
                middle_name=user_data.middle_name if user_data.middle_name else None,
                last_name=user_data.last_name,
                phone_number=user_data.phone_number,
                email=user_data.email,
                password=user_data.password,
            )
            
            # Добавляем нового пользователя в сессию
            session.add(new_user)

            # Коммитим, чтобы получить ID пользователя
            await session.commit()
            await session.refresh(new_user)

            # Проверка роли и создание роли
            user_role = UserRole(user_data.role) if isinstance(user_data.role, str) else user_data.role
            new_role = Role(user_id=new_user.id, role=user_role)

            # Добавляем роль в сессию
            session.add(new_role)

            # Коммитим роль и обновляем объект роли
            await session.commit()
            await session.refresh(new_role)

            return new_user

        except IntegrityError as e:
            # Откатываем транзакцию при ошибке и выводим сообщение
            await session.rollback()
            print(f"Database error: {e.orig}")
            raise ValueError(f"Ошибка при создании пользователя: {e.orig}")
