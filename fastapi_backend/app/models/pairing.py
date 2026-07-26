"""Mentor–mentee pairing model."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin
from app.models.enums import PairOutcome, PairStatus


class MentorMenteePair(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "mentor_mentee_pairs"

    mentor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    mentee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    cohort_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30), default=PairStatus.RECOMMENDED, nullable=False
    )
    match_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    recommended_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    accepted_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    outcome: Mapped[str] = mapped_column(
        String(30), default=PairOutcome.PENDING, nullable=False
    )
    outcome_details: Mapped[str | None] = mapped_column(Text, nullable=True)

    mentor = relationship("User", foreign_keys=[mentor_id], lazy="selectin")
    mentee = relationship("User", foreign_keys=[mentee_id], lazy="selectin")
    accepted_by = relationship("User", foreign_keys=[accepted_by_id])
    cohort = relationship("Cohort", back_populates="pairs")
    checkins = relationship(
        "CheckIn", back_populates="pair", cascade="all, delete-orphan"
    )
