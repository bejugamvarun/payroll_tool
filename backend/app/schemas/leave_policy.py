from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LeavePolicyBase(BaseModel):
    college_id: int
    name: str
    paid_leaves_per_year: int
    max_carry_forward: int = 0
    comp_leave_enabled: bool = True


class LeavePolicyCreate(LeavePolicyBase):
    pass


class LeavePolicyUpdate(BaseModel):
    name: str
    paid_leaves_per_year: int
    max_carry_forward: int
    comp_leave_enabled: bool


class LeavePolicyResponse(LeavePolicyBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
