import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON

from app.db.base import Base


class CheckIn(Base):
    __tablename__ = "checkins"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pair_id = Column(String(36), ForeignKey("mentor_mentee_pairs.id"), nullable=False)
    sequence_number = Column(Integer, nullable=False)
    date = Column(String(20), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="scheduled")
    action_items = Column(JSON, nullable=False, default=list)
    logged_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    next_checkin_date = Column(String(20), nullable=True)
    created_at = Column(String(50), nullable=False)
