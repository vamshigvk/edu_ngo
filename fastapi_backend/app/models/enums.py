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
    ADMIN = "admin"


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
