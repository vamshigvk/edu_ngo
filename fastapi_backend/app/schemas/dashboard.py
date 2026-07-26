"""Dashboard response schemas (loosely typed aggregate payloads)."""
from typing import Any

from pydantic import BaseModel


class EmployeeDashboard(BaseModel):
    platform_summary: dict[str, int]
    cohort_breakdown: list[dict[str, Any]]
    system_health: dict[str, int]


class MentorDashboard(BaseModel):
    role: str = "Mentor"
    engagement_metrics: dict[str, int]
    assigned_cohorts: list[dict[str, Any]]


class MenteeDashboard(BaseModel):
    role: str = "Mentee"
    my_program_status: dict[str, Any]
    available_resources: list[dict[str, Any]]
