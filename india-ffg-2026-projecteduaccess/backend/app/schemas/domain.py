from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class CohortBase(BaseModel):
    name: str
    program: str
    start_date: str
    end_date: str
    status: Optional[str] = "upcoming"
    max_mentees: Optional[int] = 0


class CohortCreate(CohortBase):
    pass


class CohortUpdate(BaseModel):
    name: Optional[str]
    program: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    status: Optional[str]
    max_mentees: Optional[int]


class CohortRead(CohortBase):
    id: str
    created_at: str

    class Config:
        orm_mode = True


class MentorProfileBase(BaseModel):
    user_id: int
    expertise: Optional[List[str]] = Field(default_factory=list)
    max_mentees: Optional[int] = 1
    availability: Optional[str] = None
    bio: Optional[str] = None
    languages: Optional[List[str]] = Field(default_factory=list)


class MentorProfileCreate(MentorProfileBase):
    pass


class MentorProfileUpdate(BaseModel):
    expertise: Optional[List[str]]
    max_mentees: Optional[int]
    availability: Optional[str]
    bio: Optional[str]
    languages: Optional[List[str]]


class MentorProfileRead(MentorProfileBase):
    id: str

    class Config:
        orm_mode = True


class MenteeProfileBase(BaseModel):
    user_id: int
    university: Optional[str] = None
    country: Optional[str] = None
    course: Optional[str] = None
    level: Optional[str] = None
    cohort_id: Optional[str] = None


class MenteeProfileCreate(MenteeProfileBase):
    pass


class MenteeProfileUpdate(BaseModel):
    university: Optional[str]
    country: Optional[str]
    course: Optional[str]
    level: Optional[str]
    cohort_id: Optional[str]


class MenteeProfileRead(MenteeProfileBase):
    id: str

    class Config:
        orm_mode = True


class ApplicationFormConfigBase(BaseModel):
    cohort_id: str
    role: Optional[str] = None
    field_name: str
    field_type: str
    is_required: Optional[bool] = False
    field_order: Optional[int] = 0
    options: Optional[List[Any]] = Field(default_factory=list)
    validation_rules: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class ApplicationFormConfigCreate(ApplicationFormConfigBase):
    pass


class ApplicationFormConfigUpdate(BaseModel):
    cohort_id: Optional[str]
    role: Optional[str]
    field_name: Optional[str]
    field_type: Optional[str]
    is_required: Optional[bool]
    field_order: Optional[int]
    options: Optional[List[Any]]
    validation_rules: Optional[List[Dict[str, Any]]]


class ApplicationFormConfigRead(ApplicationFormConfigBase):
    id: str

    class Config:
        orm_mode = True


class ApplicationBase(BaseModel):
    user_id: int
    cohort_id: str
    status: Optional[str] = "draft"
    answers: Optional[Dict[str, Any]] = Field(default_factory=dict)
    purpose: Optional[str] = "other"
    auto_score: Optional[float] = 0.0
    final_score: Optional[float] = 0.0
    reviewed_at: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    applicant_name: Optional[str] = None
    applicant_email: Optional[EmailStr] = None


class ApplicationUpdate(BaseModel):
    user_id: Optional[int]
    cohort_id: Optional[str]
    status: Optional[str]
    answers: Optional[Dict[str, Any]]
    purpose: Optional[str]
    auto_score: Optional[float]
    final_score: Optional[float]
    reviewed_at: Optional[str]


class ApplicationRead(ApplicationBase):
    id: int
    applicant_email: str
    applicant_name: str
    created_at: str

    class Config:
        orm_mode = True


class ScoringRuleBase(BaseModel):
    cohort_id: str
    field_name: str
    weight: Optional[float] = 1.0
    scoring_logic: Optional[Dict[str, Any]] = Field(default_factory=dict)
    created_by: Optional[int] = None


class ScoringRuleCreate(ScoringRuleBase):
    pass


class ScoringRuleUpdate(BaseModel):
    cohort_id: Optional[str]
    field_name: Optional[str]
    weight: Optional[float]
    scoring_logic: Optional[Dict[str, Any]]
    created_by: Optional[int]


class ScoringRuleRead(ScoringRuleBase):
    id: str

    class Config:
        orm_mode = True


class MatchingRuleBase(BaseModel):
    cohort_id: str
    criteria_name: str
    weight: Optional[float] = 1.0
    match_logic: Optional[Dict[str, Any]] = Field(default_factory=dict)
    created_by: Optional[int] = None


class MatchingRuleCreate(MatchingRuleBase):
    pass


class MatchingRuleUpdate(BaseModel):
    cohort_id: Optional[str]
    criteria_name: Optional[str]
    weight: Optional[float]
    match_logic: Optional[Dict[str, Any]]
    created_by: Optional[int]


class MatchingRuleRead(MatchingRuleBase):
    id: str

    class Config:
        orm_mode = True


class MentorMenteePairBase(BaseModel):
    mentor_id: int
    mentee_id: int
    cohort_id: str
    status: Optional[str] = "recommended"
    match_score: Optional[float] = 0.0
    recommended_at: Optional[str] = None
    accepted_by_id: Optional[int] = None
    accepted_at: Optional[str] = None
    rejection_reason: Optional[str] = None
    notes: Optional[str] = None
    outcome: Optional[str] = "pending"
    outcome_details: Optional[str] = None


class MentorMenteePairCreate(MentorMenteePairBase):
    pass


class MentorMenteePairUpdate(BaseModel):
    mentor_id: Optional[int]
    mentee_id: Optional[int]
    cohort_id: Optional[str]
    status: Optional[str]
    match_score: Optional[float]
    recommended_at: Optional[str]
    accepted_by_id: Optional[int]
    accepted_at: Optional[str]
    rejection_reason: Optional[str]
    notes: Optional[str]
    outcome: Optional[str]
    outcome_details: Optional[str]


class MentorMenteePairRead(MentorMenteePairBase):
    id: str

    class Config:
        orm_mode = True


class CheckInBase(BaseModel):
    pair_id: str
    sequence_number: int
    date: str
    notes: Optional[str] = None
    status: Optional[str] = "scheduled"
    action_items: Optional[List[Any]] = Field(default_factory=list)
    logged_by_id: Optional[int] = None
    next_checkin_date: Optional[str] = None


class CheckInCreate(CheckInBase):
    pass


class CheckInUpdate(BaseModel):
    sequence_number: Optional[int]
    date: Optional[str]
    notes: Optional[str]
    status: Optional[str]
    action_items: Optional[List[Any]]
    logged_by_id: Optional[int]
    next_checkin_date: Optional[str]


class CheckInRead(CheckInBase):
    id: str
    created_at: str

    class Config:
        orm_mode = True


class ResourceBase(BaseModel):
    title: str
    type: str
    continent: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    course: Optional[str] = None
    university: Optional[str] = None
    level: Optional[str] = None
    url: str
    description: Optional[str] = None
    added_by_id: Optional[int] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    title: Optional[str]
    type: Optional[str]
    continent: Optional[str]
    country: Optional[str]
    state: Optional[str]
    course: Optional[str]
    university: Optional[str]
    level: Optional[str]
    url: Optional[str]
    description: Optional[str]
    added_by_id: Optional[int]


class ResourceRead(ResourceBase):
    id: str
    created_at: str

    class Config:
        orm_mode = True


class RolePermissionBase(BaseModel):
    role: str
    resource: str
    action: str
    is_allowed: Optional[bool] = False
    modified_by_id: Optional[int] = None


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(BaseModel):
    role: Optional[str]
    resource: Optional[str]
    action: Optional[str]
    is_allowed: Optional[bool]
    modified_by_id: Optional[int]


class RolePermissionRead(RolePermissionBase):
    id: str

    class Config:
        orm_mode = True


class SubmitApplicationRequest(BaseModel):
    pass


class ReviewApplicationRequest(BaseModel):
    approve: bool = True
