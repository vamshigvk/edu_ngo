"""Cohort endpoints: CRUD + scoring/matching engine actions."""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.crud_factory import build_crud_router
from app.core.database import get_db
from app.models.application import ApplicationFormConfig
from app.schemas.application import ApplicationFormConfigRead
from app.schemas.cohort import CohortCreate, CohortRead, CohortUpdate
from app.schemas.engine import MatchingRunResponse, ScoringRunResponse
from app.services.crud import cohort_service
from app.services.matching_service import generate_pairings
from app.services.scoring_service import run_scoring

router = build_crud_router(
    service=cohort_service,
    prefix="/cohorts",
    tag="Cohorts",
    read_schema=CohortRead,
    create_schema=CohortCreate,
    update_schema=CohortUpdate,
)


@router.get(
    "/{cohort_id}/form-configs",
    response_model=list[ApplicationFormConfigRead],
    summary="List a cohort's application-form fields (ordered)",
)
async def cohort_form_configs(
    cohort_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ApplicationFormConfig)
        .where(ApplicationFormConfig.cohort_id == cohort_id)
        .order_by(ApplicationFormConfig.field_order)
    )
    return list(result.scalars().all())


@router.post(
    "/{cohort_id}/scoring/run",
    response_model=ScoringRunResponse,
    status_code=status.HTTP_200_OK,
    summary="Run the scoring engine for a cohort",
)
async def run_scoring_engine(
    cohort_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    # Ensure the cohort exists (raises 404 otherwise).
    await cohort_service.get_or_404(db, cohort_id)
    count, scores = await run_scoring(db, cohort_id)
    return ScoringRunResponse(
        cohort_id=cohort_id, applications_processed=count, scores=scores
    )


@router.post(
    "/{cohort_id}/matching/run",
    response_model=MatchingRunResponse,
    status_code=status.HTTP_200_OK,
    summary="Run the matching engine for a cohort",
)
async def run_matching_engine(
    cohort_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    pairs = await generate_pairings(db, cohort_id)
    return MatchingRunResponse(
        cohort_id=cohort_id,
        pairs_generated=pairs,
        message=f"Generated {pairs} candidate recommendations.",
    )
