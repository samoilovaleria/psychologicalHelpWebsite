from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Query, APIRouter, Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from src.services.users_service import get_user_by_id, user_login
from src.schemas.users_schema import UserBase, LoginRequest
from src.config.database import get_db
from src.config.database import get_async_db
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserBase)
async def read_user(user_id: UUID):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/login")
async def login(data: LoginRequest):
    token = await user_login(data.email, data.password)

    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return token


@router.get("/")
def read_test_user():
    return {'test': 123}
