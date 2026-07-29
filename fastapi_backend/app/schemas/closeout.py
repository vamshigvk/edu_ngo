"""Close-of-programme schemas (Phase 6): feedback and offer tracking."""
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class FeedbackCreate(BaseModel):
    rating: int = 0
    comments: str | None = None
    cohort_id: uuid.UUID | None = None


class OfferCreate(BaseModel):
    university: str
    status: str = "applied"
    cohort_id: uuid.UUID | None = None


class FeedbackRead(ORMModel):
    id: uuid.UUID
    user_id: uuid.UUID
    cohort_id: uuid.UUID | None = None
    rating: int
    comments: str | None = None
    created_at: datetime
    user_name: str | None = None


class OfferRead(ORMModel):
    id: uuid.UUID
    user_id: uuid.UUID
    cohort_id: uuid.UUID | None = None
    university: str
    status: str
    created_at: datetime
    user_name: str | None = None
