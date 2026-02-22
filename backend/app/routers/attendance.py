from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.attendance import AttendanceUploadResponse, AttendanceRecordResponse, AttendanceSummary
from app.models.attendance_uploads import AttendanceUpload
from app.models.attendance_records import AttendanceRecord
from app.services.attendance_service import process_attendance_upload, get_attendance_summary

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("/uploads", response_model=List[AttendanceUploadResponse])
def list_attendance_uploads(
    college_id: int = None,
    year: int = None,
    month: int = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all attendance uploads with filters"""
    query = db.query(AttendanceUpload)

    if college_id:
        query = query.filter(AttendanceUpload.college_id == college_id)
    if year:
        query = query.filter(AttendanceUpload.year == year)
    if month:
        query = query.filter(AttendanceUpload.month == month)

    uploads = query.offset(skip).limit(limit).all()
    return uploads


@router.get("/uploads/{upload_id}", response_model=AttendanceUploadResponse)
def get_attendance_upload(upload_id: int, db: Session = Depends(get_db)):
    """Get a specific attendance upload by ID"""
    upload = db.query(AttendanceUpload).filter(AttendanceUpload.id == upload_id).first()
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance upload with ID {upload_id} not found"
        )
    return upload


@router.post("/upload", response_model=AttendanceUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_attendance(
    college_id: int,
    year: int,
    month: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload attendance Excel file"""
    import os
    from app.config import settings
    from app.models.attendance_uploads import UploadStatus

    os.makedirs(settings.UPLOAD_PATH, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_PATH, f"{college_id}_{year}_{month}_{file.filename}")

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    db_upload = AttendanceUpload(
        college_id=college_id,
        year=year,
        month=month,
        file_name=file.filename,
        file_path=file_path,
        status=UploadStatus.PENDING,
        records_count=0
    )
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)

    # Process the upload immediately
    try:
        process_result = process_attendance_upload(db_upload.id, db)
        db.refresh(db_upload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing attendance file: {str(e)}"
        )

    return db_upload


@router.get("/records", response_model=List[AttendanceRecordResponse])
def list_attendance_records(
    employee_id: int = None,
    year: int = None,
    month: int = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List attendance records with filters"""
    from datetime import date

    query = db.query(AttendanceRecord)

    if employee_id:
        query = query.filter(AttendanceRecord.employee_id == employee_id)

    if year and month:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        query = query.filter(AttendanceRecord.date >= start_date, AttendanceRecord.date < end_date)

    records = query.offset(skip).limit(limit).all()
    return records


@router.get("/summary", response_model=List[AttendanceSummary])
def get_summary(
    college_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """Get attendance summary for a college for a specific month"""
    try:
        summary = get_attendance_summary(college_id, year, month, db)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating attendance summary: {str(e)}"
        )
