"""Mentee-mentor mapping endpoints (admin). Part of the admin-guarded /api."""
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.mapping import MappingPairRequest, MenteeTypeRequest
from app.services.mapping_service import mapping_service

router = APIRouter(prefix="/mapping", tags=["Mapping"])


@router.get("/board", summary="Mentees + mentor pool for manual mapping")
async def mapping_board(
    cohort_id: uuid.UUID | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await mapping_service.board(db, cohort_id)


@router.post("/mentee-type", summary="Set a mentee's mentorship type")
async def set_mentee_type(
    payload: MenteeTypeRequest, db: AsyncSession = Depends(get_db)
):
    await mapping_service.set_mentee_type(db, payload.mentee_id, payload.mentorship_type)
    return {"status": "ok", "mentorship_type": payload.mentorship_type}


@router.post(
    "/pair",
    status_code=status.HTTP_201_CREATED,
    summary="Create a one-on-one mentor-mentee pairing",
)
async def create_pair(
    payload: MappingPairRequest, db: AsyncSession = Depends(get_db)
):
    pair = await mapping_service.create_pair(
        db, payload.mentor_id, payload.mentee_id, payload.cohort_id
    )
    return {"pair_id": str(pair.id), "status": pair.status}
