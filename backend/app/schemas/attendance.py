from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from app.models.attendance_uploads import UploadStatus
from app.models.attendance_records import AttendanceStatus


class AttendanceUploadResponse(BaseModel):
    id: int
    college_id: int
    year: int
    month: int
    file_name: str
    file_path: str
    uploaded_at: datetime
    status: UploadStatus
    error_message: Optional[str] = None
    records_count: int

    model_config = ConfigDict(from_attributes=True)


class AttendanceRecordResponse(BaseModel):
    id: int
    employee_id: int
    date: date
    status: AttendanceStatus
    attendance_upload_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttendanceSummary(BaseModel):
    employee_id: int
    employee_name: str
    total_days: int
    present_days: Decimal
    absent_days: Decimal
    half_days: Decimal
    weekend_work_days: Decimal
    holidays: Decimal
    leaves: Decimal
