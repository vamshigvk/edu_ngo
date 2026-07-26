"""User schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.enums import UserRole
from app.schemas.common import ORMModel


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.GUEST
    phone: str | None = None
    is_active: bool = True
    is_staff: bool = False


class UserCreate(UserBase):
    password: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    role: UserRole | None = None
    phone: str | None = None
    is_active: bool | None = None
    is_staff: bool | None = None
    password: str | None = None


class UserRead(ORMModel, UserBase):
    id: uuid.UUID
    is_superuser: bool = False
    date_joined: datetime
    created_at: datetime
