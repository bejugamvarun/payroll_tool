import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, Date, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class StaffType(enum.Enum):
    TEACHING = "TEACHING"
    NON_TEACHING = "NON_TEACHING"
    SUB_STAFF = "SUB_STAFF"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=True, index=True)
    name = Column(String(255), nullable=False)
    staff_type = Column(SAEnum(StaffType), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    mobile_number = Column(String(20), nullable=True)

    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True, index=True)
    designation_id = Column(Integer, ForeignKey("designations.id"), nullable=True, index=True)

    date_of_joining = Column(Date, nullable=False)
    date_of_leaving = Column(Date, nullable=True)

    pay_scale = Column(String(500), nullable=True)
    actual_basic = Column(Numeric(12, 2), nullable=True)

    bank_name = Column(String(255), nullable=True)
    bank_branch = Column(String(255), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(20), nullable=True)
    beneficiary_name = Column(String(255), nullable=True)

    pan_number = Column(String(20), nullable=True)
    aadhaar_number = Column(String(20), nullable=True)

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
