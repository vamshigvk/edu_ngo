import uuid
from sqlalchemy import Column, String, Integer, ForeignKey

from app.db.base import Base


class MenteeProfile(Base):
    __tablename__ = "mentee_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    university = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    course = Column(String(255), nullable=True)
    level = Column(String(100), nullable=True)
    cohort_id = Column(String(36), ForeignKey("cohorts.id"), nullable=True)
