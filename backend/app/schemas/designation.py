from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class DesignationBase(BaseModel):
    name: str
    college_id: Optional[int] = None


class DesignationCreate(DesignationBase):
    pass


class DesignationUpdate(BaseModel):
    name: str


class DesignationResponse(DesignationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
