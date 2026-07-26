"""Application form config and application schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import ApplicationPurpose, ApplicationStatus, FieldType
from app.schemas.common import ORMModel


# --- Form config ------------------------------------------------------------
class ApplicationFormConfigBase(BaseModel):
    cohort_id: uuid.UUID
    field_name: str
    field_type: FieldType
    is_required: bool = False
    field_order: int = 0
    options: list = []
    validation_rules: dict = {}


class ApplicationFormConfigCreate(ApplicationFormConfigBase):
    pass


class ApplicationFormConfigUpdate(BaseModel):
    field_name: str | None = None
    field_type: FieldType | None = None
    is_required: bool | None = None
    field_order: int | None = None
    options: list | None = None
    validation_rules: dict | None = None


class ApplicationFormConfigRead(ORMModel, ApplicationFormConfigBase):
    id: uuid.UUID


# --- Application ------------------------------------------------------------
class ApplicationBase(BaseModel):
    user_id: uuid.UUID
    cohort_id: uuid.UUID
    status: ApplicationStatus = ApplicationStatus.DRAFT
    answers: dict = {}
    purpose: ApplicationPurpose = ApplicationPurpose.OTHER


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus | None = None
    answers: dict | None = None
    purpose: ApplicationPurpose | None = None
    auto_score: float | None = None
    final_score: float | None = None


class ApplicationRead(ORMModel, ApplicationBase):
    id: uuid.UUID
    auto_score: float = 0.0
    final_score: float = 0.0
    reviewed_at: datetime | None = None
    user_name: str | None = None


class ApplicationReviewRequest(BaseModel):
    approve: bool = True
