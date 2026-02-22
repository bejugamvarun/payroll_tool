from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.holiday import HolidayCreate, HolidayUpdate, HolidayResponse, HolidayBulkCreate
from app.models.holidays import Holiday

router = APIRouter(prefix="/holidays", tags=["holidays"])


@router.get("", response_model=List[HolidayResponse])
def list_holidays(
    college_id: int = None,
    year: int = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all holidays with filters"""
    from datetime import date

    query = db.query(Holiday)

    if college_id:
        query = query.filter(Holiday.college_id == college_id)

    if year:
        start_date = date(year, 1, 1)
        end_date = date(year + 1, 1, 1)
        query = query.filter(Holiday.date >= start_date, Holiday.date < end_date)

    holidays = query.offset(skip).limit(limit).all()
    return holidays


@router.get("/{holiday_id}", response_model=HolidayResponse)
def get_holiday(holiday_id: int, db: Session = Depends(get_db)):
    """Get a specific holiday by ID"""
    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not holiday:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holiday with ID {holiday_id} not found"
        )
    return holiday


@router.post("", response_model=HolidayResponse, status_code=status.HTTP_201_CREATED)
def create_holiday(holiday: HolidayCreate, db: Session = Depends(get_db)):
    """Create a new holiday"""
    db_holiday = Holiday(**holiday.model_dump())
    db.add(db_holiday)
    db.commit()
    db.refresh(db_holiday)
    return db_holiday


@router.post("/bulk", response_model=List[HolidayResponse], status_code=status.HTTP_201_CREATED)
def create_holidays_bulk(holidays: HolidayBulkCreate, db: Session = Depends(get_db)):
    """Create multiple holidays in bulk"""
    db_holidays = [Holiday(**holiday.model_dump()) for holiday in holidays.holidays]
    db.add_all(db_holidays)
    db.commit()
    for holiday in db_holidays:
        db.refresh(holiday)
    return db_holidays


@router.put("/{holiday_id}", response_model=HolidayResponse)
def update_holiday(
    holiday_id: int,
    holiday_update: HolidayUpdate,
    db: Session = Depends(get_db)
):
    """Update a holiday"""
    db_holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not db_holiday:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holiday with ID {holiday_id} not found"
        )

    update_data = holiday_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_holiday, key, value)

    db.commit()
    db.refresh(db_holiday)
    return db_holiday


@router.delete("/{holiday_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holiday(holiday_id: int, db: Session = Depends(get_db)):
    """Delete a holiday"""
    db_holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not db_holiday:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holiday with ID {holiday_id} not found"
        )

    db.delete(db_holiday)
    db.commit()
    return None
