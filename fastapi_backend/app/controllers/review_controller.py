"""Reviewer endpoints for profile screening.

Mounted at ``/api`` but OUTSIDE the admin-only dependency (like the public
router), so users with the ``reviewer`` role — not just admins — can screen the
applications assigned to them.
"""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_reviewer
from app.models.user import User
from app.schemas.review import (
    ApplicationReviewRead,
    AssignedApplicationRead,
    ReviewSubmitRequest,
)
from app.services.decision_service import decision_service

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get(
    "/assigned",
    response_model=list[AssignedApplicationRead],
    summary="Applications assigned to the current reviewer",
)
async def assigned(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_reviewer),
):
    reviews = await decision_service.list_assigned(db, current_user.id)
    return [
        AssignedApplicationRead(
            review_id=r.id,
            application_id=r.application_id,
            applicant_name=(
                r.application.user.full_name
                if r.application and r.application.user
                else None
            ),
            disadvantage_score=r.application.disadvantage_score if r.application else 0.0,
            answers=r.application.answers if r.application else {},
            my_decision=r.decision,
            my_description=r.description,
        )
        for r in reviews
    ]


@router.post(
    "/{review_id}/submit",
    response_model=ApplicationReviewRead,
    status_code=status.HTTP_200_OK,
    summary="Submit a profile-screening decision",
)
async def submit(
    review_id: uuid.UUID,
    payload: ReviewSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_reviewer),
):
    return await decision_service.submit_review(
        db, review_id, current_user.id, payload.decision, payload.description
    )
