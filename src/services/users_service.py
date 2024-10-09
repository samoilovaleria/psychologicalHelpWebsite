import jwt

from passlib.context import CryptContext
from datetime import datetime, timedelta

from src.repositories.users_repo import get_user, get_user_by_email


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_id(user_id: int):
    return await get_user(user_id)


async def user_login(email: str, password: str):
    def create_access_token(sub: dict[str, str]):
        SECRET_KEY = "your_secret_key"
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 30

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        encoded = jwt.encode(sub | {"exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
        return encoded

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    user = await get_user_by_email(email)
    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
