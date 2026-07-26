import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey

from app.db.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    type = Column(String(30), nullable=False)
    continent = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    course = Column(String(255), nullable=True)
    university = Column(String(255), nullable=True)
    level = Column(String(100), nullable=True)
    url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    added_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(String(50), nullable=False)
