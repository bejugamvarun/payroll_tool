from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class ComponentType(enum.Enum):
    EARNING = "EARNING"
    DEDUCTION = "DEDUCTION"


class SalaryComponent(Base):
    __tablename__ = "salary_components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    component_type = Column(SAEnum(ComponentType), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    employee_structures = relationship("EmployeeSalaryStructure", back_populates="salary_component")
    payroll_entry_components = relationship("PayrollEntryComponent", back_populates="salary_component")
