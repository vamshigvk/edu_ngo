"""Email notifications for the application workflow.

Each notification is persisted in the database and, when SMTP is configured,
will also be delivered to the recipient via email.
"""
import smtplib
import uuid
from email.message import EmailMessage

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.enums import DecisionOutcome
from app.models.notification import NotificationLog
from app.models.user import User

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


async def _resolve_recipient_email(db: AsyncSession, user_id: uuid.UUID | None) -> str | None:
    if not user_id:
        return None
    user = await db.get(User, user_id)
    return user.email if user else None


async def _deliver_via_smtp(*, recipient: str, subject: str, body: str) -> bool:
    if not settings.smtp_host:
        return False

    message = EmailMessage()
    message["From"] = settings.smtp_from_email or settings.smtp_username or "noreply@example.com"
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    smtp_class = smtplib.SMTP_SSL if settings.smtp_use_ssl else smtplib.SMTP
    with smtp_class(
        settings.smtp_host,
        settings.smtp_port or 25,
        timeout=settings.smtp_timeout_seconds,
    ) as server:
        if not settings.smtp_use_ssl and settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_username and settings.smtp_password:
            server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)
    return True


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
    entry = await log(
        db,
        template=template,
        subject=subject,
        body=body,
        user_id=user_id,
        application_id=application_id,
    )

    recipient = await _resolve_recipient_email(db, user_id)
    if recipient:
        try:
            sent = await _deliver_via_smtp(
                recipient=recipient,
                subject=subject,
                body=body,
            )
            entry.status = "sent" if sent else "logged"
        except Exception:
            entry.status = "failed"
    else:
        entry.status = "logged"

    await db.flush()
    return entry
