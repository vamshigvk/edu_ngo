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
    FAQ,
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

# Starter knowledge base for the Noor chatbot + FAQ page. Mirrors Noor's
# suggested prompts on projecteduaccess.com plus the most common questions.
FAQS = [
    {
        "question": "I want to study abroad",
        "answer": (
            "Great! Project EduAccess offers free, personalised 1:1 mentorship to help "
            "learners from marginalised communities apply to universities abroad for "
            "postgraduate study (masters and PhD). Head to the Apply page to apply as a "
            "mentee, or explore the India Graduate Mentorship Programme to learn more."
        ),
        "category": "Getting started",
        "tags": ["study", "abroad", "mentee", "apply"],
        "display_order": 1,
    },
    {
        "question": "Tell me about the Graduate Mentorship Programme",
        "answer": (
            "The India Graduate Mentorship Programme (IGMP) helps Indian learners from "
            "marginalised communities apply to universities abroad for graduate studies. "
            "Mentees get personalised 1:1 mentorship on university and scholarship "
            "applications, mentee-only workshops, interview and English-language support, "
            "and affinity-based support. It is completely free of cost."
        ),
        "category": "Programmes",
        "tags": ["graduate", "mentorship", "programme", "igmp"],
        "display_order": 2,
    },
    {
        "question": "Tell me about your Fellowships",
        "answer": (
            "In India we run the PRISM Fellowship at NCBS and the PRISM National "
            "Fellowship — fully-funded, residential research programmes promoting Research "
            "& Inclusion in STEM for life-science students from disadvantaged backgrounds. "
            "See Our Work → India for details."
        ),
        "category": "Programmes",
        "tags": ["fellowship", "prism", "research", "stem"],
        "display_order": 3,
    },
    {
        "question": "Workshops & resources",
        "answer": (
            "We regularly organise public workshops on scholarships and university "
            "applications, and publish guides and recordings. Visit the Resources page for "
            "Guides on Application Documents, recordings from online workshops, and the "
            "Kashmir University workshop material."
        ),
        "category": "Resources",
        "tags": ["workshops", "resources", "guides", "recordings"],
        "display_order": 4,
    },
    {
        "question": "Tell me about Guides on Application Documents",
        "answer": (
            "Our Guides on Application Documents series covers writing your CV, drafting "
            "personal statements and statements of purpose, writing research proposals, and "
            "references/LoRs. Find them under Resources → Guides on Application Documents."
        ),
        "category": "Resources",
        "tags": ["guides", "cv", "sop", "personal statement", "documents"],
        "display_order": 5,
    },
    {
        "question": "Is the mentorship free?",
        "answer": (
            "Yes — Project EduAccess mentorship is completely free of cost. If anyone asks "
            "you to pay a fee claiming to be associated with us, please report it to "
            "info@projecteduaccess.com."
        ),
        "category": "General",
        "tags": ["free", "cost", "fee"],
        "display_order": 6,
    },
    {
        "question": "Who is eligible to apply as a mentee?",
        "answer": (
            "You can apply if you have completed (or are in the final year of) an "
            "undergraduate degree in India, plan to apply for a postgraduate degree "
            "abroad, and are disadvantaged by social position, economic ability and/or "
            "geography."
        ),
        "category": "Applications",
        "tags": ["eligibility", "eligible", "mentee", "apply"],
        "display_order": 7,
    },
    {
        "question": "How do I become a mentor?",
        "answer": (
            "We welcome mentors who have pursued or are pursuing graduate studies abroad. "
            "Applications are accepted on a rolling basis — use the 'Become a mentor' option "
            "on the Apply page to sign up."
        ),
        "category": "Applications",
        "tags": ["mentor", "volunteer", "become"],
        "display_order": 8,
    },
]

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
        for model in (CheckIn, MentorMenteePair, MenteeProfile, MentorProfile, User, Cohort, FAQ):
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

        print("Seeding FAQs (Noor knowledge base)...")
        for f in FAQS:
            db.add(FAQ(**f))
        await db.commit()

    await engine.dispose()
    print("Seeding complete. Default password for seeded users: 'password123'.")


if __name__ == "__main__":
    asyncio.run(seed())
