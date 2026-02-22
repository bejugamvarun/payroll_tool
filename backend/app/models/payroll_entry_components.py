from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.salary_components import ComponentType


class PayrollEntryComponent(Base):
    __tablename__ = "payroll_entry_components"

    id = Column(Integer, primary_key=True, index=True)
    payroll_entry_id = Column(Integer, ForeignKey("payroll_entries.id"), nullable=False, index=True)
    salary_component_id = Column(Integer, ForeignKey("salary_components.id"), nullable=False, index=True)
    component_type = Column(SAEnum(ComponentType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    payroll_entry = relationship("PayrollEntry", back_populates="components")
    salary_component = relationship("SalaryComponent", back_populates="payroll_entry_components")
