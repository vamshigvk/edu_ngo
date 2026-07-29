"""Mentor and mentee profile models."""
import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin


class MentorProfile(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "mentor_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    expertise: Mapped[list] = mapped_column(JSON, default=list)
    max_mentees: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    availability: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    languages: Mapped[list] = mapped_column(JSON, default=list)
    # Mentor selection: reviewer confirms study-abroad background (Phase 2).
    studied_abroad: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Broad discipline used by the mapper (Phase 3).
    discipline: Mapped[str | None] = mapped_column(String(120), nullable=True)
    english_support_opt_in: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    user = relationship("User", back_populates="mentor_profile", lazy="selectin")


class MenteeProfile(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "mentee_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    university: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    course: Mapped[str | None] = mapped_column(String(255), nullable=True)
    level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Broad discipline (Phase 3 mapping) + how they are mentored.
    discipline: Mapped[str | None] = mapped_column(String(120), nullable=True)
    mentorship_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    english_support_opt_in: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    cohort_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True
    )

    user = relationship("User", back_populates="mentee_profile", lazy="selectin")
    cohort = relationship("Cohort", back_populates="mentees")
