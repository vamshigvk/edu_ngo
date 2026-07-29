"""Dashboard endpoints (employee / mentor / mentee aggregate metrics).

Each endpoint is role-guarded: only an admin sees the program dashboard, and the
mentor/mentee portals are limited to those roles (admins always pass).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_admin, require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.dashboard import (
    EmployeeDashboard,
    MenteeDashboard,
    MentorDashboard,
)
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboards"])


@router.get(
    "/emp", response_model=EmployeeDashboard, summary="Program manager / admin dashboard"
)
async def employee_dashboard(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    return await dashboard_service.employee_dashboard(db)


@router.get("/mentor", response_model=MentorDashboard, summary="Mentor portal metrics")
async def mentor_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTOR)),
):
    return await dashboard_service.mentor_dashboard(db, current_user)


@router.get("/mentee", response_model=MenteeDashboard, summary="Mentee portal metrics")
async def mentee_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MENTEE)),
):
    return await dashboard_service.mentee_dashboard(db, current_user)
