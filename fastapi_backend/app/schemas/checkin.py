"""Check-in schemas."""
import uuid
# Aliased so the ``date`` *field* name below does not shadow the ``date`` type
# during Pydantic annotation evaluation.
from datetime import date as _date
from datetime import datetime as _datetime

from pydantic import BaseModel

from app.models.enums import CheckInStatus
from app.schemas.common import ORMModel


class CheckInBase(BaseModel):
    pair_id: uuid.UUID
    sequence_number: int
    date: _date
    notes: str | None = None
    status: CheckInStatus = CheckInStatus.SCHEDULED
    action_items: list = []
    logged_by_id: uuid.UUID | None = None
    next_checkin_date: _date | None = None


class CheckInCreate(CheckInBase):
    pass


class CheckInUpdate(BaseModel):
    sequence_number: int | None = None
    date: _date | None = None
    notes: str | None = None
    status: CheckInStatus | None = None
    action_items: list | None = None
    logged_by_id: uuid.UUID | None = None
    next_checkin_date: _date | None = None


class CheckInRead(ORMModel, CheckInBase):
    id: uuid.UUID
    created_at: _datetime
