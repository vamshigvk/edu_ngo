"""Instantiated CRUD services for every simple resource.

Resources with business logic (users/auth, applications, scoring, matching,
dashboards) have their own dedicated service modules.
"""
from app.models.application import Application, ApplicationFormConfig
from app.models.checkin import CheckIn
from app.models.cohort import Cohort
from app.models.faq import FAQ
from app.models.pairing import MentorMenteePair
from app.models.permission import RolePermission
from app.models.profile import MenteeProfile, MentorProfile
from app.models.resource import Resource
from app.models.rules import MatchingRule, ScoringRule
from app.services.base import CRUDService
from app.services.enrich import enrich_pair_names, enrich_user_name

cohort_service = CRUDService(Cohort)
mentor_profile_service = CRUDService(MentorProfile, enrich=enrich_user_name)
mentee_profile_service = CRUDService(MenteeProfile, enrich=enrich_user_name)
form_config_service = CRUDService(ApplicationFormConfig)
application_service = CRUDService(Application, enrich=enrich_user_name)
scoring_rule_service = CRUDService(ScoringRule)
matching_rule_service = CRUDService(MatchingRule)
pair_service = CRUDService(MentorMenteePair, enrich=enrich_pair_names)
checkin_service = CRUDService(CheckIn)
resource_service = CRUDService(Resource)
permission_service = CRUDService(RolePermission)
faq_service = CRUDService(FAQ)
