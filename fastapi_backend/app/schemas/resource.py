"""Learning resource schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import ResourceType
from app.schemas.common import ORMModel


class ResourceBase(BaseModel):
    title: str
    type: ResourceType
    continent: str | None = None
    country: str | None = None
    state: str | None = None
    course: str | None = None
    university: str | None = None
    level: str | None = None
    url: str
    description: str | None = None
    added_by_id: uuid.UUID | None = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    title: str | None = None
    type: ResourceType | None = None
    continent: str | None = None
    country: str | None = None
    state: str | None = None
    course: str | None = None
    university: str | None = None
    level: str | None = None
    url: str | None = None
    description: str | None = None


class ResourceRead(ORMModel, ResourceBase):
    id: uuid.UUID
    created_at: datetime
