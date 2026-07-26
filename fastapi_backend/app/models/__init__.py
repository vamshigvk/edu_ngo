"""ORM models package.

Importing this package registers every model on ``Base.metadata`` — used by
Alembic autogeneration and by ``Base.metadata.create_all``.
"""
from app.core.database import Base
from app.models.application import Application, ApplicationFormConfig
from app.models.checkin import CheckIn
from app.models.cohort import Cohort
from app.models.pairing import MentorMenteePair
from app.models.permission import RolePermission
from app.models.profile import MenteeProfile, MentorProfile
from app.models.resource import Resource
from app.models.rules import MatchingRule, ScoringRule
from app.models.user import User

__all__ = [
    "Base",
    "Application",
    "ApplicationFormConfig",
    "CheckIn",
    "Cohort",
    "MentorMenteePair",
    "RolePermission",
    "MenteeProfile",
    "MentorProfile",
    "Resource",
    "MatchingRule",
    "ScoringRule",
    "User",
]
