from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal


class LeaveBalanceBase(BaseModel):
    employee_id: int
    year: int
    paid_leaves_total: Decimal
    paid_leaves_used: Decimal = Decimal("0")
    comp_leaves_earned: Decimal = Decimal("0")
    comp_leaves_used: Decimal = Decimal("0")
    carry_forward_leaves: Decimal = Decimal("0")


class LeaveBalanceCreate(LeaveBalanceBase):
    pass


class LeaveBalanceUpdate(BaseModel):
    paid_leaves_used: Optional[Decimal] = None
    comp_leaves_earned: Optional[Decimal] = None
    comp_leaves_used: Optional[Decimal] = None


class LeaveBalanceResponse(LeaveBalanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
