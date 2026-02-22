from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.salary_component import (
    SalaryComponentCreate,
    SalaryComponentUpdate,
    SalaryComponentResponse
)
from app.models.salary_components import SalaryComponent

router = APIRouter(prefix="/salary-components", tags=["salary-components"])


@router.get("", response_model=List[SalaryComponentResponse])
def list_salary_components(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all salary components"""
    components = db.query(SalaryComponent).offset(skip).limit(limit).all()
    return components


@router.get("/{component_id}", response_model=SalaryComponentResponse)
def get_salary_component(component_id: int, db: Session = Depends(get_db)):
    """Get a specific salary component by ID"""
    component = db.query(SalaryComponent).filter(SalaryComponent.id == component_id).first()
    if not component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salary component with ID {component_id} not found"
        )
    return component


@router.post("", response_model=SalaryComponentResponse, status_code=status.HTTP_201_CREATED)
def create_salary_component(component: SalaryComponentCreate, db: Session = Depends(get_db)):
    """Create a new salary component"""
    db_component = SalaryComponent(**component.model_dump())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component


@router.put("/{component_id}", response_model=SalaryComponentResponse)
def update_salary_component(
    component_id: int,
    component_update: SalaryComponentUpdate,
    db: Session = Depends(get_db)
):
    """Update a salary component"""
    db_component = db.query(SalaryComponent).filter(SalaryComponent.id == component_id).first()
    if not db_component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salary component with ID {component_id} not found"
        )

    update_data = component_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_component, key, value)

    db.commit()
    db.refresh(db_component)
    return db_component


@router.delete("/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_salary_component(component_id: int, db: Session = Depends(get_db)):
    """Delete a salary component"""
    db_component = db.query(SalaryComponent).filter(SalaryComponent.id == component_id).first()
    if not db_component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salary component with ID {component_id} not found"
        )

    db.delete(db_component)
    db.commit()
    return None
