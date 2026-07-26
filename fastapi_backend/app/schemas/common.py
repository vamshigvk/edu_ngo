"""Shared schema base classes."""
from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    """Base for read schemas that are populated from ORM objects."""

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Generic success/status envelope used by action endpoints."""

    status: str = "success"
    message: str
