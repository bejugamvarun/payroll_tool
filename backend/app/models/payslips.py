from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Payslip(Base):
    __tablename__ = "payslips"

    id = Column(Integer, primary_key=True, index=True)
    payroll_entry_id = Column(Integer, ForeignKey("payroll_entries.id"), unique=True, nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    payroll_cycle_id = Column(Integer, ForeignKey("payroll_cycles.id"), nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    payroll_entry = relationship("PayrollEntry", back_populates="payslip")
    employee = relationship("Employee", back_populates="payslips")
    payroll_cycle = relationship("PayrollCycle", back_populates="payslips")
