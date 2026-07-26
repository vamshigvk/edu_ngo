"""Application endpoints: CRUD + submit / review workflow actions."""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.crud_factory import build_crud_router
from app.core.database import get_db
from app.schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationReviewRequest,
    ApplicationUpdate,
)
from app.services.application_workflow import application_workflow_service
from app.services.crud import application_service

router = build_crud_router(
    service=application_service,
    prefix="/applications",
    tag="Applications",
    read_schema=ApplicationRead,
    create_schema=ApplicationCreate,
    update_schema=ApplicationUpdate,
)


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
