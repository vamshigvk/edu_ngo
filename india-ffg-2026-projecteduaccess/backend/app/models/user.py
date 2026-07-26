from sqlalchemy import Column, Integer, String, Text

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    password_salt = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    verified_as = Column(String(50), nullable=True)
    token = Column(Text, nullable=True)
    created_at = Column(String(50), nullable=False)
