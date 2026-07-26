"""Response schemas for scoring/matching engine actions."""
import uuid

from pydantic import BaseModel


class ScoreRecord(BaseModel):
    application_id: str
    score: float


class ScoringRunResponse(BaseModel):
    cohort_id: uuid.UUID
    applications_processed: int
    scores: list[ScoreRecord]


class MatchingRunResponse(BaseModel):
    status: str = "success"
    cohort_id: uuid.UUID
    pairs_generated: int
    message: str
