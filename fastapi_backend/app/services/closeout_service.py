"""Close-of-programme service (Phase 6): feedback, offers, alumni conversion."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.closeout import OfferRecord, ProgrammeFeedback
from app.models.enums import UserRole
from app.models.profile import MentorProfile
from app.models.user import User


def _decorate(row):
    row.user_name = row.user.full_name if row.user else None
    return row


class CloseoutService:
    async def add_feedback(self, db: AsyncSession, user_id: uuid.UUID, data: dict) -> ProgrammeFeedback:
        fb = ProgrammeFeedback(user_id=user_id, **data)
        db.add(fb)
        await db.commit()
        await db.refresh(fb)
        return _decorate(fb)

    async def add_offer(self, db: AsyncSession, user_id: uuid.UUID, data: dict) -> OfferRecord:
        offer = OfferRecord(user_id=user_id, **data)
        db.add(offer)
        await db.commit()
        await db.refresh(offer)
        return _decorate(offer)

    async def list_feedback(self, db: AsyncSession) -> list[ProgrammeFeedback]:
        rows = (
            await db.execute(select(ProgrammeFeedback).order_by(ProgrammeFeedback.created_at.desc()))
        ).scalars().all()
        return [_decorate(r) for r in rows]

    async def list_offers(self, db: AsyncSession) -> list[OfferRecord]:
        rows = (
            await db.execute(select(OfferRecord).order_by(OfferRecord.created_at.desc()))
        ).scalars().all()
        return [_decorate(r) for r in rows]

    async def become_mentor(self, db: AsyncSession, user: User) -> User:
        """Graduating mentee opts to return as a mentor (alumni)."""
        existing = (
            await db.execute(
                select(MentorProfile).where(MentorProfile.user_id == user.id)
            )
        ).scalar_one_or_none()
        if existing is None:
            db.add(MentorProfile(user_id=user.id, expertise=[], languages=[]))
        user.role = UserRole.MENTOR.value
        user.is_alumni = True
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


closeout_service = CloseoutService()
