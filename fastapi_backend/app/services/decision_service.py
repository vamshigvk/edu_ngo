"""Mentee selection funnel: reviewer assignment, screening, and decisions.

Formula (see Phase 1 plan):
  * ``select``   if disadvantage_score >= cohort.selection_threshold AND the
                 majority of submitted reviewer decisions is ``select``;
  * ``reject``   if below threshold, or the reviewer majority is ``reject``;
  * ``waitlist`` if at/above threshold but reviewers are split/mixed/absent.

``reconciliation_needed`` is True when a clear reviewer majority disagrees with
the system decision — the PDF's trigger for a second-round review.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.application import Application
from app.models.cohort import Cohort
from app.models.enums import ApplicationStatus, DecisionOutcome
from app.models.review import ApplicationReview
from app.services import notification_service

_STATUS_FOR_DECISION = {
    DecisionOutcome.SELECT: ApplicationStatus.ACCEPTED,
    DecisionOutcome.WAITLIST: ApplicationStatus.WAITLISTED,
    DecisionOutcome.REJECT: ApplicationStatus.REJECTED,
}


def evaluate(disadvantage_score: float, threshold: float, reviews) -> dict:
    """Pure decision logic — no DB. ``reviews`` is any iterable with .decision."""
    decisions = [r.decision for r in reviews if r.decision]
    selects = sum(1 for d in decisions if d == DecisionOutcome.SELECT)
    rejects = sum(1 for d in decisions if d == DecisionOutcome.REJECT)
    if selects > rejects:
        majority = DecisionOutcome.SELECT
    elif rejects > selects:
        majority = DecisionOutcome.REJECT
    else:
        majority = None

    meets = disadvantage_score >= threshold
    if not meets:
        system = DecisionOutcome.REJECT
    elif majority == DecisionOutcome.SELECT:
        system = DecisionOutcome.SELECT
    elif majority == DecisionOutcome.REJECT:
        system = DecisionOutcome.REJECT
    else:
        system = DecisionOutcome.WAITLIST

    reconciliation_needed = majority is not None and system != majority
    return {
        "system_decision": system,
        "reviewer_majority": majority,
        "reconciliation_needed": reconciliation_needed,
    }


class DecisionService:
    async def _get_application(self, db: AsyncSession, application_id: uuid.UUID) -> Application:
        app = await db.get(Application, application_id)
        if app is None:
            raise NotFoundError("Application record not found.")
        return app

    async def assign_reviewers(
        self,
        db: AsyncSession,
        application_id: uuid.UUID,
        reviewer_ids: list[uuid.UUID],
        round: int = 1,
    ) -> list[ApplicationReview]:
        app = await self._get_application(db, application_id)
        existing = {
            (r.reviewer_id, r.round)
            for r in (
                await db.execute(
                    select(ApplicationReview).where(
                        ApplicationReview.application_id == application_id
                    )
                )
            ).scalars().all()
        }
        created: list[ApplicationReview] = []
        for reviewer_id in reviewer_ids:
            if (reviewer_id, round) in existing:
                continue
            review = ApplicationReview(
                application_id=application_id, reviewer_id=reviewer_id, round=round
            )
            db.add(review)
            created.append(review)
        if app.status == ApplicationStatus.SUBMITTED:
            app.status = ApplicationStatus.UNDER_REVIEW
            db.add(app)
        await db.commit()
        for r in created:
            await db.refresh(r)
        return created

    async def submit_review(
        self,
        db: AsyncSession,
        review_id: uuid.UUID,
        reviewer_id: uuid.UUID,
        decision: DecisionOutcome,
        description: str | None,
    ) -> ApplicationReview:
        review = await db.get(ApplicationReview, review_id)
        if review is None:
            raise NotFoundError("Review assignment not found.")
        if review.reviewer_id != reviewer_id:
            raise PermissionDeniedError("You can only submit your own review.")
        review.decision = decision.value
        review.description = description
        review.submitted_at = datetime.now(timezone.utc)
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review

    async def compute_system_decision(
        self, db: AsyncSession, application_id: uuid.UUID
    ) -> dict:
        app = await self._get_application(db, application_id)
        cohort = await db.get(Cohort, app.cohort_id)
        threshold = cohort.selection_threshold if cohort else 0.0
        result = evaluate(app.disadvantage_score, threshold, app.reviews)
        app.system_decision = result["system_decision"].value
        db.add(app)
        await db.commit()
        return result

    async def admin_decide(
        self,
        db: AsyncSession,
        application_id: uuid.UUID,
        decision: DecisionOutcome,
        notes: str | None,
    ) -> Application:
        app = await self._get_application(db, application_id)
        app.admin_decision = decision.value
        app.admin_decision_notes = notes
        app.status = _STATUS_FOR_DECISION[decision]
        app.reviewed_at = datetime.now(timezone.utc)
        db.add(app)
        await notification_service.log_decision(
            db, decision=decision, user_id=app.user_id, application_id=app.id
        )
        await db.commit()
        await db.refresh(app)
        return app

    async def list_assigned(
        self, db: AsyncSession, reviewer_id: uuid.UUID
    ) -> list[ApplicationReview]:
        rows = (
            await db.execute(
                select(ApplicationReview)
                .where(ApplicationReview.reviewer_id == reviewer_id)
                .options(selectinload(ApplicationReview.application))
                .order_by(ApplicationReview.created_at.desc())
            )
        ).scalars().all()
        return list(rows)

    async def review_board(
        self,
        db: AsyncSession,
        *,
        cohort_id: uuid.UUID | None = None,
        status: str | None = None,
    ) -> list[dict]:
        stmt = select(Application)
        if cohort_id:
            stmt = stmt.where(Application.cohort_id == cohort_id)
        if status:
            stmt = stmt.where(Application.status == status)
        stmt = stmt.order_by(Application.created_at.desc())
        apps = (await db.execute(stmt)).scalars().all()

        # Threshold per cohort (batch-load the cohorts we touch).
        cohort_ids = {a.cohort_id for a in apps}
        thresholds: dict = {}
        for cid in cohort_ids:
            c = await db.get(Cohort, cid)
            thresholds[cid] = c.selection_threshold if c else 0.0

        rows: list[dict] = []
        for a in apps:
            majority = evaluate(
                a.disadvantage_score, thresholds.get(a.cohort_id, 0.0), a.reviews
            )
            rows.append(
                {
                    "id": a.id,
                    "applicant_name": a.user.full_name if a.user else None,
                    "applicant_email": a.user.email if a.user else None,
                    "status": a.status,
                    "disadvantage_score": a.disadvantage_score,
                    "reviews": [
                        {
                            "reviewer_id": r.reviewer_id,
                            "reviewer_name": r.reviewer.full_name if r.reviewer else None,
                            "decision": r.decision,
                            "description": r.description,
                        }
                        for r in a.reviews
                    ],
                    "system_decision": a.system_decision,
                    "admin_decision": a.admin_decision,
                    "reconciliation_needed": majority["reconciliation_needed"],
                }
            )
        return rows


decision_service = DecisionService()
