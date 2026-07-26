import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text

from app.db.base import Base


class MentorMenteePair(Base):
    __tablename__ = "mentor_mentee_pairs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cohort_id = Column(String(36), ForeignKey("cohorts.id"), nullable=False)
    status = Column(String(30), nullable=False, default="recommended")
    match_score = Column(Float, nullable=False, default=0.0)
    recommended_at = Column(String(50), nullable=False)
    accepted_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    accepted_at = Column(String(50), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    outcome = Column(String(30), nullable=False, default="pending")
    outcome_details = Column(Text, nullable=True)
