"""Cohort model."""
from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import CohortStatus


class Cohort(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "cohorts"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    program: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=CohortStatus.UPCOMING, nullable=False
    )
    max_mentees: Mapped[int] = mapped_column(Integer, nullable=False)
    # Minimum disadvantage score for the system to recommend selection.
    selection_threshold: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    mentees = relationship("MenteeProfile", back_populates="cohort")
    form_configs = relationship(
        "ApplicationFormConfig", back_populates="cohort", cascade="all, delete-orphan"
    )
    applications = relationship(
        "Application", back_populates="cohort", cascade="all, delete-orphan"
    )
    scoring_rules = relationship(
        "ScoringRule", back_populates="cohort", cascade="all, delete-orphan"
    )
    matching_rules = relationship(
        "MatchingRule", back_populates="cohort", cascade="all, delete-orphan"
    )
    pairs = relationship(
        "MentorMenteePair", back_populates="cohort", cascade="all, delete-orphan"
    )
