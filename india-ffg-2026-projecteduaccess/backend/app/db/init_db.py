from app.db.base import Base, engine
from app.models import (
    Application,
    Notice,
    User,
    Cohort,
    MentorProfile,
    MenteeProfile,
    ApplicationFormConfig,
    ScoringRule,
    MatchingRule,
    MentorMenteePair,
    CheckIn,
    Resource,
    RolePermission,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
