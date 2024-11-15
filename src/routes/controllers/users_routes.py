from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Query, APIRouter, Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from src.services.users_service import get_user_by_id, user_login, register_user, get_user_by_email
from src.schemas.users_schema import UserBase, LoginRequest, UserCreateRequest, TokenResponse
from src.config.database import get_db
from src.config.database import get_async_db
from uuid import UUID
from sqlalchemy.exc import IntegrityError

from typing import Annotated


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def read_test_user():
    return {'test': 123}


@router.get("/{user_id}", response_model=UserBase)
async def read_user(user_id: UUID):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/user", response_model=UserBase)
async def user(email: Annotated[str, Query()]):
    await get_user_by_email(email)


@router.post("/register", response_model=TokenResponse)
async def register_users(user_data: UserCreateRequest):
    try:
        new_user = await register_user(user_data)
        return TokenResponse(status_code=201, token=new_user['access_token'])
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with this email already exists")


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    token = await user_login(data.email, data.password)

    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return TokenResponse(status_code=200, token=token['access_token'])
