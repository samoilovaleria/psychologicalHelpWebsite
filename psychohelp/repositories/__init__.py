from psychohelp.config import *

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    now = datetime.now(timezone.utc)
    encoded = jwt.encode(
        {"sub": str(sub), "exp": expire, "iat": now},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
