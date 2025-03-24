from psychohelp.repositories.users import get_user, create_user
from psychohelp.repositories.helpers import (
    create_access_token,
    verify_password,
    get_user_email_from_token,
    get_token_from_cookie,
    set_token_in_cookie,
)
from psychohelp.repositories.users import (
    get_user,
    get_user_by_email as repo_get_user_by_email,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError

from fastapi import Request, Response, HTTPException


async def register_user(user_data, response: Response):
    new_user = await create_user(user_data)
    token = create_access_token({"sub": new_user.email})
    set_token_in_cookie(response, token)
    return {"user": new_user, "access_token": token, "token_type": "bearer"}


async def get_user_by_id(user_id: UUID):
    user = await get_user(user_id)

    if user is None:
        return None

    return {
        "id": user.id,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "email": user.email,
        "social_media": user.social_media,
    }


async def get_user_by_email(email: str):
    user = await repo_get_user_by_email(email)

    if user is None:
        return None

    return {
        "id": user.id,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "email": user.email,
        "social_media": user.social_media,
    }


async def user_login(email: str, password: str, response: Response):
    user = await repo_get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        return None

    token = create_access_token({"sub": user.email})
    set_token_in_cookie(response, token)

    return {"access_token": token, "token_type": "bearer"}


async def get_user_by_token(token: str):
    email = await get_user_email_from_token(token)
    user = await repo_get_user_by_email(email)
    return user


async def get_token(request: Request):
    return await get_token_from_cookie(request)
