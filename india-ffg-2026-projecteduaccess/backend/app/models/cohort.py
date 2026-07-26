import uuid
from sqlalchemy import Column, String, Integer

from app.db.base import Base


class Cohort(Base):
    __tablename__ = "cohorts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    program = Column(String(255), nullable=False)
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="upcoming")
    max_mentees = Column(Integer, nullable=False, default=0)
    created_at = Column(String(50), nullable=False)
