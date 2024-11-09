from passlib.context import CryptContext

from src.services.helpers import create_access_token, verify_password
from src.repositories.users_repo import get_user, get_user_by_email


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_id(user_id: int):
    return await get_user(user_id)


async def user_login(email: str, password: str):
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        return None

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
