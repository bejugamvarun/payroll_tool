from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(Integer, nullable=False)
    college_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    departments = relationship("Department", back_populates="college", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="college", cascade="all, delete-orphan")
    leave_policies = relationship("LeavePolicy", back_populates="college", cascade="all, delete-orphan")
    attendance_uploads = relationship("AttendanceUpload", back_populates="college", cascade="all, delete-orphan")
    holidays = relationship("Holiday", back_populates="college", cascade="all, delete-orphan")
    payroll_cycles = relationship("PayrollCycle", back_populates="college", cascade="all, delete-orphan")
    designations = relationship("Designation", back_populates="college", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="college")
