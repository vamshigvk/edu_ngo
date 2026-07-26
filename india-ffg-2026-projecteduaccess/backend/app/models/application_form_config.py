import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, JSON

from app.db.base import Base


class ApplicationFormConfig(Base):
    __tablename__ = "application_form_configs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cohort_id = Column(String(36), ForeignKey("cohorts.id"), nullable=False)
    role = Column(String(50), nullable=True)
    field_name = Column(String(255), nullable=False)
    field_type = Column(String(30), nullable=False)
    is_required = Column(Boolean, nullable=False, default=False)
    field_order = Column(Integer, nullable=False, default=0)
    options = Column(JSON, nullable=False, default=list)
    validation_rules = Column(JSON, nullable=False, default=dict)
