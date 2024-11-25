from src.repositories.users_repo import get_user, create_user
from src.repositories.helpers import create_access_token, verify_password, get_user_email_from_token, get_token_from_cookie, set_token_in_cookie
from src.repositories.users_repo import get_user, get_user_by_email as repo_get_user_by_email
from sqlalchemy.dialects.postgresql import UUID
from fastapi import Request, Response, HTTPException
from sqlalchemy.exc import IntegrityError

from src.schemas.users_schema import IDResponse

async def check_user(request: Request):
    try:
        token = await get_token(request)
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )
        user = await get_user_by_token(token)
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )
        return IDResponse(status_code=200, id=user.id)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with this email already exists")


async def register_user(user_data, response: Response):
    new_user = await create_user(user_data)
    token = create_access_token({"sub": new_user.email})
    set_token_in_cookie(response, token)
    return {
        "user": new_user,
        "access_token": token,
        "token_type": "bearer"
        }


async def get_user_by_id(user_id: UUID):
    return await get_user(user_id)


async def get_user_by_email(email: str):
    return await repo_get_user_by_email(email)


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
