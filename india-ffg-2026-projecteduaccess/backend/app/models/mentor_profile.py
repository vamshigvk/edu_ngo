import uuid
from sqlalchemy import Column, String, Integer, Text, ForeignKey, JSON

from app.db.base import Base


class MentorProfile(Base):
    __tablename__ = "mentor_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expertise = Column(JSON, nullable=False, default=list)
    max_mentees = Column(Integer, nullable=False, default=1)
    availability = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    languages = Column(JSON, nullable=False, default=list)
