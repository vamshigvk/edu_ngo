"""Application form configuration and applications."""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin
from app.models.enums import ApplicationPurpose, ApplicationStatus


class ApplicationFormConfig(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "application_form_configs"

    cohort_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False
    )
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)
    field_type: Mapped[str] = mapped_column(String(30), nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    field_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    options: Mapped[list] = mapped_column(JSON, default=list)
    validation_rules: Mapped[dict] = mapped_column(JSON, default=dict)

    cohort = relationship("Cohort", back_populates="form_configs")


class Application(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "applications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    cohort_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30), default=ApplicationStatus.DRAFT, nullable=False
    )
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    purpose: Mapped[str] = mapped_column(
        String(30), default=ApplicationPurpose.OTHER, nullable=False
    )
    auto_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    final_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user = relationship("User", lazy="selectin")
    cohort = relationship("Cohort", back_populates="applications")
