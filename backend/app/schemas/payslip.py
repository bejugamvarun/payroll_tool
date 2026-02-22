from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PayslipResponse(BaseModel):
    id: int
    payroll_entry_id: int
    employee_id: int
    payroll_cycle_id: int
    file_path: str
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
