from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.college import (
    CollegeCreate,
    CollegeUpdate,
    CollegeResponse,
    CollegeBulkCreate,
)
from app.models.colleges import College

router = APIRouter(prefix="/colleges", tags=["colleges"])


@router.get("", response_model=List[CollegeResponse])
def list_colleges(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all colleges with pagination"""
    colleges = db.query(College).offset(skip).limit(limit).all()
    return colleges


@router.get("/{college_id}", response_model=CollegeResponse)
def get_college(college_id: int, db: Session = Depends(get_db)):
    """Get a specific college by ID"""
    college = db.query(College).filter(College.id == college_id).first()
    if not college:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"College with ID {college_id} not found"
        )
    return college


@router.post("", response_model=CollegeResponse, status_code=status.HTTP_201_CREATED)
def create_college(college: CollegeCreate, db: Session = Depends(get_db)):
    """Create a new college"""
    db_college = College(**college.model_dump())
    db.add(db_college)
    db.commit()
    db.refresh(db_college)
    return db_college


@router.post("/bulk", response_model=List[CollegeResponse], status_code=status.HTTP_201_CREATED)
def create_colleges_bulk(colleges: CollegeBulkCreate, db: Session = Depends(get_db)):
    """Create multiple colleges in bulk"""
    db_colleges = [College(**college.model_dump()) for college in colleges.colleges]
    db.add_all(db_colleges)
    db.commit()
    for college in db_colleges:
        db.refresh(college)
    return db_colleges


@router.put("/{college_id}", response_model=CollegeResponse)
def update_college(
    college_id: int,
    college_update: CollegeUpdate,
    db: Session = Depends(get_db)
):
    """Update a college"""
    db_college = db.query(College).filter(College.id == college_id).first()
    if not db_college:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"College with ID {college_id} not found"
        )

    update_data = college_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_college, key, value)

    db.commit()
    db.refresh(db_college)
    return db_college


@router.delete("/{college_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_college(college_id: int, db: Session = Depends(get_db)):
    """Delete a college"""
    db_college = db.query(College).filter(College.id == college_id).first()
    if not db_college:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"College with ID {college_id} not found"
        )

    db.delete(db_college)
    db.commit()
    return None
