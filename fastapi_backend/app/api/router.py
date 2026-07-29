"""Aggregates every controller into the top-level routers.

- ``api_router``       → mounted under ``/api`` (resources, engines, workflows)
- ``auth_router``      → mounted at root (``/auth/...``)
- ``dashboard_router`` → mounted at root (``/dashboard/...``)
"""
from fastapi import APIRouter

from app.controllers import (
    application_controller,
    auth_controller,
    closeout_controller,
    cohort_controller,
    dashboard_controller,
    document_controller,
    mapping_controller,
    notification_controller,
    public_controller,
    review_controller,
    user_controller,
    workshop_controller,
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

# --- /api namespace (admin-guarded in main.py) ------------------------------
api_router = APIRouter()
api_router.include_router(cohort_controller.router)
api_router.include_router(user_controller.router)
api_router.include_router(mentor_profile_router)
api_router.include_router(mentee_profile_router)
api_router.include_router(form_config_router)
# Selection-pipeline routes registered BEFORE the application CRUD router so the
# static ``/applications/review-board`` path is matched ahead of ``/{item_id}``.
api_router.include_router(application_controller.selection_router)
api_router.include_router(application_controller.router)
api_router.include_router(scoring_rule_router)
api_router.include_router(matching_rule_router)
api_router.include_router(pair_router)
api_router.include_router(checkin_router)
api_router.include_router(resource_router)
api_router.include_router(permission_router)
api_router.include_router(notification_controller.router)
api_router.include_router(mapping_controller.router)

# --- public /api namespace (NO auth — mounted separately in main.py) --------
# Kept out of ``api_router`` so the admin auth dependency does not apply to it.
public_router = public_controller.router

# --- reviewer /api namespace (reviewer-or-admin, mounted separately) --------
# Kept out of ``api_router`` so reviewers (not just admins) can reach it; each
# endpoint carries its own ``require_reviewer`` guard.
review_router = review_controller.router

# --- mixed-role /api routers (per-endpoint guards, mounted separately) ------
# These span mentee/mentor/admin; each endpoint guards its own role.
document_router = document_controller.router
workshop_router = workshop_controller.router
closeout_router = closeout_controller.router

# --- root-level namespaces --------------------------------------------------
auth_router = auth_controller.router
dashboard_router = dashboard_controller.router
