"""Mentee-mentor mapping schemas (Phase 3)."""
import uuid

from pydantic import BaseModel

from app.models.enums import MentorshipType


class MenteeTypeRequest(BaseModel):
    mentee_id: uuid.UUID  # mentee's user id
    mentorship_type: MentorshipType


class MappingPairRequest(BaseModel):
    mentor_id: uuid.UUID
    mentee_id: uuid.UUID
    cohort_id: uuid.UUID
