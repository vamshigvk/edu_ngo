"""CRUD routers for resources without extra business-logic actions.

Each router is a standard CRUD surface built via ``build_crud_router``.
"""
from app.controllers.crud_factory import build_crud_router
from app.schemas.application import (
    ApplicationFormConfigCreate,
    ApplicationFormConfigRead,
    ApplicationFormConfigUpdate,
)
from app.schemas.checkin import CheckInCreate, CheckInRead, CheckInUpdate
from app.schemas.permission import (
    RolePermissionCreate,
    RolePermissionRead,
    RolePermissionUpdate,
)
from app.schemas.pairing import (
    MentorMenteePairCreate,
    MentorMenteePairRead,
    MentorMenteePairUpdate,
)
from app.schemas.profile import (
    MenteeProfileCreate,
    MenteeProfileRead,
    MenteeProfileUpdate,
    MentorProfileCreate,
    MentorProfileRead,
    MentorProfileUpdate,
)
from app.schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate
from app.schemas.rules import (
    MatchingRuleCreate,
    MatchingRuleRead,
    MatchingRuleUpdate,
    ScoringRuleCreate,
    ScoringRuleRead,
    ScoringRuleUpdate,
)
from app.services.crud import (
    checkin_service,
    form_config_service,
    matching_rule_service,
    mentee_profile_service,
    mentor_profile_service,
    pair_service,
    permission_service,
    resource_service,
    scoring_rule_service,
)

mentor_profile_router = build_crud_router(
    service=mentor_profile_service,
    prefix="/mentor-profiles",
    tag="Mentor Profiles",
    read_schema=MentorProfileRead,
    create_schema=MentorProfileCreate,
    update_schema=MentorProfileUpdate,
)

mentee_profile_router = build_crud_router(
    service=mentee_profile_service,
    prefix="/mentee-profiles",
    tag="Mentee Profiles",
    read_schema=MenteeProfileRead,
    create_schema=MenteeProfileCreate,
    update_schema=MenteeProfileUpdate,
)

form_config_router = build_crud_router(
    service=form_config_service,
    prefix="/form-configs",
    tag="Form Configs",
    read_schema=ApplicationFormConfigRead,
    create_schema=ApplicationFormConfigCreate,
    update_schema=ApplicationFormConfigUpdate,
)

scoring_rule_router = build_crud_router(
    service=scoring_rule_service,
    prefix="/scoring-rules",
    tag="Scoring Rules",
    read_schema=ScoringRuleRead,
    create_schema=ScoringRuleCreate,
    update_schema=ScoringRuleUpdate,
)

matching_rule_router = build_crud_router(
    service=matching_rule_service,
    prefix="/matching-rules",
    tag="Matching Rules",
    read_schema=MatchingRuleRead,
    create_schema=MatchingRuleCreate,
    update_schema=MatchingRuleUpdate,
)

pair_router = build_crud_router(
    service=pair_service,
    prefix="/pairs",
    tag="Pairs",
    read_schema=MentorMenteePairRead,
    create_schema=MentorMenteePairCreate,
    update_schema=MentorMenteePairUpdate,
)

checkin_router = build_crud_router(
    service=checkin_service,
    prefix="/checkins",
    tag="Check-Ins",
    read_schema=CheckInRead,
    create_schema=CheckInCreate,
    update_schema=CheckInUpdate,
)

resource_router = build_crud_router(
    service=resource_service,
    prefix="/resources",
    tag="Resources",
    read_schema=ResourceRead,
    create_schema=ResourceCreate,
    update_schema=ResourceUpdate,
)

permission_router = build_crud_router(
    service=permission_service,
    prefix="/permissions",
    tag="Permissions",
    read_schema=RolePermissionRead,
    create_schema=RolePermissionCreate,
    update_schema=RolePermissionUpdate,
)
