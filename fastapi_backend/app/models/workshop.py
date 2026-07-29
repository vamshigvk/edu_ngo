"""Workshops and panellist sign-ups (Phase 5).

Workshops are run over Zoom/Meet and recorded to YouTube; the recording URL is
surfaced on mentee/mentor dashboards. Mentors sign up to be panellists.
"""
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin
from app.models.enums import WorkshopAudience


class Workshop(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "workshops"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheduled_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    recording_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    audience: Mapped[str] = mapped_column(
        String(20), default=WorkshopAudience.PUBLIC, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    signups = relationship(
        "WorkshopSignup", back_populates="workshop", cascade="all, delete-orphan",
        lazy="selectin",
    )


class WorkshopSignup(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "workshop_signups"

    workshop_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workshops.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    workshop = relationship("Workshop", back_populates="signups")
    user = relationship("User", lazy="selectin")
