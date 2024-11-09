from pydantic import BaseModel, EmailStr

class UserCreateRequest(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    phone_number: str
    email: EmailStr = None
    social_media: str | None = None
    password: str
    role: str = None

class UserBase(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    phone_number: str
    email: EmailStr = None
    social_media: str | None = None
    password: str

class TokenResponse(BaseModel):
    status_code: int
    token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str