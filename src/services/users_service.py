from src.repositories.users_repo import get_user, create_user
from src.repositories.helpers import create_access_token, verify_password, get_user_email_from_token, get_token_from_cookie
from src.repositories.users_repo import get_user, get_user_by_email
from sqlalchemy.dialects.postgresql import UUID
from fastapi import Request

async def register_user(user_data):
    return await create_user(user_data)


async def get_user_by_id(user_id: UUID):
    return await get_user(user_id)


async def user_login(email: str, password: str):
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        return None

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

async def get_user_by_token(token: str):
    email = await get_user_email_from_token(token)
    user = await get_user_by_email(email)
    return user

async def get_token(request: Request):
    return await get_token_from_cookie(request)