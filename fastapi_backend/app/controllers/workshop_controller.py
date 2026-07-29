"""Workshop endpoints (Phase 5).

Mounted at ``/api`` OUTSIDE the admin dependency: any authenticated user can
list workshops, mentors sign up as panellists, admins create/delete.
"""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin, require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.workshop import WorkshopCreate, WorkshopRead
from app.services.workshop_service import workshop_service

router = APIRouter(prefix="/workshops", tags=["Workshops"])


@router.get("", response_model=list[WorkshopRead], summary="List workshops")
async def list_workshops(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return await workshop_service.list_with_counts(db)


@router.post(
    "",
    response_model=WorkshopRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a workshop (admin)",
)
async def create_workshop(
    payload: WorkshopCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    return await workshop_service.create(db, payload.model_dump())


@router.delete(
    "/{workshop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a workshop (admin)",
)
async def delete_workshop(
    workshop_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    await workshop_service.delete(db, workshop_id)


@router.post(
    "/{workshop_id}/signup",
    response_model=MessageResponse,
    summary="Sign up as a workshop panellist (mentor)",
)
async def signup_workshop(
    workshop_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTOR)),
):
    await workshop_service.signup(db, workshop_id, current_user.id)
    return MessageResponse(message="Signed up as a panellist.")
