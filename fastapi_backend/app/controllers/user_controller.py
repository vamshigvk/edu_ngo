"""User endpoints (dedicated service handles password hashing & email uniqueness)."""
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserPage, UserRead, UserUpdate
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=UserPage, summary="List users (search + pagination)")
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: str | None = Query(None, description="Match against name or email."),
    role: str | None = Query(None, description="Filter by role, e.g. mentor/mentee."),
    db: AsyncSession = Depends(get_db),
):
    items = await user_service.list(
        db, skip=skip, limit=limit, search=search, role=role
    )
    total = await user_service.count(db, search=search, role=role)
    return {"items": items, "total": total}


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create(db, payload.model_dump())


@router.get("/{user_id}", response_model=UserRead, summary="Retrieve a user")
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await user_service.get_or_404(db, user_id)


@router.patch("/{user_id}", response_model=UserRead, summary="Update a user")
async def update_user(
    user_id: uuid.UUID, payload: UserUpdate, db: AsyncSession = Depends(get_db)
):
    return await user_service.update(db, user_id, payload.model_dump(exclude_unset=True))


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await user_service.delete(db, user_id)
