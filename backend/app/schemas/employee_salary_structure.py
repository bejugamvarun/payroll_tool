from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


class SalaryStructureBase(BaseModel):
    employee_id: int
    salary_component_id: int
    amount: Decimal
    effective_from: date
    effective_to: Optional[date] = None


class SalaryStructureCreate(SalaryStructureBase):
    pass


class SalaryStructureUpdate(BaseModel):
    amount: Optional[Decimal] = None
    effective_to: Optional[date] = None


class SalaryStructureResponse(SalaryStructureBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SalaryStructureBulkCreate(BaseModel):
    structures: list[SalaryStructureCreate]


class SalaryStructureBulkUpdate(BaseModel):
    structure_id: int
    amount: Optional[Decimal] = None
    effective_to: Optional[date] = None
