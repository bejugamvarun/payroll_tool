from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20))

    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    designation_id = Column(Integer, ForeignKey("designations.id"), nullable=False, index=True)

    date_of_joining = Column(Date, nullable=False)
    date_of_leaving = Column(Date, nullable=True)

    bank_name = Column(String(255))
    bank_account_number = Column(String(50))
    ifsc_code = Column(String(20))
    pan_number = Column(String(20))

    ctc = Column(Numeric(12, 2), nullable=False)
    monthly_gross = Column(Numeric(12, 2), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    college = relationship("College", back_populates="employees")
    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    salary_structures = relationship("EmployeeSalaryStructure", back_populates="employee", cascade="all, delete-orphan")
    leave_balances = relationship("EmployeeLeaveBalance", back_populates="employee", cascade="all, delete-orphan")
    attendance_records = relationship("AttendanceRecord", back_populates="employee", cascade="all, delete-orphan")
    payroll_entries = relationship("PayrollEntry", back_populates="employee", cascade="all, delete-orphan")
    payslips = relationship("Payslip", back_populates="employee", cascade="all, delete-orphan")
