"""Scoring engine — evaluates applications against a cohort's scoring rules.

Ported from Django ``ScoringEngineService``. Fix: reads ``scoring_logic``
(the real model field) instead of the non-existent ``criteria`` attribute.
"""
import operator
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import Application
from app.models.enums import ApplicationStatus
from app.models.rules import ScoringRule

_OPERATORS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "contains": lambda container, item: item in container if container else False,
}


class ScoringEngineService:
    def __init__(self, cohort_id: uuid.UUID):
        self.cohort_id = cohort_id

    async def run(self, db: AsyncSession) -> tuple[int, list[dict]]:
        rules = (
            (await db.execute(
                select(ScoringRule).where(ScoringRule.cohort_id == self.cohort_id)
            )).scalars().all()
        )
        applications = (
            (await db.execute(
                select(Application).where(Application.cohort_id == self.cohort_id)
            )).scalars().all()
        )

        processed: list[dict] = []
        for app in applications:
            answers = app.answers if isinstance(app.answers, dict) else {}
            total = 0.0

            for rule in rules:
                logic = rule.scoring_logic if isinstance(rule.scoring_logic, dict) else {}
                target_field = logic.get("field", rule.field_name)
                op_func = _OPERATORS.get(logic.get("operator"))
                threshold = logic.get("value")

                if target_field in answers and op_func is not None:
                    try:
                        if op_func(answers[target_field], threshold):
                            total += float(rule.weight)
                    except (TypeError, ValueError):
                        continue

            app.auto_score = total
            app.final_score = total
            app.disadvantage_score = total
            if app.status == ApplicationStatus.SUBMITTED:
                app.status = ApplicationStatus.SCORED
            db.add(app)
            processed.append({"application_id": str(app.id), "score": total})

        await db.commit()
        return len(processed), processed


async def run_scoring(db: AsyncSession, cohort_id: uuid.UUID) -> tuple[int, list[dict]]:
    return await ScoringEngineService(cohort_id).run(db)
