from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class AttendanceStatus(enum.Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    HALF_DAY = "HALF_DAY"
    WEEKEND_WORK = "WEEKEND_WORK"
    HOLIDAY = "HOLIDAY"
    LEAVE = "LEAVE"


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='uq_employee_date'),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(SAEnum(AttendanceStatus), nullable=False)
    attendance_upload_id = Column(Integer, ForeignKey("attendance_uploads.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="attendance_records")
    attendance_upload = relationship("AttendanceUpload", back_populates="attendance_records")
