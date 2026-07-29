"""Dashboard response schemas (loosely typed aggregate payloads)."""
from typing import Any

from pydantic import BaseModel


class EmployeeDashboard(BaseModel):
    platform_summary: dict[str, int]
    cohort_breakdown: list[dict[str, Any]]
    system_health: dict[str, int]


class MentorDashboard(BaseModel):
    role: str = "Mentor"
    profile: dict[str, Any] | None = None
    engagement_metrics: dict[str, int]
    mentees: list[dict[str, Any]] = []
    assigned_cohorts: list[dict[str, Any]]


class MenteeDashboard(BaseModel):
    role: str = "Mentee"
    profile: dict[str, Any] | None = None
    my_program_status: dict[str, Any]
    mentor: dict[str, Any] | None = None
    checkins: list[dict[str, Any]] = []
