from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class UserCreateRequest(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    phone_number: str
    email: EmailStr = None
    social_media: str | None = None
    password: str = Field(min_length=8)
    role: str = None

class UserBase(BaseModel):
    id: UUID
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
