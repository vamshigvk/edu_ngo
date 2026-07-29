"""Stubbed notification service — the PDF's "Mail Merge", minus the email.

Instead of sending, it appends a ``NotificationLog`` row. When a real provider
is wired up, only ``send`` changes; callers stay the same.
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import DecisionOutcome
from app.models.notification import NotificationLog

# template key -> (subject, body) for selection-decision emails.
_TEMPLATES = {
    DecisionOutcome.SELECT: (
        "SELECTION",
        "Congratulations — you have been selected",
        "You have been selected for the mentorship programme. Please complete "
        "your onboarding and submit your declaration to confirm participation.",
    ),
    DecisionOutcome.WAITLIST: (
        "WAITLIST",
        "Your application has been waitlisted",
        "Your application is strong but the current cohort is full. You have "
        "been placed on the waitlist and we will be in touch if a place opens.",
    ),
    DecisionOutcome.REJECT: (
        "REJECTION",
        "Update on your mentorship application",
        "Thank you for applying. After review we are unable to offer you a place "
        "in this cohort. We encourage you to reapply in a future cycle.",
    ),
}


async def log(
    db: AsyncSession,
    *,
    template: str,
    subject: str,
    body: str,
    user_id: uuid.UUID | None = None,
    application_id: uuid.UUID | None = None,
) -> NotificationLog:
    entry = NotificationLog(
        user_id=user_id,
        application_id=application_id,
        template=template,
        subject=subject,
        body=body,
    )
    db.add(entry)
    await db.flush()
    return entry


async def log_decision(
    db: AsyncSession,
    *,
    decision: DecisionOutcome,
    user_id: uuid.UUID | None,
    application_id: uuid.UUID,
) -> NotificationLog:
    template, subject, body = _TEMPLATES[decision]
    return await log(
        db,
        template=template,
        subject=subject,
        body=body,
        user_id=user_id,
        application_id=application_id,
    )
