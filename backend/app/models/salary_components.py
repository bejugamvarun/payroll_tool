import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SAEnum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ComponentType(enum.Enum):
    EARNING = "EARNING"
    DEDUCTION = "DEDUCTION"


class AppliesTo(enum.Enum):
    ALL = "ALL"
    TEACHING = "TEACHING"
    NON_TEACHING = "NON_TEACHING"
    SUB_STAFF = "SUB_STAFF"


class SalaryComponent(Base):
    __tablename__ = "salary_components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    component_type = Column(SAEnum(ComponentType), nullable=False)
    applies_to = Column(SAEnum(AppliesTo), nullable=False, default=AppliesTo.ALL)
    is_default = Column(Boolean, default=False, nullable=False)
    is_percentage = Column(Boolean, default=False, nullable=False)
    percentage_value = Column(Numeric(5, 2), nullable=True)
    percentage_of = Column(String(50), nullable=True)  # "BASIC" or "GROSS"
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    employee_structures = relationship("EmployeeSalaryStructure", back_populates="salary_component")
    payroll_entry_components = relationship("PayrollEntryComponent", back_populates="salary_component")
