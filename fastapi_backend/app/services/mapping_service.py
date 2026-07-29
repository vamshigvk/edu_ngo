"""Mentee-mentor mapping (Phase 3).

Supports the PDF's manual "mapper": lists mentees and the mentor pool (with
discipline + remaining capacity), suggests same-discipline mentors, assigns a
mentorship type (one-on-one vs cohort), and records a one-on-one pairing.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models.application import Application
from app.models.enums import MentorshipType, PairStatus
from app.models.pairing import MentorMenteePair
from app.models.profile import MenteeProfile, MentorProfile


class MappingService:
    async def board(self, db: AsyncSession, cohort_id: uuid.UUID | None = None) -> dict:
        mstmt = select(MenteeProfile).options(selectinload(MenteeProfile.user))
        if cohort_id:
            mstmt = mstmt.where(MenteeProfile.cohort_id == cohort_id)
        mentees = (await db.execute(mstmt)).scalars().all()

        mentors = (
            await db.execute(
                select(MentorProfile).options(selectinload(MentorProfile.user))
            )
        ).scalars().all()

        pstmt = select(MentorMenteePair)
        if cohort_id:
            pstmt = pstmt.where(MentorMenteePair.cohort_id == cohort_id)
        pairs = (await db.execute(pstmt)).scalars().all()

        load: dict = {}
        mentee_mentor: dict = {}
        for p in pairs:
            load[p.mentor_id] = load.get(p.mentor_id, 0) + 1
            mentee_mentor.setdefault(p.mentee_id, p.mentor_id)

        # Best disadvantage score per mentee (from their applications).
        scores: dict = {}
        mentee_ids = [m.user_id for m in mentees]
        if mentee_ids:
            rows = (
                await db.execute(
                    select(Application.user_id, Application.disadvantage_score).where(
                        Application.user_id.in_(mentee_ids)
                    )
                )
            ).all()
            for uid, sc in rows:
                scores[uid] = max(scores.get(uid, 0.0), sc or 0.0)

        mentors_out = [
            {
                "user_id": str(m.user_id),
                "name": m.user.full_name if m.user else None,
                "discipline": m.discipline,
                "max_mentees": m.max_mentees,
                "assigned": load.get(m.user_id, 0),
                "studied_abroad": m.studied_abroad,
                "availability": m.availability,
            }
            for m in mentors
        ]
        mentor_name = {m["user_id"]: m["name"] for m in mentors_out}

        def suggestions(discipline: str | None) -> list[str]:
            if not discipline:
                return []
            d = discipline.lower()
            return [
                m["user_id"] for m in mentors_out
                if m["discipline"] and m["discipline"].lower() == d
                and m["assigned"] < m["max_mentees"]
            ]

        mentees_out = []
        for m in mentees:
            cur = mentee_mentor.get(m.user_id)
            mentees_out.append({
                "user_id": str(m.user_id),
                "name": m.user.full_name if m.user else None,
                "discipline": m.discipline,
                "cohort_id": str(m.cohort_id) if m.cohort_id else None,
                "disadvantage_score": scores.get(m.user_id, 0.0),
                "mentorship_type": m.mentorship_type,
                "current_mentor_id": str(cur) if cur else None,
                "current_mentor_name": mentor_name.get(str(cur)) if cur else None,
                "suggested_mentor_ids": suggestions(m.discipline),
            })

        return {"mentees": mentees_out, "mentors": mentors_out}

    async def _mentee_profile(self, db: AsyncSession, user_id: uuid.UUID) -> MenteeProfile:
        profile = (
            await db.execute(
                select(MenteeProfile).where(MenteeProfile.user_id == user_id)
            )
        ).scalar_one_or_none()
        if profile is None:
            raise NotFoundError("Mentee profile not found.")
        return profile

    async def set_mentee_type(
        self, db: AsyncSession, mentee_user_id: uuid.UUID, mentorship_type: MentorshipType
    ) -> MenteeProfile:
        profile = await self._mentee_profile(db, mentee_user_id)
        profile.mentorship_type = mentorship_type.value
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile

    async def create_pair(
        self,
        db: AsyncSession,
        mentor_id: uuid.UUID,
        mentee_id: uuid.UUID,
        cohort_id: uuid.UUID,
    ) -> MentorMenteePair:
        pair = MentorMenteePair(
            mentor_id=mentor_id, mentee_id=mentee_id, cohort_id=cohort_id,
            status=PairStatus.ACTIVE,
        )
        db.add(pair)
        profile = await self._mentee_profile(db, mentee_id)
        profile.mentorship_type = MentorshipType.ONE_ON_ONE.value
        db.add(profile)
        await db.commit()
        await db.refresh(pair)
        return pair


mapping_service = MappingService()
