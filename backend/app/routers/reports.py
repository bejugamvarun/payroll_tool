from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
from app.database import get_db
from app.schemas.report import ReportGenerateRequest, ReportResponse
from app.models.reports import Report
from app.services.report_service import generate_report as create_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=List[ReportResponse])
def list_reports(
    college_id: int = None,
    year: int = None,
    month: int = None,
    report_type: str = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all reports with filters"""
    query = db.query(Report)

    if college_id:
        query = query.filter(Report.college_id == college_id)
    if year:
        query = query.filter(Report.year == year)
    if month:
        query = query.filter(Report.month == month)
    if report_type:
        query = query.filter(Report.report_type == report_type)

    reports = query.order_by(Report.generated_at.desc()).offset(skip).limit(limit).all()
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get a specific report by ID"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found"
        )
    return report


@router.post("/generate", response_model=ReportResponse)
def generate_report(request: ReportGenerateRequest, db: Session = Depends(get_db)):
    """Generate a new report"""
    try:
        report = create_report(
            college_id=request.college_id,
            year=request.year,
            month=request.month,
            report_type=request.report_type,
            db=db
        )
        return report
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )


@router.get("/{report_id}/download")
def download_report(report_id: int, db: Session = Depends(get_db)):
    """Download report file"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found"
        )

    if not os.path.exists(report.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found"
        )

    return FileResponse(
        path=report.file_path,
        filename=os.path.basename(report.file_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
