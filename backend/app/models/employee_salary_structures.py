from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class EmployeeSalaryStructure(Base):
    __tablename__ = "employee_salary_structures"
    __table_args__ = (
        UniqueConstraint('employee_id', 'salary_component_id', 'effective_from',
                         name='uq_employee_component_effective'),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    salary_component_id = Column(Integer, ForeignKey("salary_components.id"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="salary_structures")
    salary_component = relationship("SalaryComponent", back_populates="employee_structures")
