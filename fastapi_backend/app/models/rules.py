"""Scoring and matching rule models."""
import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin


class ScoringRule(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "scoring_rules"

    cohort_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False
    )
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    scoring_logic: Mapped[dict] = mapped_column(JSON, default=dict)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    cohort = relationship("Cohort", back_populates="scoring_rules")
    created_by = relationship("User")


class MatchingRule(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "matching_rules"

    cohort_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False
    )
    criteria_name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    match_logic: Mapped[dict] = mapped_column(JSON, default=dict)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    cohort = relationship("Cohort", back_populates="matching_rules")
    created_by = relationship("User")
