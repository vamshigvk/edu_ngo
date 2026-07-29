"""ORM models package.

Importing this package registers every model on ``Base.metadata`` — used by
Alembic autogeneration and by ``Base.metadata.create_all``.
"""
from app.core.database import Base
from app.models.application import Application, ApplicationFormConfig
from app.models.checkin import CheckIn
from app.models.closeout import OfferRecord, ProgrammeFeedback
from app.models.cohort import Cohort
from app.models.document import Document
from app.models.faq import FAQ
from app.models.notification import NotificationLog
from app.models.pairing import MentorMenteePair
from app.models.permission import RolePermission
from app.models.profile import MenteeProfile, MentorProfile
from app.models.resource import Resource
from app.models.review import ApplicationReview
from app.models.rules import MatchingRule, ScoringRule
from app.models.user import User
from app.models.workshop import Workshop, WorkshopSignup

__all__ = [
    "Base",
    "Application",
    "ApplicationFormConfig",
    "ApplicationReview",
    "CheckIn",
    "Cohort",
    "Document",
    "FAQ",
    "MentorMenteePair",
    "NotificationLog",
    "OfferRecord",
    "ProgrammeFeedback",
    "RolePermission",
    "MenteeProfile",
    "MentorProfile",
    "Resource",
    "MatchingRule",
    "ScoringRule",
    "User",
    "Workshop",
    "WorkshopSignup",
]
