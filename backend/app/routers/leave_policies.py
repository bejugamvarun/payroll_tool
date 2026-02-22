from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.leave_policy import LeavePolicyCreate, LeavePolicyUpdate, LeavePolicyResponse
from app.models.leave_policies import LeavePolicy

router = APIRouter(prefix="/leave-policies", tags=["leave-policies"])


@router.get("", response_model=List[LeavePolicyResponse])
def list_leave_policies(
    college_id: int = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all leave policies with optional college filter"""
    query = db.query(LeavePolicy)
    if college_id:
        query = query.filter(LeavePolicy.college_id == college_id)
    policies = query.offset(skip).limit(limit).all()
    return policies


@router.get("/{policy_id}", response_model=LeavePolicyResponse)
def get_leave_policy(policy_id: int, db: Session = Depends(get_db)):
    """Get a specific leave policy by ID"""
    policy = db.query(LeavePolicy).filter(LeavePolicy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave policy with ID {policy_id} not found"
        )
    return policy


@router.post("", response_model=LeavePolicyResponse, status_code=status.HTTP_201_CREATED)
def create_leave_policy(policy: LeavePolicyCreate, db: Session = Depends(get_db)):
    """Create a new leave policy"""
    db_policy = LeavePolicy(**policy.model_dump())
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy


@router.put("/{policy_id}", response_model=LeavePolicyResponse)
def update_leave_policy(
    policy_id: int,
    policy_update: LeavePolicyUpdate,
    db: Session = Depends(get_db)
):
    """Update a leave policy"""
    db_policy = db.query(LeavePolicy).filter(LeavePolicy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave policy with ID {policy_id} not found"
        )

    update_data = policy_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_policy, key, value)

    db.commit()
    db.refresh(db_policy)
    return db_policy


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave_policy(policy_id: int, db: Session = Depends(get_db)):
    """Delete a leave policy"""
    db_policy = db.query(LeavePolicy).filter(LeavePolicy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Leave policy with ID {policy_id} not found"
        )

    db.delete(db_policy)
    db.commit()
    return None
