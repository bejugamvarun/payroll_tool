from typing import Dict, List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.attendance_uploads import AttendanceUpload, UploadStatus
from app.models.attendance_records import AttendanceRecord, AttendanceStatus
from app.models.employees import Employee
from app.schemas.attendance import AttendanceSummary
from app.utils.excel_parser import parse_attendance_excel


def process_attendance_upload(upload_id: int, db: Session) -> Dict:
    """
    Process an uploaded attendance Excel file.

    Args:
        upload_id: AttendanceUpload ID
        db: Database session

    Returns:
        Dictionary with processing results
    """
    # Get the upload record
    upload = db.query(AttendanceUpload).filter(AttendanceUpload.id == upload_id).first()

    if not upload:
        raise ValueError(f"Attendance upload with ID {upload_id} not found")

    if upload.status != UploadStatus.PENDING:
        raise ValueError(f"Upload {upload_id} is not in PENDING status")

    # Update status to PROCESSING
    upload.status = UploadStatus.PROCESSING
    db.commit()

    try:
        # Parse the Excel file
        parse_result = parse_attendance_excel(upload.file_path, upload.college_id, db)

        if parse_result["errors"]:
            # If there are errors, mark as failed
            upload.status = UploadStatus.FAILED
            upload.error_message = "; ".join(parse_result["errors"][:5])  # Store first 5 errors
            upload.records_count = 0
            db.commit()

            return {
                "success": False,
                "upload_id": upload_id,
                "errors": parse_result["errors"],
                "records_created": 0
            }

        # Create or update attendance records
        records_created = 0
        records_updated = 0

        for record_data in parse_result["records"]:
            # Check if record already exists
            existing_record = db.query(AttendanceRecord).filter(
                AttendanceRecord.employee_id == record_data["employee_id"],
                AttendanceRecord.date == record_data["date"]
            ).first()

            if existing_record:
                # Update existing record
                existing_record.status = record_data["status"]
                existing_record.attendance_upload_id = upload_id
                records_updated += 1
            else:
                # Create new record
                new_record = AttendanceRecord(
                    employee_id=record_data["employee_id"],
                    date=record_data["date"],
                    status=record_data["status"],
                    attendance_upload_id=upload_id
                )
                db.add(new_record)
                records_created += 1

        # Commit all records
        db.commit()

        # Update upload status
        upload.status = UploadStatus.COMPLETED
        upload.records_count = records_created + records_updated
        db.commit()

        return {
            "success": True,
            "upload_id": upload_id,
            "records_created": records_created,
            "records_updated": records_updated,
            "total_records": records_created + records_updated,
            "errors": []
        }

    except Exception as e:
        # Mark as failed
        upload.status = UploadStatus.FAILED
        upload.error_message = str(e)
        db.commit()

        return {
            "success": False,
            "upload_id": upload_id,
            "errors": [str(e)],
            "records_created": 0
        }


def get_attendance_summary(
    college_id: int,
    year: int,
    month: int,
    db: Session
) -> List[AttendanceSummary]:
    """
    Get attendance summary for all employees in a college for a specific month.

    Args:
        college_id: College ID
        year: Year
        month: Month
        db: Database session

    Returns:
        List of AttendanceSummary objects
    """
    from datetime import date
    from calendar import monthrange

    # Get date range for the month
    start_date = date(year, month, 1)
    _, last_day = monthrange(year, month)
    end_date = date(year, month, last_day)

    # Get all active employees for the college
    employees = db.query(Employee).filter(
        Employee.college_id == college_id,
        Employee.is_active == True
    ).all()

    summaries = []

    for employee in employees:
        # Get attendance records for the month
        records = db.query(AttendanceRecord).filter(
            AttendanceRecord.employee_id == employee.id,
            AttendanceRecord.date >= start_date,
            AttendanceRecord.date <= end_date
        ).all()

        # Calculate statistics
        present_days = Decimal(0)
        absent_days = Decimal(0)
        half_days = Decimal(0)
        weekend_work_days = Decimal(0)
        holidays = Decimal(0)
        leaves = Decimal(0)

        for record in records:
            if record.status == AttendanceStatus.PRESENT:
                present_days += Decimal(1)
            elif record.status == AttendanceStatus.ABSENT:
                absent_days += Decimal(1)
            elif record.status == AttendanceStatus.HALF_DAY:
                half_days += Decimal(1)
                present_days += Decimal("0.5")
            elif record.status == AttendanceStatus.WEEKEND_WORK:
                weekend_work_days += Decimal(1)
                present_days += Decimal(1)
            elif record.status == AttendanceStatus.HOLIDAY:
                holidays += Decimal(1)
            elif record.status == AttendanceStatus.LEAVE:
                leaves += Decimal(1)

        summary = AttendanceSummary(
            employee_id=employee.id,
            employee_name=f"{employee.first_name} {employee.last_name}",
            total_days=last_day,
            present_days=present_days,
            absent_days=absent_days,
            half_days=half_days,
            weekend_work_days=weekend_work_days,
            holidays=holidays,
            leaves=leaves
        )

        summaries.append(summary)

    return summaries
