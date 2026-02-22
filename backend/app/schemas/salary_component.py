from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.salary_components import ComponentType


class SalaryComponentBase(BaseModel):
    name: str
    component_type: ComponentType
    is_default: bool = False
    description: Optional[str] = None


class SalaryComponentCreate(SalaryComponentBase):
    pass


class SalaryComponentUpdate(BaseModel):
    name: Optional[str] = None
    component_type: Optional[ComponentType] = None
    is_default: Optional[bool] = None
    description: Optional[str] = None


class SalaryComponentResponse(SalaryComponentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
