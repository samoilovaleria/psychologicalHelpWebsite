from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from src.config.configs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(sub: dict[str, str]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded = jwt.encode(sub | {"exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)