"""Document review portal schemas (Phase 4)."""
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import DocumentStatus
from app.schemas.common import ORMModel


class DocumentCreate(BaseModel):
    title: str
    url: str
    doc_type: str = "cv"
    cohort_id: uuid.UUID | None = None


class DocumentAssignRequest(BaseModel):
    reviewer_id: uuid.UUID


class DocumentReviewRequest(BaseModel):
    feedback: str


class DocumentRead(ORMModel):
    id: uuid.UUID
    user_id: uuid.UUID
    cohort_id: uuid.UUID | None = None
    doc_type: str
    title: str
    url: str
    status: DocumentStatus
    reviewer_id: uuid.UUID | None = None
    feedback: str | None = None
    created_at: datetime
    # Derived, populated in the controller for display.
    applicant_name: str | None = None
    reviewer_name: str | None = None
