"""Application endpoints: CRUD + submit / review workflow + selection funnel."""
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.crud_factory import build_crud_router
from app.core.database import get_db
from app.schemas.application import (
    AdminDecisionRequest,
    ApplicationCreate,
    ApplicationRead,
    ApplicationReviewRequest,
    ApplicationUpdate,
    ReviewBoardRow,
)
from app.schemas.review import ApplicationReviewRead, ReviewerAssignRequest
from app.services.application_workflow import application_workflow_service
from app.services.crud import application_service
from app.services.decision_service import decision_service

router = build_crud_router(
    service=application_service,
    prefix="/applications",
    tag="Applications",
    read_schema=ApplicationRead,
    create_schema=ApplicationCreate,
    update_schema=ApplicationUpdate,
)

# Selection-pipeline routes live on their own router that is mounted BEFORE the
# CRUD router, so the static ``/review-board`` path is matched ahead of the
# CRUD factory's catch-all ``GET /{item_id}``.
selection_router = APIRouter(prefix="/applications", tags=["Applications"])


@selection_router.get(
    "/review-board",
    response_model=list[ReviewBoardRow],
    summary="Enriched applications for the admin review board",
)
async def review_board(
    cohort_id: uuid.UUID | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
):
    return await decision_service.review_board(
        db, cohort_id=cohort_id, status=status_filter
    )


@selection_router.post(
    "/{application_id}/reviewers",
    response_model=list[ApplicationReviewRead],
    status_code=status.HTTP_201_CREATED,
    summary="Assign profile-screening reviewers to an application",
)
async def assign_reviewers(
    application_id: uuid.UUID,
    payload: ReviewerAssignRequest,
    db: AsyncSession = Depends(get_db),
):
    return await decision_service.assign_reviewers(
        db, application_id, payload.reviewer_ids, round=payload.round
    )


@selection_router.post(
    "/{application_id}/system-decision",
    summary="Compute the system (formula) decision from score + reviews",
)
async def system_decision(
    application_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    return await decision_service.compute_system_decision(db, application_id)


@selection_router.post(
    "/{application_id}/admin-decision",
    response_model=ApplicationRead,
    summary="Record the final admin decision (select / waitlist / reject)",
)
async def admin_decision(
    application_id: uuid.UUID,
    payload: AdminDecisionRequest,
    db: AsyncSession = Depends(get_db),
):
    app = await decision_service.admin_decide(
        db, application_id, payload.decision, payload.notes
    )
    application_service._decorate(app)
    return app


@router.post(
    "/{application_id}/submit",
    response_model=ApplicationRead,
    status_code=status.HTTP_200_OK,
    summary="Validate and submit a draft application",
)
async def submit_application(
    application_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    app = await application_workflow_service.validate_and_submit(db, application_id)
    application_service._decorate(app)
    return app


@router.post(
    "/{application_id}/review",
    response_model=ApplicationRead,
    status_code=status.HTTP_200_OK,
    summary="Approve or reject a submitted application",
)
async def review_application(
    application_id: uuid.UUID,
    payload: ApplicationReviewRequest,
    db: AsyncSession = Depends(get_db),
):
    app = await application_workflow_service.review_application(
        db, application_id, approve=payload.approve
    )
    application_service._decorate(app)
    return app
