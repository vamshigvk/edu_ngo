"""Workshop schemas (Phase 5)."""
import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.models.enums import WorkshopAudience
from app.schemas.common import ORMModel


class WorkshopCreate(BaseModel):
    title: str
    description: str | None = None
    scheduled_date: date | None = None
    recording_url: str | None = None
    audience: WorkshopAudience = WorkshopAudience.PUBLIC


class WorkshopRead(ORMModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    scheduled_date: date | None = None
    recording_url: str | None = None
    audience: WorkshopAudience
    signup_count: int = 0
    created_at: datetime


class EnglishSupportRequest(BaseModel):
    opt_in: bool = True
