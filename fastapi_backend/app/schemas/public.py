"""Schemas for the unauthenticated public application flow.

These back the website's Apply forms. Unlike the admin ``UserCreate`` surface,
the caller can NOT choose a role — the server pins it to mentee/mentor — so the
public endpoints can never be used to mint an admin account.
"""
import uuid

from pydantic import BaseModel, EmailStr


class PublicMentorApplication(BaseModel):
    full_name: str
    email: EmailStr
    country: str | None = None
    about: str | None = None
    discipline: str | None = None
    studied_abroad: bool = False


class PublicStudentApplication(BaseModel):
    full_name: str
    email: EmailStr
    country: str | None = None
    rural_urban: str | None = None
    education: str | None = None
    score: str | None = None
    gender: str | None = None
    about: str | None = None
    # Answers for the cohort's configured (dynamic) form fields. Merged over the
    # named fields above, so a fully form-driven submission works too.
    answers: dict = {}
    # Optional: pin to a specific cohort; otherwise the first active one is used.
    cohort_id: uuid.UUID | None = None


class PublicApplyResponse(BaseModel):
    detail: str
    user_id: uuid.UUID
