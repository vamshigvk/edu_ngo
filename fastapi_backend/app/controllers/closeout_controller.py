"""Close-of-programme endpoints (Phase 6).

Mounted at ``/api`` OUTSIDE the admin dependency: mentees submit feedback/offers
and can opt to return as a mentor; admins read the submissions.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_admin, require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.closeout import (
    FeedbackCreate,
    FeedbackRead,
    OfferCreate,
    OfferRead,
)
from app.schemas.user import UserRead
from app.services.closeout_service import closeout_service

router = APIRouter(prefix="/closeout", tags=["Close of Programme"])


@router.post(
    "/feedback",
    response_model=FeedbackRead,
    status_code=status.HTTP_201_CREATED,
    summary="Submit programme feedback (mentee)",
)
async def submit_feedback(
    payload: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTEE)),
):
    return await closeout_service.add_feedback(db, current_user.id, payload.model_dump())


@router.post(
    "/offers",
    response_model=OfferRead,
    status_code=status.HTTP_201_CREATED,
    summary="Submit an offer / impact record (mentee)",
)
async def submit_offer(
    payload: OfferCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTEE)),
):
    return await closeout_service.add_offer(db, current_user.id, payload.model_dump())


@router.post(
    "/become-mentor",
    response_model=UserRead,
    summary="Return to the programme as a mentor (mentee alumni)",
)
async def become_mentor(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTEE)),
):
    return await closeout_service.become_mentor(db, current_user)


@router.get(
    "/feedback",
    response_model=list[FeedbackRead],
    summary="All programme feedback (admin)",
)
async def list_feedback(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    return await closeout_service.list_feedback(db)


@router.get(
    "/offers",
    response_model=list[OfferRead],
    summary="All offer records (admin)",
)
async def list_offers(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    return await closeout_service.list_offers(db)
