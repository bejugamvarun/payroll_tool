from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class UploadStatus(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AttendanceUpload(Base):
    __tablename__ = "attendance_uploads"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(SAEnum(UploadStatus), default=UploadStatus.PENDING, nullable=False)
    error_message = Column(String(1000), nullable=True)
    records_count = Column(Integer, default=0, nullable=False)

    # Relationships
    college = relationship("College", back_populates="attendance_uploads")
    attendance_records = relationship("AttendanceRecord", back_populates="attendance_upload", cascade="all, delete-orphan")
