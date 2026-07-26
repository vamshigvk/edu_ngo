from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON

from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    cohort_id = Column(String(36), nullable=True)
    applicant_email = Column(String(255), nullable=False)
    applicant_name = Column(String(255), nullable=False)
    program = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="draft")
    answers = Column(JSON, nullable=False, default=dict)
    purpose = Column(String(30), nullable=False, default="other")
    auto_score = Column(Float, nullable=False, default=0.0)
    final_score = Column(Float, nullable=False, default=0.0)
    reviewed_at = Column(String(50), nullable=True)
    created_at = Column(String(50), nullable=False)
