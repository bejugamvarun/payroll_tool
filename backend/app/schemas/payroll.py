from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal
from app.models.payroll_cycles import PayrollCycleStatus
from app.models.salary_components import ComponentType


class PayrollCycleResponse(BaseModel):
    id: int
    college_id: int
    year: int
    month: int
    total_working_days: int
    status: PayrollCycleStatus
    created_at: datetime
    updated_at: datetime
    locked_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PayrollEntryComponentResponse(BaseModel):
    id: int
    payroll_entry_id: int
    salary_component_id: int
    component_type: ComponentType
    amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PayrollEntryResponse(BaseModel):
    id: int
    payroll_cycle_id: int
    employee_id: int
    days_present: Decimal
    days_absent: Decimal
    paid_leaves_used: Decimal
    comp_leaves_used: Decimal
    unpaid_leaves: Decimal
    loss_of_pay: Decimal
    gross_earnings: Decimal
    total_deductions: Decimal
    net_pay: Decimal
    created_at: datetime
    components: list[PayrollEntryComponentResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PayrollCalculateRequest(BaseModel):
    college_id: Optional[int] = None
    year: int
    month: int
    employee_ids: Optional[list[int]] = None


class PayrollSummaryResponse(BaseModel):
    total_employees: int
    total_gross_earnings: Decimal
    total_deductions: Decimal
    total_net_pay: Decimal
    processed_employees: int
    pending_employees: int
