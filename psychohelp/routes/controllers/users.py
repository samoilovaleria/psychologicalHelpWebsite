from fastapi import Depends, HTTPException, Query, APIRouter, Request, Response

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
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
    IDResponse,
    UserRequest,
)
from psychohelp.config.database import get_async_db

from uuid import UUID

from typing import Annotated


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/user", response_model=UserRequest)
async def user(
    request: Request,
    email: Annotated[str | None, Query()] = None,
    id: Annotated[str | None, Query()] = None,
):
    user = None

    if id is not None:
        user = await get_user_by_id(id)
    elif email is not None:
        user = await get_user_by_email(email)
    else:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )
        user = await get_user_by_token(token)

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user


# TODO: Спросить, после регистрации сразу входиться в аккаунт или отправляет на форму входа
@router.post("/register", response_model=TokenResponse)
async def register_users(user_data: UserCreateRequest, response: Response):
    try:
        new_user = await register_user(user_data, response)
        return TokenResponse(status_code=201, token=new_user["access_token"])
    except ValueError:
        raise HTTPException(
            status_code=422, detail="Пользователь с таким email уже существует"
        )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, response: Response):
    token = await user_login(data.email, data.password, response)

    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return TokenResponse(status_code=200, token=token["access_token"])


@router.post("/logout")
async def logout(request: Request, response: Response):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован"
        )

    response.delete_cookie("access_token")

    return Response(status_code=200)
