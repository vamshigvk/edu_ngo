"""Shared enumerations mirroring the Django `choices` definitions.

Stored as plain strings in the database for portability and API friendliness.
"""
from enum import StrEnum


class CohortStatus(StrEnum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class UserRole(StrEnum):
    GUEST = "guest"
    MENTEE = "mentee"
    MENTOR = "mentor"
    REVIEWER = "reviewer"
    ADMIN = "admin"


class DecisionOutcome(StrEnum):
    """Select / Reject / Waitlist decision used by reviewers, the system, and admin."""

    SELECT = "select"
    REJECT = "reject"
    WAITLIST = "waitlist"


class FieldType(StrEnum):
    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    DROPDOWN = "dropdown"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    FILE_UPLOAD = "file_upload"
    BOOLEAN = "boolean"


class ApplicationStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    SCORED = "scored"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"


class ApplicationPurpose(StrEnum):
    SCHOLARSHIP = "scholarship"
    ADMISSION = "admission"
    CAREER_SWITCH = "career_switch"
    SKILL_BUILDING = "skill_building"
    OTHER = "other"


class PairStatus(StrEnum):
    RECOMMENDED = "recommended"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    TERMINATED = "terminated"


class PairOutcome(StrEnum):
    ACHIEVED = "achieved"
    PARTIAL = "partial"
    NOT_ACHIEVED = "not_achieved"
    PENDING = "pending"
    UNKNOWN = "unknown"


class CheckInStatus(StrEnum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    MISSED = "missed"
    CANCELLED = "cancelled"


class ResourceType(StrEnum):
    SCHOLARSHIP = "scholarship"
    COURSE = "course"
    UNIVERSITY_INFO = "university_info"
    GUIDE = "guide"
    VIDEO = "video"


class PermissionAction(StrEnum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class MentorshipType(StrEnum):
    """How a selected mentee is mentored (Phase 3 mapping)."""

    ONE_ON_ONE = "one_on_one"
    COHORT = "cohort"


class DocumentStatus(StrEnum):
    """University-application document review lifecycle (Phase 4)."""

    PENDING = "pending"
    ASSIGNED = "assigned"
    REVIEWED = "reviewed"


class WorkshopAudience(StrEnum):
    """Who a workshop is for (Phase 5)."""

    MENTEE_ONLY = "mentee_only"
    PUBLIC = "public"
