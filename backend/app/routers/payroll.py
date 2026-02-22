from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.payroll import (
    PayrollCycleResponse,
    PayrollEntryResponse,
    PayrollCalculateRequest,
    PayrollSummaryResponse
)
from app.models.payroll_cycles import PayrollCycle
from app.models.payroll_entries import PayrollEntry
from app.services.payroll_service import calculate_payroll as run_payroll_calculation, lock_payroll_cycle

router = APIRouter(prefix="/payroll", tags=["payroll"])


@router.get("/cycles", response_model=List[PayrollCycleResponse])
def list_payroll_cycles(
    college_id: int = None,
    year: int = None,
    month: int = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all payroll cycles with filters"""
    query = db.query(PayrollCycle)

    if college_id:
        query = query.filter(PayrollCycle.college_id == college_id)
    if year:
        query = query.filter(PayrollCycle.year == year)
    if month:
        query = query.filter(PayrollCycle.month == month)

    cycles = query.order_by(PayrollCycle.year.desc(), PayrollCycle.month.desc()).offset(skip).limit(limit).all()
    return cycles


@router.get("/cycles/{cycle_id}", response_model=PayrollCycleResponse)
def get_payroll_cycle(cycle_id: int, db: Session = Depends(get_db)):
    """Get a specific payroll cycle by ID"""
    cycle = db.query(PayrollCycle).filter(PayrollCycle.id == cycle_id).first()
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payroll cycle with ID {cycle_id} not found"
        )
    return cycle


@router.post("/calculate", response_model=PayrollCycleResponse)
def trigger_payroll_calculation(request: PayrollCalculateRequest, db: Session = Depends(get_db)):
    """Trigger payroll calculation for a college/month"""
    if not request.college_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="college_id is required"
        )
    try:
        cycle = run_payroll_calculation(request.college_id, request.year, request.month, db)
        return cycle
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payroll calculation failed: {str(e)}"
        )


@router.post("/cycles/{cycle_id}/lock", response_model=PayrollCycleResponse)
def lock_cycle(cycle_id: int, db: Session = Depends(get_db)):
    """Lock a payroll cycle"""
    try:
        cycle = lock_payroll_cycle(cycle_id, db)
        return cycle
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/entries", response_model=List[PayrollEntryResponse])
def list_payroll_entries(
    payroll_cycle_id: int = None,
    employee_id: int = None,
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db)
):
    """List all payroll entries with filters"""
    query = db.query(PayrollEntry)

    if payroll_cycle_id:
        query = query.filter(PayrollEntry.payroll_cycle_id == payroll_cycle_id)
    if employee_id:
        query = query.filter(PayrollEntry.employee_id == employee_id)

    entries = query.offset(skip).limit(limit).all()
    return entries


@router.get("/entries/{entry_id}", response_model=PayrollEntryResponse)
def get_payroll_entry(entry_id: int, db: Session = Depends(get_db)):
    """Get a specific payroll entry by ID"""
    entry = db.query(PayrollEntry).filter(PayrollEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payroll entry with ID {entry_id} not found"
        )
    return entry


@router.get("/summary", response_model=PayrollSummaryResponse)
def get_payroll_summary(
    college_id: int = None,
    year: int = None,
    month: int = None,
    db: Session = Depends(get_db)
):
    """Get payroll summary for a specific period"""
    from decimal import Decimal
    from sqlalchemy import func

    query = db.query(PayrollEntry).join(PayrollCycle)

    if college_id:
        query = query.filter(PayrollCycle.college_id == college_id)
    if year:
        query = query.filter(PayrollCycle.year == year)
    if month:
        query = query.filter(PayrollCycle.month == month)

    result = query.with_entities(
        func.count(PayrollEntry.id).label('total_employees'),
        func.sum(PayrollEntry.gross_earnings).label('total_gross'),
        func.sum(PayrollEntry.total_deductions).label('total_deductions'),
        func.sum(PayrollEntry.net_pay).label('total_net_pay')
    ).first()

    return {
        "total_employees": result.total_employees or 0,
        "total_gross_earnings": result.total_gross or Decimal("0"),
        "total_deductions": result.total_deductions or Decimal("0"),
        "total_net_pay": result.total_net_pay or Decimal("0"),
        "processed_employees": result.total_employees or 0,
        "pending_employees": 0
    }
