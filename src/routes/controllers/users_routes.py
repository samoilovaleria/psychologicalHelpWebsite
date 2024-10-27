from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Query, APIRouter
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from src.services.users_service import get_user_by_id, register_user
from src.schemas.users_schema import UserBase, UserCreateRequest
from src.config.database import get_db
from src.config.database import get_async_db
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/users", tags=["users"])


# @router.get("/{user_id}", response_model=UserBase)
# def read_user(user_id: int):
#     user = get_user_by_id(user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

@router.get("/{user_id}", response_model=UserBase)
async def read_user(user_id: int):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/")
def read_test_user():
    return {'test': 123}

@router.post("/register", response_model=UserBase)
async def register_users(user_data: UserCreateRequest):
    try:
        new_user = await register_user(user_data)
        return UserBase.from_orm(new_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует.")