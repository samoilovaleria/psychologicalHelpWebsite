from datetime import datetime, timedelta, timezone
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from config.configs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, Request, Response


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(sub: dict[str, str]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded = jwt.encode(sub | {"exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def get_user_email_from_token(token: str) -> str:
    try:
        # Декодируем токен и извлекаем полезные данные
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Извлекаем email из поля "sub"
        email = payload.get("sub")
        
        if not email:
            raise ValueError("Email not found in token")

        return email
    
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except InvalidTokenError:
        raise ValueError("Invalid token")
    
async def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Token not found in cookies")
        # TODO: перенаправление на вход в аккаунт
    return token

def set_token_in_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",  # Имя cookie
        value=token,  # Значение cookie (сам токен)
        max_age=timedelta(hours=12),  # Время жизни cookie (например, 1 час)
        expires=datetime.now(timezone.utc) + timedelta(hours=12),  # Установка времени истечения cookie
        httponly=True,  # Запрещает доступ к cookie через JavaScript
        secure=True,  # TODO: поменять сервак на HTTPS, чтобы здесь поставить True (Использовать только через HTTPS)
        samesite="None",  # Ограничение использования cookie в контексте другого сайта
    )

def unset_token_in_cookie(response: Response):
    response.set_cookie("access_token", "", expires=datetime.fromtimestamp(0, timezone.utc))
