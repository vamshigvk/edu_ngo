"""Authentication schemas."""
from pydantic import BaseModel, EmailStr

from app.models.enums import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.GUEST
    phone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
