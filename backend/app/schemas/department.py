from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DepartmentBase(BaseModel):
    college_id: int
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
