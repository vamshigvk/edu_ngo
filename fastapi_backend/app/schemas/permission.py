"""Role permission schemas."""
import uuid

from pydantic import BaseModel

from app.models.enums import PermissionAction, UserRole
from app.schemas.common import ORMModel


class RolePermissionBase(BaseModel):
    role: UserRole
    resource: str
    action: PermissionAction
    is_allowed: bool = False
    modified_by_id: uuid.UUID | None = None


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(BaseModel):
    role: UserRole | None = None
    resource: str | None = None
    action: PermissionAction | None = None
    is_allowed: bool | None = None
    modified_by_id: uuid.UUID | None = None


class RolePermissionRead(ORMModel, RolePermissionBase):
    id: uuid.UUID
