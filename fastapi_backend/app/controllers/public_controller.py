"""Public (unauthenticated) endpoints for the marketing site.

Deliberately open — these are the ONLY write paths reachable without a token:
  * ``POST /api/public/apply/mentor``  — mentor sign-up (rolling basis)
  * ``POST /api/public/apply/student`` — mentee application (create → submit)
plus read-only ``GET /api/public/cohorts`` and ``GET /api/public/resources``
that the public pages render.

Everything else under ``/api`` requires an authenticated admin (see main.py).
The role is forced server-side, so this surface can never create an admin.
"""
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import ValidationError
from app.models.application import ApplicationFormConfig
from app.models.cohort import Cohort
from app.models.faq import FAQ
from app.models.enums import (
    ApplicationPurpose,
    ApplicationStatus,
    CohortStatus,
    UserRole,
)
from app.schemas.application import FormFieldRead
from app.schemas.cohort import CohortRead
from app.schemas.faq import ChatRequest, ChatResponse, FAQRead
from app.schemas.public import (
    PublicApplyResponse,
    PublicMentorApplication,
    PublicStudentApplication,
)
from app.schemas.resource import ResourceRead
from app.services import chat_service
from app.services.application_workflow import application_workflow_service
from app.services.crud import (
    application_service,
    mentee_profile_service,
    mentor_profile_service,
    resource_service,
)
from app.services.user_service import user_service

router = APIRouter(prefix="/public", tags=["Public"])


@router.get(
    "/cohorts",
    response_model=list[CohortRead],
    summary="List active cohorts (public)",
)
async def public_cohorts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Cohort)
        .where(Cohort.status == CohortStatus.ACTIVE)
        .order_by(Cohort.created_at.desc())
    )
    return list(result.scalars().all())


@router.get(
    "/cohorts/{cohort_id}/form",
    response_model=list[FormFieldRead],
    summary="Application-form fields for a cohort (public, dynamic form)",
)
async def public_cohort_form(
    cohort_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ApplicationFormConfig)
        .where(ApplicationFormConfig.cohort_id == cohort_id)
        .order_by(ApplicationFormConfig.field_order)
    )
    return list(result.scalars().all())


@router.get(
    "/resources",
    response_model=list[ResourceRead],
    summary="List learning resources (public)",
)
async def public_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    return await resource_service.list(db, skip=skip, limit=limit)


@router.get(
    "/faqs",
    response_model=list[FAQRead],
    summary="List published FAQs (public)",
)
async def public_faqs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FAQ)
        .where(FAQ.is_published.is_(True))
        .order_by(FAQ.display_order, FAQ.created_at)
    )
    return list(result.scalars().all())


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Ask Noor (FAQ-grounded chatbot)",
)
async def chat(payload: ChatRequest, db: AsyncSession = Depends(get_db)):
    return await chat_service.answer_query(db, payload.message)


@router.post(
    "/apply/mentor",
    response_model=PublicApplyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Public mentor sign-up",
)
async def apply_mentor(
    payload: PublicMentorApplication, db: AsyncSession = Depends(get_db)
):
    user = await user_service.create(
        db,
        {
            "email": payload.email,
            "full_name": payload.full_name,
            "role": UserRole.MENTOR.value,  # forced — cannot be overridden
        },
    )
    about = payload.about or ""
    bio = f"{about}\n\nCountry: {payload.country}" if payload.country else about
    await mentor_profile_service.create(
        db,
        {
            "user_id": user.id,
            "bio": bio,
            "expertise": [],
            "languages": [],
            "discipline": payload.discipline,
            "studied_abroad": payload.studied_abroad,
        },
    )
    return PublicApplyResponse(detail="Mentor application received.", user_id=user.id)


@router.post(
    "/apply/student",
    response_model=PublicApplyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Public mentee application",
)
async def apply_student(
    payload: PublicStudentApplication, db: AsyncSession = Depends(get_db)
):
    cohort_id = payload.cohort_id
    if cohort_id is None:
        result = await db.execute(
            select(Cohort)
            .where(Cohort.status == CohortStatus.ACTIVE)
            .order_by(Cohort.created_at.desc())
        )
        cohort = result.scalars().first()
        if cohort is None:
            raise ValidationError("No cohort is currently open for applications.")
        cohort_id = cohort.id

    user = await user_service.create(
        db,
        {
            "email": payload.email,
            "full_name": payload.full_name,
            "role": UserRole.MENTEE.value,  # forced — cannot be overridden
        },
    )
    await mentee_profile_service.create(
        db,
        {
            "user_id": user.id,
            "country": payload.country,
            "level": payload.education,
            "cohort_id": cohort_id,
        },
    )
    # Named fields first, then any dynamic form answers (which win on conflict).
    answers = {
        "rural_urban": payload.rural_urban,
        "highest_education": payload.education,
        "score": payload.score,
        "gender": payload.gender,
        "about": payload.about,
        **(payload.answers or {}),
    }
    application = await application_service.create(
        db,
        {
            "user_id": user.id,
            "cohort_id": cohort_id,
            "purpose": ApplicationPurpose.SKILL_BUILDING.value,
            "status": ApplicationStatus.DRAFT.value,
            "answers": answers,
        },
    )
    await application_workflow_service.validate_and_submit(db, application.id)
    return PublicApplyResponse(
        detail="Application received.", user_id=user.id
    )
