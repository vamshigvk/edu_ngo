"""Document review portal endpoints (Phase 4).

Mounted at ``/api`` OUTSIDE the admin dependency: mentees upload, mentors review,
admins assign — each endpoint carries its own role guard.
"""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_admin, require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.document import (
    DocumentAssignRequest,
    DocumentCreate,
    DocumentRead,
    DocumentReviewRequest,
)
from app.services.document_service import document_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Upload an application document (mentee)",
)
async def upload_document(
    payload: DocumentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTEE)),
):
    return await document_service.create(db, current_user.id, payload.model_dump())


@router.get(
    "/mine",
    response_model=list[DocumentRead],
    summary="My uploaded documents (mentee)",
)
async def my_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTEE)),
):
    return await document_service.list_by_user(db, current_user.id)


@router.get(
    "/assigned",
    response_model=list[DocumentRead],
    summary="Documents assigned to me for review (mentor)",
)
async def assigned_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTOR)),
):
    return await document_service.list_assigned(db, current_user.id)


@router.post(
    "/{document_id}/review",
    response_model=DocumentRead,
    summary="Submit review feedback for a document (mentor)",
)
async def review_document(
    document_id: uuid.UUID,
    payload: DocumentReviewRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTOR)),
):
    return await document_service.review(db, document_id, current_user.id, payload.feedback)


@router.get(
    "",
    response_model=list[DocumentRead],
    summary="All documents (admin)",
)
async def all_documents(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    return await document_service.list_all(db)


@router.post(
    "/{document_id}/assign",
    response_model=DocumentRead,
    summary="Assign a reviewer to a document (admin)",
)
async def assign_document(
    document_id: uuid.UUID,
    payload: DocumentAssignRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    return await document_service.assign(db, document_id, payload.reviewer_id)
