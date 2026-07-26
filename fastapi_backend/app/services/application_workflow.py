"""Application lifecycle workflow — submit and review transitions.

Ported from Django ``ApplicationWorkflowService`` with fixes:
- Validates against real ``ApplicationFormConfig`` rows (field_name / is_required)
  filtered by the application's cohort — the Django code referenced non-existent
  ``config.role`` / ``config.schema_fields``.
- Review transitions to ``accepted``/``rejected`` (matching the status enum), not
  the invalid ``approved`` value used in Django.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ValidationError
from app.models.application import Application, ApplicationFormConfig
from app.models.enums import ApplicationStatus


class ApplicationWorkflowService:
    async def validate_and_submit(
        self, db: AsyncSession, application_id: uuid.UUID
    ) -> Application:
        app = await db.get(Application, application_id)
        if app is None:
            raise NotFoundError("Application record not found.")

        if app.status != ApplicationStatus.DRAFT:
            raise ValidationError(
                f"Cannot submit application. Current status is '{app.status}', "
                "expected 'draft'."
            )

        required_fields = (
            (await db.execute(
                select(ApplicationFormConfig.field_name).where(
                    ApplicationFormConfig.cohort_id == app.cohort_id,
                    ApplicationFormConfig.is_required.is_(True),
                )
            )).scalars().all()
        )
        answers = app.answers or {}
        for field_name in required_fields:
            if field_name not in answers:
                raise ValidationError(
                    f"Validation Error: Missing required form response field: "
                    f"'{field_name}'"
                )

        app.status = ApplicationStatus.SUBMITTED
        db.add(app)
        await db.commit()
        await db.refresh(app)
        return app

    async def review_application(
        self, db: AsyncSession, application_id: uuid.UUID, approve: bool = True
    ) -> Application:
        app = await db.get(Application, application_id)
        if app is None:
            raise NotFoundError("Application record not found.")

        if app.status not in (
            ApplicationStatus.SUBMITTED,
            ApplicationStatus.UNDER_REVIEW,
            ApplicationStatus.SCORED,
        ):
            raise ValidationError(
                "Application must be in 'submitted', 'under_review', or 'scored' "
                "status to process a decision."
            )

        app.status = (
            ApplicationStatus.ACCEPTED if approve else ApplicationStatus.REJECTED
        )
        app.reviewed_at = datetime.now(timezone.utc)
        db.add(app)
        await db.commit()
        await db.refresh(app)
        return app


application_workflow_service = ApplicationWorkflowService()
