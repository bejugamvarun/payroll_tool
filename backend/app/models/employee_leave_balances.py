from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class EmployeeLeaveBalance(Base):
    __tablename__ = "employee_leave_balances"
    __table_args__ = (
        UniqueConstraint('employee_id', 'year', name='uq_employee_year'),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    paid_leaves_total = Column(Numeric(5, 2), nullable=False)
    paid_leaves_used = Column(Numeric(5, 2), default=0, nullable=False)
    comp_leaves_earned = Column(Numeric(5, 2), default=0, nullable=False)
    comp_leaves_used = Column(Numeric(5, 2), default=0, nullable=False)
    carry_forward_leaves = Column(Numeric(5, 2), default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="leave_balances")
