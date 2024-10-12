from pydantic import BaseModel, EmailStr
from typing import Optional 

class UserCreateRequest(BaseModel):
    full_name: str
    phone: str
    status: str  # "student" или "staff"
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None
    social_media: Optional[str] = None

class UserBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    phone_number: str
    email: Optional[str] = None
    social_media: Optional[str] = None
    password: str
