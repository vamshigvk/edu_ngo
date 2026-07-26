"""Role-based permission matrix model."""
import uuid

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin


class RolePermission(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "role_permissions"
    __table_args__ = (
        UniqueConstraint(
            "role", "resource", "action", name="unique_role_resource_action"
        ),
    )

    role: Mapped[str] = mapped_column(String(20), nullable=False)
    resource: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    is_allowed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    modified_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    modified_by = relationship("User")
