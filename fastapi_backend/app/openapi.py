"""Custom OpenAPI schema with a JWT bearer security scheme for Swagger."""
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app import __version__

DESCRIPTION = """
**FFG Mentorship Platform API** — enterprise FastAPI backend.

Manages cohorts, users, mentor/mentee profiles, applications, scoring & matching
engines, mentor–mentee pairings, check-ins, resources, and role permissions.

### Authentication
1. `POST /auth/register` to create an account.
2. `POST /auth/login` (OAuth2 password flow) to obtain a JWT.
3. Click **Authorize** and paste the token to call protected endpoints.
"""

TAGS_METADATA = [
    {"name": "Auth", "description": "Registration, login (JWT), and current user."},
    {"name": "Cohorts", "description": "Cohorts plus scoring/matching engine runs."},
    {"name": "Users", "description": "User account management."},
    {"name": "Mentor Profiles", "description": "Mentor profile records."},
    {"name": "Mentee Profiles", "description": "Mentee profile records."},
    {"name": "Form Configs", "description": "Per-cohort application form fields."},
    {"name": "Applications", "description": "Applications with submit/review workflow."},
    {"name": "Scoring Rules", "description": "Scoring rule configuration."},
    {"name": "Matching Rules", "description": "Matching rule configuration."},
    {"name": "Pairs", "description": "Mentor–mentee pairings."},
    {"name": "Check-Ins", "description": "Mentorship check-in tracking."},
    {"name": "Resources", "description": "Learning resource library."},
    {"name": "Permissions", "description": "Role-based permission matrix."},
    {"name": "Dashboards", "description": "Aggregate metrics per persona."},
]


def custom_openapi(app: FastAPI):
    def _openapi():
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(
            title=app.title,
            version=__version__,
            description=DESCRIPTION,
            routes=app.routes,
            tags=TAGS_METADATA,
        )
        schema["info"]["contact"] = {
            "name": "FFG Platform Team",
            "email": "support@ffg.example",
        }
        schema["info"]["license"] = {"name": "Proprietary"}
        schema.setdefault("components", {})["securitySchemes"] = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
        schema["security"] = [{"bearerAuth": []}]
        app.openapi_schema = schema
        return schema

    return _openapi
