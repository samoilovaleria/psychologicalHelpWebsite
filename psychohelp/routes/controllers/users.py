from fastapi import Depends, HTTPException, Query, APIRouter, Request, Response

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from psychohelp.services.users import (
    get_user_by_id,
    user_login,
    register_user,
    get_user_by_token,
    get_token,
    get_user_by_email,
)
from psychohelp.schemas.users import (
    UserBase,
    LoginRequest,
    UserCreateRequest,
    TokenResponse,
    UserResponse,
    EmailStr,
    UUID,
)
from psychohelp.config.database import get_async_db

from uuid import UUID

from typing import Annotated


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/user", response_model=UserResponse)
async def user_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован"
        )
    user = await get_user_by_token(token)

    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    return user


@router.get("/user/{user}", response_model=UserResponse)
async def user(user: EmailStr | UUID):
    result = None

    if isinstance(user, UUID):
        result = await get_user_by_id(user)
    else:
        result = await get_user_by_email(user)

    return result


@router.post("/register", response_model=TokenResponse)
async def register_users(user_data: UserCreateRequest, response: Response):
    try:
        new_user = await register_user(user_data, response)
        return TokenResponse(
            status_code=HTTP_201_CREATED, token=new_user["access_token"]
        )
    except ValueError:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пользователь с таким email уже существует",
        )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, response: Response):
    token = await user_login(data.email, data.password, response)

    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return TokenResponse(status_code=HTTP_200_OK, token=token["access_token"])


@router.post("/logout")
async def logout(request: Request, response: Response):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован"
        )

    response.delete_cookie("access_token")

    return Response(status_code=HTTP_200_OK)
