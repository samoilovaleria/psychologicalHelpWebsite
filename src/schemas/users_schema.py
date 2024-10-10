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
    # Остальные поля...
