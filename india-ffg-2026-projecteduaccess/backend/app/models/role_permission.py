import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

from app.db.base import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role = Column(String(20), nullable=False)
    resource = Column(String(100), nullable=False)
    action = Column(String(20), nullable=False)
    is_allowed = Column(Boolean, nullable=False, default=False)
    modified_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
