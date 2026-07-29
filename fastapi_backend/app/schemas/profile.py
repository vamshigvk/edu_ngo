"""Mentor and mentee profile schemas."""
import uuid

from pydantic import BaseModel

from app.models.enums import MentorshipType
from app.schemas.common import ORMModel


# --- Mentor -----------------------------------------------------------------
class MentorProfileBase(BaseModel):
    user_id: uuid.UUID
    expertise: list = []
    max_mentees: int = 1
    availability: str | None = None
    bio: str | None = None
    languages: list = []
    studied_abroad: bool = False
    discipline: str | None = None
    english_support_opt_in: bool = False


class MentorProfileCreate(MentorProfileBase):
    pass


class MentorProfileUpdate(BaseModel):
    expertise: list | None = None
    max_mentees: int | None = None
    availability: str | None = None
    bio: str | None = None
    languages: list | None = None
    studied_abroad: bool | None = None
    discipline: str | None = None
    english_support_opt_in: bool | None = None


class MentorProfileRead(ORMModel, MentorProfileBase):
    id: uuid.UUID
    user_name: str | None = None


# --- Mentee -----------------------------------------------------------------
class MenteeProfileBase(BaseModel):
    user_id: uuid.UUID
    university: str | None = None
    country: str | None = None
    course: str | None = None
    level: str | None = None
    discipline: str | None = None
    mentorship_type: MentorshipType | None = None
    english_support_opt_in: bool = False
    cohort_id: uuid.UUID | None = None


class MenteeProfileCreate(MenteeProfileBase):
    pass


class MenteeProfileUpdate(BaseModel):
    university: str | None = None
    country: str | None = None
    course: str | None = None
    level: str | None = None
    discipline: str | None = None
    mentorship_type: MentorshipType | None = None
    english_support_opt_in: bool | None = None
    cohort_id: uuid.UUID | None = None


class MenteeProfileRead(ORMModel, MenteeProfileBase):
    id: uuid.UUID
    user_name: str | None = None
