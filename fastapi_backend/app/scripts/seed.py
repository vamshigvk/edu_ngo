"""Seed the database with sample cohorts, users, pairings, and check-ins.

Run with:  python -m app.scripts.seed
Creates tables if they do not exist, then populates demo data.
"""
import asyncio
from datetime import date, timedelta

from sqlalchemy import delete, select

from app.core.database import AsyncSessionLocal, Base, engine
from app.core.security import hash_password
from app.models import (  # noqa: F401  (ensure all models are registered)
    CheckIn,
    Cohort,
    MenteeProfile,
    MentorMenteePair,
    MentorProfile,
    User,
)
from app.models.enums import (
    CheckInStatus,
    CohortStatus,
    PairStatus,
    UserRole,
)

USERS = [
    {"full_name": "Admin User", "email": "admin@example.com", "role": UserRole.ADMIN},
    {"full_name": "Rena Reviewer", "email": "reviewer@example.com", "role": UserRole.REVIEWER},
    {"full_name": "Aarav Mehta", "email": "aarav.mehta@example.com", "role": UserRole.MENTEE},
    {"full_name": "Ananya Rao", "email": "ananya.rao@example.com", "role": UserRole.MENTEE},
    {"full_name": "Vikram Singh", "email": "vikram.singh@example.com", "role": UserRole.MENTOR},
    {"full_name": "Priya Sharma", "email": "priya.sharma@example.com", "role": UserRole.MENTOR},
]


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        print("Purging stale demo records...")
        for model in (CheckIn, MentorMenteePair, MenteeProfile, MentorProfile, User, Cohort):
            await db.execute(delete(model))
        await db.commit()

        print("Seeding active cohort...")
        cohort = Cohort(
            name="Global Engineering Mentorship 2026",
            program="Software Development Track",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 1) + timedelta(days=180),
            status=CohortStatus.ACTIVE,
            max_mentees=50,
        )
        db.add(cohort)
        await db.commit()
        await db.refresh(cohort)

        print("Seeding users (mentors & mentees)...")
        users = []
        for u in USERS:
            user = User(
                full_name=u["full_name"],
                email=u["email"],
                role=u["role"],
                hashed_password=hash_password("password123"),
            )
            db.add(user)
            users.append(user)
        await db.commit()
        for user in users:
            await db.refresh(user)

        mentees = [u for u in users if u.role == UserRole.MENTEE]
        mentors = [u for u in users if u.role == UserRole.MENTOR]

        print("Seeding profiles...")
        for m in mentors:
            db.add(MentorProfile(user_id=m.id, expertise=["python", "systems"], max_mentees=3))
        for i, m in enumerate(mentees):
            db.add(
                MenteeProfile(
                    user_id=m.id, university="Sample University", course="python",
                    country="India", level="undergraduate", cohort_id=cohort.id,
                )
            )
        await db.commit()

        print("Seeding pairings...")
        pairs = []
        for index, mentee in enumerate(mentees):
            mentor = mentors[index % len(mentors)]
            pair = MentorMenteePair(
                mentor_id=mentor.id, mentee_id=mentee.id, cohort_id=cohort.id,
                status=PairStatus.ACTIVE, match_score=94.5,
            )
            db.add(pair)
            pairs.append(pair)
        await db.commit()
        for p in pairs:
            await db.refresh(p)

        print("Seeding check-in history...")
        for pair in pairs:
            for seq in range(1, 4):
                db.add(
                    CheckIn(
                        pair_id=pair.id,
                        sequence_number=seq,
                        date=date(2026, 1, 1) + timedelta(days=seq * 7),
                        notes=f"Completed checkpoint #{seq}.",
                        status=CheckInStatus.COMPLETED,
                    )
                )
        await db.commit()

    await engine.dispose()
    print("Seeding complete. Default password for seeded users: 'password123'.")


if __name__ == "__main__":
    asyncio.run(seed())
