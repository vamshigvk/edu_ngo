"""Check-in tracking model."""
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin
from app.models.enums import CheckInStatus


class CheckIn(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "checkins"

    pair_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("mentor_mentee_pairs.id", ondelete="CASCADE"), nullable=False
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default=CheckInStatus.SCHEDULED, nullable=False
    )
    action_items: Mapped[list] = mapped_column(JSON, default=list)
    logged_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    next_checkin_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    pair = relationship("MentorMenteePair", back_populates="checkins")
    logged_by = relationship("User")
