from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class PayrollEntry(Base):
    __tablename__ = "payroll_entries"
    __table_args__ = (
        UniqueConstraint('payroll_cycle_id', 'employee_id', name='uq_cycle_employee'),
    )

    id = Column(Integer, primary_key=True, index=True)
    payroll_cycle_id = Column(Integer, ForeignKey("payroll_cycles.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)

    days_present = Column(Numeric(5, 2), nullable=False)
    days_absent = Column(Numeric(5, 2), nullable=False)
    paid_leaves_used = Column(Numeric(5, 2), default=0, nullable=False)
    comp_leaves_used = Column(Numeric(5, 2), default=0, nullable=False)
    unpaid_leaves = Column(Numeric(5, 2), default=0, nullable=False)
    loss_of_pay = Column(Numeric(12, 2), default=0, nullable=False)

    gross_earnings = Column(Numeric(12, 2), nullable=False)
    total_deductions = Column(Numeric(12, 2), nullable=False)
    net_pay = Column(Numeric(12, 2), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    payroll_cycle = relationship("PayrollCycle", back_populates="payroll_entries")
    employee = relationship("Employee", back_populates="payroll_entries")
    components = relationship("PayrollEntryComponent", back_populates="payroll_entry", cascade="all, delete-orphan")
    payslip = relationship("Payslip", back_populates="payroll_entry", uselist=False, cascade="all, delete-orphan")
