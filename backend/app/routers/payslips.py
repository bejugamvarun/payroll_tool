from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
from app.database import get_db
from app.schemas.payslip import PayslipResponse
from app.models.payslips import Payslip
from app.services.payslip_service import generate_payslips_for_cycle, generate_bulk_zip
from app.config import settings

router = APIRouter(prefix="/payslips", tags=["payslips"])


@router.get("", response_model=List[PayslipResponse])
def list_payslips(
    employee_id: int = None,
    payroll_cycle_id: int = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all payslips with filters"""
    query = db.query(Payslip)

    if employee_id:
        query = query.filter(Payslip.employee_id == employee_id)
    if payroll_cycle_id:
        query = query.filter(Payslip.payroll_cycle_id == payroll_cycle_id)

    payslips = query.offset(skip).limit(limit).all()
    return payslips


@router.post("/generate/{payroll_cycle_id}", response_model=List[PayslipResponse])
def generate_payslips(payroll_cycle_id: int, db: Session = Depends(get_db)):
    """Generate payslips for a payroll cycle"""
    try:
        payslips = generate_payslips_for_cycle(payroll_cycle_id, db)
        return payslips
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payslip generation failed: {str(e)}"
        )


@router.get("/download-bulk/{cycle_id}")
def download_bulk_payslips(cycle_id: int, db: Session = Depends(get_db)):
    """Download all payslips for a cycle as a ZIP file"""
    from pathlib import Path

    zip_dir = Path(settings.PAYSLIP_PATH)
    zip_dir.mkdir(parents=True, exist_ok=True)
    zip_path = str(zip_dir / f"payslips_cycle_{cycle_id}.zip")

    try:
        generate_bulk_zip(cycle_id, db, zip_path)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return FileResponse(
        path=zip_path,
        filename=f"payslips_cycle_{cycle_id}.zip",
        media_type="application/zip"
    )


@router.get("/{payslip_id}", response_model=PayslipResponse)
def get_payslip(payslip_id: int, db: Session = Depends(get_db)):
    """Get a specific payslip by ID"""
    payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
    if not payslip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payslip with ID {payslip_id} not found"
        )
    return payslip


@router.get("/{payslip_id}/download")
def download_payslip(payslip_id: int, db: Session = Depends(get_db)):
    """Download payslip PDF"""
    payslip = db.query(Payslip).filter(Payslip.id == payslip_id).first()
    if not payslip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payslip with ID {payslip_id} not found"
        )

    if not os.path.exists(payslip.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payslip file not found"
        )

    return FileResponse(
        path=payslip.file_path,
        filename=os.path.basename(payslip.file_path),
        media_type="application/pdf"
    )
