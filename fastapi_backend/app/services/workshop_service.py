"""Workshop service (Phase 5): CRUD, panellist sign-ups, listing with counts."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.workshop import Workshop, WorkshopSignup


class WorkshopService:
    async def create(self, db: AsyncSession, data: dict) -> Workshop:
        ws = Workshop(**data)
        db.add(ws)
        await db.commit()
        await db.refresh(ws)
        ws.signup_count = 0
        return ws

    async def delete(self, db: AsyncSession, workshop_id: uuid.UUID) -> None:
        ws = await db.get(Workshop, workshop_id)
        if ws is None:
            raise NotFoundError("Workshop not found.")
        await db.delete(ws)
        await db.commit()

    async def list_with_counts(self, db: AsyncSession) -> list[Workshop]:
        rows = (
            await db.execute(select(Workshop).order_by(Workshop.created_at.desc()))
        ).scalars().all()
        for ws in rows:
            ws.signup_count = len(ws.signups)
        return list(rows)

    async def signup(
        self, db: AsyncSession, workshop_id: uuid.UUID, user_id: uuid.UUID
    ) -> WorkshopSignup:
        ws = await db.get(Workshop, workshop_id)
        if ws is None:
            raise NotFoundError("Workshop not found.")
        existing = (
            await db.execute(
                select(WorkshopSignup).where(
                    WorkshopSignup.workshop_id == workshop_id,
                    WorkshopSignup.user_id == user_id,
                )
            )
        ).scalar_one_or_none()
        if existing is not None:
            raise ConflictError("You have already signed up for this workshop.")
        signup = WorkshopSignup(workshop_id=workshop_id, user_id=user_id)
        db.add(signup)
        await db.commit()
        await db.refresh(signup)
        return signup


workshop_service = WorkshopService()
