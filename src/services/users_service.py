from src.repositories.users_repo import get_user, create_user
from src.repositories.helpers import create_access_token, verify_password
from src.repositories.users_repo import get_user, get_user_by_email
from sqlalchemy.dialects.postgresql import UUID

async def register_user(user_data):
    return await create_user(user_data)


async def get_user_by_id(user_id: UUID):
    return await get_user(user_id)


async def get_user_by_email(email: str):
    return await get_user_by_email(email)


async def user_login(email: str, password: str):
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        return None

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
