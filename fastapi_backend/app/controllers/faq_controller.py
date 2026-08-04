"""Admin FAQ management (mounted under the admin-guarded /api namespace).

CRUD plus a bulk-import endpoint so admins can ingest many Q&A rows at once
(the client parses CSV/JSON into `items`). The public read + chatbot endpoints
live in ``public_controller`` so anonymous visitors can reach them.
"""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.faq import FAQ
from app.schemas.faq import (
    BulkImportResult,
    FAQBulkImport,
    FAQCreate,
    FAQRead,
    FAQUpdate,
)
from app.services.crud import faq_service

router = APIRouter(prefix="/faqs", tags=["FAQs"])


@router.get("", response_model=list[FAQRead], summary="List all FAQs (admin)")
async def list_faqs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FAQ).order_by(FAQ.display_order, FAQ.created_at))
    return list(result.scalars().all())


@router.post(
    "",
    response_model=FAQRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a FAQ",
)
async def create_faq(payload: FAQCreate, db: AsyncSession = Depends(get_db)):
    return await faq_service.create(db, payload.model_dump())


@router.post(
    "/bulk-import",
    response_model=BulkImportResult,
    status_code=status.HTTP_201_CREATED,
    summary="Bulk-import FAQs (ingest many Q&A rows)",
)
async def bulk_import(payload: FAQBulkImport, db: AsyncSession = Depends(get_db)):
    count = 0
    for item in payload.items:
        await faq_service.create(db, item.model_dump())
        count += 1
    return BulkImportResult(created=count)


@router.patch("/{faq_id}", response_model=FAQRead, summary="Update a FAQ")
async def update_faq(
    faq_id: uuid.UUID, payload: FAQUpdate, db: AsyncSession = Depends(get_db)
):
    return await faq_service.update(db, faq_id, payload.model_dump(exclude_unset=True))


@router.delete(
    "/{faq_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a FAQ",
)
async def delete_faq(faq_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await faq_service.delete(db, faq_id)
