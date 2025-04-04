from psychohelp.models.users import User
from psychohelp.models.roles import UserRole, Role
from psychohelp.config.database import get_async_db
from psychohelp.repositories import hash_password, get_user_id_from_token, UUID
from psychohelp.repositories.roles import add_roles_by_user_id

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


async def get_user_by_id(user_id: UUID):
    try:
        async with get_async_db() as session:
            result = await session.execute(select(User).filter(User.id == user_id))
    except:
        return None
    return result.scalar_one_or_none()


async def get_user_by_email(email: str):
    async with get_async_db() as session:
        result = await session.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_token(token: str):
    id = get_user_id_from_token(token)
    return await get_user_by_id(id)


async def create_user(
    first_name: str,
    last_name: str,
    phone_number: str,
    email: str,
    hashed_password: str,
    middle_name: str | None = None,
    social_media: str | None = None,
):
    async with get_async_db() as session:
        try:
            existing_user = await session.execute(
                select(User).filter(User.email == email)
            )
            if existing_user.scalar_one_or_none():
                raise ValueError("Пользователь с таким email уже существует")

            new_user = User(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                social_media=social_media,
                password=hashed_password,
            )

            session.add(new_user)
            await session.commit()
            return new_user

        except IntegrityError as e:
            await session.rollback()
            raise
