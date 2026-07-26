"""Matching engine — scores mentor/mentee pairs and generates recommendations.

Ported from Django ``MatchingEngineService`` using explicit async queries.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.cohort import Cohort
from app.models.enums import PairStatus
from app.models.pairing import MentorMenteePair
from app.models.profile import MenteeProfile, MentorProfile
from app.models.rules import MatchingRule
from app.models.user import User


class MatchingEngineService:
    def __init__(self, cohort_id: uuid.UUID):
        self.cohort_id = cohort_id

    def calculate_match_score(
        self, rules: list[MatchingRule], mentor: MentorProfile, mentee: MenteeProfile
    ) -> float:
        if not rules:
            return 50.0

        total_weight = 0.0
        earned = 0.0
        for rule in rules:
            weight = rule.weight
            total_weight += weight
            logic = rule.match_logic if isinstance(rule.match_logic, dict) else {}
            rule_type = logic.get("type")

            if rule_type == "array_intersection":
                mentor_vals = getattr(mentor, logic.get("mentor_field", ""), None) or []
                mentee_val = getattr(mentee, logic.get("mentee_field", ""), None)
                if isinstance(mentor_vals, list) and mentee_val in mentor_vals:
                    earned += weight
            elif rule_type == "exact_match":
                m_val = getattr(mentor, logic.get("mentor_field", ""), None)
                e_val = getattr(mentee, logic.get("mentee_field", ""), None)
                if m_val and e_val and m_val == e_val:
                    earned += weight

        if total_weight == 0:
            return 50.0
        return round((earned / total_weight) * 100, 2)

    async def generate_pairings(self, db: AsyncSession) -> int:
        cohort = await db.get(Cohort, self.cohort_id)
        if cohort is None:
            raise NotFoundError(f"Cohort '{self.cohort_id}' not found.")

        rules = list(
            (await db.execute(
                select(MatchingRule).where(MatchingRule.cohort_id == self.cohort_id)
            )).scalars().all()
        )
        mentees = list(
            (await db.execute(
                select(MenteeProfile).where(MenteeProfile.cohort_id == self.cohort_id)
            )).scalars().all()
        )
        mentors = list(
            (await db.execute(
                select(MentorProfile)
                .join(User, MentorProfile.user_id == User.id)
                .where(User.is_active.is_(True))
            )).scalars().all()
        )
        existing = set(
            (await db.execute(
                select(MentorMenteePair.mentor_id, MentorMenteePair.mentee_id).where(
                    MentorMenteePair.cohort_id == self.cohort_id
                )
            )).all()
        )

        created = 0
        for mentee in mentees:
            for mentor in mentors:
                if (mentor.user_id, mentee.user_id) in existing:
                    continue
                score = self.calculate_match_score(rules, mentor, mentee)
                db.add(
                    MentorMenteePair(
                        mentor_id=mentor.user_id,
                        mentee_id=mentee.user_id,
                        cohort_id=self.cohort_id,
                        status=PairStatus.RECOMMENDED,
                        match_score=score,
                    )
                )
                existing.add((mentor.user_id, mentee.user_id))
                created += 1

        await db.commit()
        return created


async def generate_pairings(db: AsyncSession, cohort_id: uuid.UUID) -> int:
    return await MatchingEngineService(cohort_id).generate_pairings(db)
