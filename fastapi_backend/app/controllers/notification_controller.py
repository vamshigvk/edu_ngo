"""Read-only view of the stubbed notification log (admin)."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.notification import NotificationLog
from app.schemas.notification import NotificationLogRead

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get(
    "",
    response_model=list[NotificationLogRead],
    summary="List logged notifications (stubbed emails)",
)
async def list_notifications(
    application_id: uuid.UUID | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(NotificationLog)
    if application_id:
        stmt = stmt.where(NotificationLog.application_id == application_id)
    stmt = stmt.order_by(NotificationLog.created_at.desc()).limit(limit)
    return list((await db.execute(stmt)).scalars().all())
