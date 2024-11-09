from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone_number: str
    email: str
    social_media: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str