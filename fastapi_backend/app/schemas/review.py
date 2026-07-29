"""Profile-screening (reviewer) schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import DecisionOutcome
from app.schemas.common import ORMModel


class ReviewerAssignRequest(BaseModel):
    reviewer_ids: list[uuid.UUID]
    round: int = 1


class ReviewSubmitRequest(BaseModel):
    decision: DecisionOutcome
    description: str | None = None


class ApplicationReviewRead(ORMModel):
    id: uuid.UUID
    application_id: uuid.UUID
    reviewer_id: uuid.UUID | None = None
    decision: DecisionOutcome | None = None
    description: str | None = None
    round: int = 1
    submitted_at: datetime | None = None


class AssignedApplicationRead(BaseModel):
    """What a reviewer sees for one of their assigned applications.

    Deliberately excludes other reviewers' decisions and the system/admin
    outcome so screening stays independent.
    """

    review_id: uuid.UUID
    application_id: uuid.UUID
    applicant_name: str | None = None
    disadvantage_score: float = 0.0
    answers: dict = {}
    my_decision: DecisionOutcome | None = None
    my_description: str | None = None
