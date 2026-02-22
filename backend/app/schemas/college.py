from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class CollegeBase(BaseModel):
    serial_number: int
    college_code: str
    name: str
    address: Optional[str] = None


class CollegeCreate(CollegeBase):
    pass


class CollegeUpdate(BaseModel):
    serial_number: Optional[int] = None
    college_code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None


class CollegeResponse(CollegeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CollegeBulkCreate(BaseModel):
    colleges: list[CollegeCreate]


class CollegeBulkUpdate(BaseModel):
    college_id: int
    serial_number: Optional[int] = None
    college_code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
