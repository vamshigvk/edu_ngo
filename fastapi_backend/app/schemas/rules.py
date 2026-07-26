"""Scoring and matching rule schemas."""
import uuid

from pydantic import BaseModel

from app.schemas.common import ORMModel


# --- Scoring ----------------------------------------------------------------
class ScoringRuleBase(BaseModel):
    cohort_id: uuid.UUID
    field_name: str
    weight: float = 1.0
    scoring_logic: dict = {}
    created_by_id: uuid.UUID | None = None


class ScoringRuleCreate(ScoringRuleBase):
    pass


class ScoringRuleUpdate(BaseModel):
    field_name: str | None = None
    weight: float | None = None
    scoring_logic: dict | None = None


class ScoringRuleRead(ORMModel, ScoringRuleBase):
    id: uuid.UUID


# --- Matching ---------------------------------------------------------------
class MatchingRuleBase(BaseModel):
    cohort_id: uuid.UUID
    criteria_name: str
    weight: float = 1.0
    match_logic: dict = {}
    created_by_id: uuid.UUID | None = None


class MatchingRuleCreate(MatchingRuleBase):
    pass


class MatchingRuleUpdate(BaseModel):
    criteria_name: str | None = None
    weight: float | None = None
    match_logic: dict | None = None


class MatchingRuleRead(ORMModel, MatchingRuleBase):
    id: uuid.UUID
