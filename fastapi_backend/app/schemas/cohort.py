"""Cohort schemas."""
import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.models.enums import CohortStatus
from app.schemas.common import ORMModel


class CohortBase(BaseModel):
    name: str
    program: str
    start_date: date
    end_date: date
    status: CohortStatus = CohortStatus.UPCOMING
    max_mentees: int


class CohortCreate(CohortBase):
    pass


class CohortUpdate(BaseModel):
    name: str | None = None
    program: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: CohortStatus | None = None
    max_mentees: int | None = None


class CohortRead(ORMModel, CohortBase):
    id: uuid.UUID
    created_at: datetime
