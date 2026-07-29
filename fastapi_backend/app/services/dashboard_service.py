"""Dashboard aggregate metrics (employee / mentor / mentee).

Ported from the Django standalone dashboard views using async aggregate queries.
"""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.application import Application
from app.models.checkin import CheckIn
from app.models.cohort import Cohort
from app.models.enums import (
    ApplicationStatus,
    CheckInStatus,
    CohortStatus,
    PairStatus,
)
from app.models.pairing import MentorMenteePair
from app.models.profile import MenteeProfile, MentorProfile
from app.models.user import User

_ACTIVE_PAIR = (PairStatus.ACTIVE, PairStatus.ACCEPTED)


async def _scalar(db: AsyncSession, stmt) -> int:
    return int((await db.execute(stmt)).scalar_one())


async def employee_dashboard(db: AsyncSession) -> dict:
    total_users = await _scalar(db, select(func.count()).select_from(User))
    total_active_cohorts = await _scalar(
        db,
        select(func.count()).select_from(Cohort).where(
            Cohort.status == CohortStatus.ACTIVE
        ),
    )
    total_under_review = await _scalar(
        db,
        select(func.count()).select_from(Application).where(
            Application.status == ApplicationStatus.SUBMITTED
        ),
    )
    total_pairs = await _scalar(db, select(func.count()).select_from(MentorMenteePair))
    completed_checkins = await _scalar(
        db,
        select(func.count()).select_from(CheckIn).where(
            CheckIn.status == CheckInStatus.COMPLETED
        ),
    )

    breakdown_rows = (
        await db.execute(
            select(
                Cohort.id,
                Cohort.name,
                Cohort.status,
                func.count(MentorMenteePair.id).label("total_pairs"),
            )
            .outerjoin(MentorMenteePair, MentorMenteePair.cohort_id == Cohort.id)
            .group_by(Cohort.id, Cohort.name, Cohort.status)
        )
    ).all()

    return {
        "platform_summary": {
            "total_users": total_users,
            "total_active_cohorts": total_active_cohorts,
            "total_applications_under_review": total_under_review,
        },
        "cohort_breakdown": [
            {
                "id": str(row.id),
                "name": row.name,
                "status": row.status,
                "total_pairs": int(row.total_pairs),
            }
            for row in breakdown_rows
        ],
        "system_health": {
            "total_pairings_formed": total_pairs,
            "completed_checkins": completed_checkins,
        },
    }


async def mentor_dashboard(db: AsyncSession, user: User) -> dict:
    """Metrics for the *signed-in* mentor: only their own pairings/check-ins."""
    pairs = (
        await db.execute(
            select(MentorMenteePair)
            .where(MentorMenteePair.mentor_id == user.id)
            .options(selectinload(MentorMenteePair.cohort))
            .order_by(MentorMenteePair.recommended_at.desc())
        )
    ).scalars().all()
    pair_ids = [p.id for p in pairs]

    completed = pending = 0
    if pair_ids:
        completed = await _scalar(
            db,
            select(func.count()).select_from(CheckIn).where(
                CheckIn.pair_id.in_(pair_ids),
                CheckIn.status == CheckInStatus.COMPLETED,
            ),
        )
        pending = await _scalar(
            db,
            select(func.count()).select_from(CheckIn).where(
                CheckIn.pair_id.in_(pair_ids),
                CheckIn.status == CheckInStatus.SCHEDULED,
            ),
        )

    profile = (
        await db.execute(
            select(MentorProfile).where(MentorProfile.user_id == user.id)
        )
    ).scalar_one_or_none()

    mentees = [
        {
            "name": p.mentee.full_name if p.mentee else str(p.mentee_id),
            "email": p.mentee.email if p.mentee else None,
            "status": p.status,
            "match_score": p.match_score,
            "cohort_name": p.cohort.name if p.cohort else None,
        }
        for p in pairs
    ]

    cohorts: dict = {}
    for p in pairs:
        if p.cohort and p.cohort.id not in cohorts:
            cohorts[p.cohort.id] = {
                "name": p.cohort.name,
                "start_date": p.cohort.start_date.isoformat() if p.cohort.start_date else None,
                "end_date": p.cohort.end_date.isoformat() if p.cohort.end_date else None,
                "status": p.cohort.status,
            }

    return {
        "role": "Mentor",
        "profile": None if profile is None else {
            "expertise": profile.expertise or [],
            "languages": profile.languages or [],
            "max_mentees": profile.max_mentees,
            "availability": profile.availability,
            "bio": profile.bio,
            "discipline": profile.discipline,
            "english_support_opt_in": profile.english_support_opt_in,
        },
        "engagement_metrics": {
            "assigned_mentees": len(pairs),
            "active_mentees": sum(1 for p in pairs if p.status in _ACTIVE_PAIR),
            "pending_checkins": pending,
            "completed_checkins": completed,
        },
        "mentees": mentees,
        "assigned_cohorts": list(cohorts.values()),
    }


async def mentee_dashboard(db: AsyncSession, user: User) -> dict:
    """Metrics for the *signed-in* mentee: their own match, check-ins, status."""
    pairs = (
        await db.execute(
            select(MentorMenteePair)
            .where(MentorMenteePair.mentee_id == user.id)
            .options(selectinload(MentorMenteePair.cohort))
            .order_by(MentorMenteePair.recommended_at.desc())
        )
    ).scalars().all()
    # Prefer an active/accepted pairing; otherwise fall back to the latest one.
    pair = next((p for p in pairs if p.status in _ACTIVE_PAIR), pairs[0] if pairs else None)

    mentor_info = None
    checkins: list[dict] = []
    if pair is not None:
        mentor_info = {
            "name": pair.mentor.full_name if pair.mentor else str(pair.mentor_id),
            "email": pair.mentor.email if pair.mentor else None,
            "status": pair.status,
            "match_score": pair.match_score,
            "cohort_name": pair.cohort.name if pair.cohort else None,
        }
        rows = (
            await db.execute(
                select(CheckIn)
                .where(CheckIn.pair_id == pair.id)
                .order_by(CheckIn.sequence_number)
            )
        ).scalars().all()
        checkins = [
            {
                "sequence_number": c.sequence_number,
                "date": c.date.isoformat() if c.date else None,
                "status": c.status,
                "notes": c.notes,
            }
            for c in rows
        ]

    profile = (
        await db.execute(
            select(MenteeProfile).where(MenteeProfile.user_id == user.id)
        )
    ).scalar_one_or_none()

    application_status = (
        await db.execute(
            select(Application.status).where(Application.user_id == user.id)
        )
    ).scalars().first()

    return {
        "role": "Mentee",
        "profile": None if profile is None else {
            "country": profile.country,
            "level": profile.level,
            "university": profile.university,
            "course": profile.course,
            "discipline": profile.discipline,
            "mentorship_type": profile.mentorship_type,
            "english_support_opt_in": profile.english_support_opt_in,
        },
        "my_program_status": {
            "has_active_match": pair is not None and pair.status in _ACTIVE_PAIR,
            "mentor_name": mentor_info["name"] if mentor_info else None,
            "match_status": pair.status if pair else None,
            "application_status": application_status,
            "logged_checkins_count": sum(
                1 for c in checkins if c["status"] == CheckInStatus.COMPLETED
            ),
            "upcoming_checkins_count": sum(
                1 for c in checkins if c["status"] == CheckInStatus.SCHEDULED
            ),
        },
        "mentor": mentor_info,
        "checkins": checkins,
    }
