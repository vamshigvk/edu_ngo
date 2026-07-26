from sqlalchemy import Column, Integer, String, Text

from app.db.base import Base


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(String(50), nullable=False)
