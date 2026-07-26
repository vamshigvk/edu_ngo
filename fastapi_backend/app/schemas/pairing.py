"""Mentor–mentee pairing schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import PairOutcome, PairStatus
from app.schemas.common import ORMModel


class MentorMenteePairBase(BaseModel):
    mentor_id: uuid.UUID
    mentee_id: uuid.UUID
    cohort_id: uuid.UUID
    status: PairStatus = PairStatus.RECOMMENDED
    match_score: float = 0.0
    accepted_by_id: uuid.UUID | None = None
    accepted_at: datetime | None = None
    rejection_reason: str | None = None
    notes: str | None = None
    outcome: PairOutcome = PairOutcome.PENDING
    outcome_details: str | None = None


class MentorMenteePairCreate(MentorMenteePairBase):
    pass


class MentorMenteePairUpdate(BaseModel):
    status: PairStatus | None = None
    match_score: float | None = None
    accepted_by_id: uuid.UUID | None = None
    accepted_at: datetime | None = None
    rejection_reason: str | None = None
    notes: str | None = None
    outcome: PairOutcome | None = None
    outcome_details: str | None = None


class MentorMenteePairRead(ORMModel, MentorMenteePairBase):
    id: uuid.UUID
    recommended_at: datetime
    mentor_name: str | None = None
    mentee_name: str | None = None
