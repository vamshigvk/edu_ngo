import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON

from app.db.base import Base


class ScoringRule(Base):
    __tablename__ = "scoring_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cohort_id = Column(String(36), ForeignKey("cohorts.id"), nullable=False)
    field_name = Column(String(255), nullable=False)
    weight = Column(Float, nullable=False, default=1.0)
    scoring_logic = Column(JSON, nullable=False, default=dict)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
