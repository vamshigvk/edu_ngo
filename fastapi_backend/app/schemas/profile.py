"""Mentor and mentee profile schemas."""
import uuid

from pydantic import BaseModel

from app.schemas.common import ORMModel


# --- Mentor -----------------------------------------------------------------
class MentorProfileBase(BaseModel):
    user_id: uuid.UUID
    expertise: list = []
    max_mentees: int = 1
    availability: str | None = None
    bio: str | None = None
    languages: list = []


class MentorProfileCreate(MentorProfileBase):
    pass


class MentorProfileUpdate(BaseModel):
    expertise: list | None = None
    max_mentees: int | None = None
    availability: str | None = None
    bio: str | None = None
    languages: list | None = None


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
    cohort_id: uuid.UUID | None = None


class MenteeProfileCreate(MenteeProfileBase):
    pass


class MenteeProfileUpdate(BaseModel):
    university: str | None = None
    country: str | None = None
    course: str | None = None
    level: str | None = None
    cohort_id: uuid.UUID | None = None


class MenteeProfileRead(ORMModel, MenteeProfileBase):
    id: uuid.UUID
    user_name: str | None = None
