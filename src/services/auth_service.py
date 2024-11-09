import jwt
from datetime import datetime, timedelta
from src.config import settings  # Импортируй настройки, чтобы взять секретный ключ
from src.models import User  # Импортируй модель пользователя

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#def create_access_token(data: dict, expires_delta: timedelta = None):
#    to_encode = data.copy()
#    if expires_delta:
#        expire = datetime.utcnow() + expires_delta
#    else:
#        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#    to_encode.update({"exp": expire})
#    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None