"""Aggregates every controller into the top-level routers.

- ``api_router``       → mounted under ``/api`` (resources, engines, workflows)
- ``auth_router``      → mounted at root (``/auth/...``)
- ``dashboard_router`` → mounted at root (``/dashboard/...``)
"""
from fastapi import APIRouter

from app.controllers import (
    application_controller,
    auth_controller,
    cohort_controller,
    dashboard_controller,
    user_controller,
)
from app.controllers.simple_resources import (
    checkin_router,
    form_config_router,
    matching_rule_router,
    mentee_profile_router,
    mentor_profile_router,
    pair_router,
    permission_router,
    resource_router,
    scoring_rule_router,
)

# --- /api namespace ---------------------------------------------------------
api_router = APIRouter()
api_router.include_router(cohort_controller.router)
api_router.include_router(user_controller.router)
api_router.include_router(mentor_profile_router)
api_router.include_router(mentee_profile_router)
api_router.include_router(form_config_router)
api_router.include_router(application_controller.router)
api_router.include_router(scoring_rule_router)
api_router.include_router(matching_rule_router)
api_router.include_router(pair_router)
api_router.include_router(checkin_router)
api_router.include_router(resource_router)
api_router.include_router(permission_router)

# --- root-level namespaces --------------------------------------------------
auth_router = auth_controller.router
dashboard_router = dashboard_controller.router
