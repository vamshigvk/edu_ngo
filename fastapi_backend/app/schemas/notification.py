"""Notification-log (stubbed email) schemas."""
import uuid
from datetime import datetime

from app.schemas.common import ORMModel


class NotificationLogRead(ORMModel):
    id: uuid.UUID
    user_id: uuid.UUID | None = None
    application_id: uuid.UUID | None = None
    channel: str = "email"
    template: str
    subject: str
    body: str
    status: str = "logged"
    created_at: datetime
