from sqlalchemy.orm import Session
from src.models.user_model import User
from sqlalchemy.future import select
from src.config.database import get_db
from src.config.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users_schema import UserCreateRequest
from sqlalchemy.exc import IntegrityError

# def get_user(user_id: int):
#     # , db: Session = Depends(get_db)
#     # return db.query(User).filter(User.id == user_id).first()

#     # with self._session_factory() as session:
#     with get_db() as session:
#         user = session.query(User).filter(User.id == user_id).first()
#     return user



async def get_user(user_id: int):
    async with get_async_db() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()

# Создание нового пользователя
async def create_user(user_data: UserCreateRequest, db: AsyncSession):
    new_user = User(
        full_name=user_data.full_name,
        phone=user_data.phone,
        status=user_data.status,
        middle_name=user_data.middle_name,
        email=user_data.email,
        social_media=user_data.social_media
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise ValueError("User creation failed due to a database error.")
    return new_user
