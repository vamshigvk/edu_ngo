"""FAQ / Noor chatbot schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class FAQBase(BaseModel):
    question: str
    answer: str
    category: str | None = None
    tags: list[str] = Field(default_factory=list)
    is_published: bool = True
    display_order: int = 0


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    is_published: bool | None = None
    display_order: int | None = None


class FAQRead(ORMModel, FAQBase):
    id: uuid.UUID
    created_at: datetime


class FAQBulkImport(BaseModel):
    """Admin bulk ingest — a list of FAQ rows (parsed from CSV/JSON on the client)."""

    items: list[FAQCreate]


class BulkImportResult(BaseModel):
    created: int


# --- Noor chatbot ---------------------------------------------------------
class ChatRequest(BaseModel):
    message: str


class ChatSource(BaseModel):
    question: str
    category: str | None = None


class ChatResponse(BaseModel):
    answer: str
    matched: bool
    sources: list[ChatSource] = Field(default_factory=list)
