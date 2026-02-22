from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class PayrollCycleStatus(enum.Enum):
    DRAFT = "DRAFT"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    LOCKED = "LOCKED"


class PayrollCycle(Base):
    __tablename__ = "payroll_cycles"
    __table_args__ = (
        UniqueConstraint('college_id', 'year', 'month', name='uq_college_year_month'),
    )

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)
    total_working_days = Column(Integer, nullable=False)
    status = Column(SAEnum(PayrollCycleStatus), default=PayrollCycleStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    locked_at = Column(DateTime, nullable=True)

    # Relationships
    college = relationship("College", back_populates="payroll_cycles")
    payroll_entries = relationship("PayrollEntry", back_populates="payroll_cycle", cascade="all, delete-orphan")
    payslips = relationship("Payslip", back_populates="payroll_cycle", cascade="all, delete-orphan")
