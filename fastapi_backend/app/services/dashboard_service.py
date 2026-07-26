"""Dashboard aggregate metrics (employee / mentor / mentee).

Ported from the Django standalone dashboard views using async aggregate queries.
"""
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import Application
from app.models.checkin import CheckIn
from app.models.cohort import Cohort
from app.models.enums import (
    ApplicationStatus,
    CheckInStatus,
    CohortStatus,
)
from app.models.pairing import MentorMenteePair


async def _scalar(db: AsyncSession, stmt) -> int:
    return int((await db.execute(stmt)).scalar_one())


async def employee_dashboard(db: AsyncSession) -> dict:
    total_users = await _scalar(db, select(func.count()).select_from(_user_table()))
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


async def mentor_dashboard(db: AsyncSession) -> dict:
    active_assigned = await _scalar(
        db, select(func.count()).select_from(MentorMenteePair)
    )
    pending_items = await _scalar(
        db,
        select(func.count()).select_from(CheckIn).where(
            CheckIn.status == CheckInStatus.SCHEDULED
        ),
    )
    cohort_rows = (
        await db.execute(
            select(
                distinct(Cohort.name), Cohort.start_date, Cohort.end_date
            ).join(MentorMenteePair, MentorMenteePair.cohort_id == Cohort.id)
        )
    ).all()

    return {
        "role": "Mentor",
        "engagement_metrics": {
            "active_assigned_mentees": active_assigned,
            "pending_action_items": pending_items,
        },
        "assigned_cohorts": [
            {
                "name": row[0],
                "start_date": row[1].isoformat() if row[1] else None,
                "end_date": row[2].isoformat() if row[2] else None,
            }
            for row in cohort_rows
        ],
    }


async def mentee_dashboard(db: AsyncSession) -> dict:
    has_match = (
        await _scalar(db, select(func.count()).select_from(MentorMenteePair)) > 0
    )
    logged = await _scalar(
        db,
        select(func.count()).select_from(CheckIn).where(
            CheckIn.status == CheckInStatus.COMPLETED
        ),
    )
    return {
        "role": "Mentee",
        "my_program_status": {
            "has_active_match": has_match,
            "logged_checkins_count": logged,
        },
        "available_resources": [
            {"title": "Platform Onboarding Guide", "type": "PDF"},
            {"title": "Setting SMART Goals Document", "type": "Doc"},
        ],
    }


def _user_table():
    # Imported lazily to keep the module import graph flat.
    from app.models.user import User

    return User
