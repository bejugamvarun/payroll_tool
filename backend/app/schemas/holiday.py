from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional


class HolidayBase(BaseModel):
    college_id: int
    date: date
    name: str
    is_optional: bool = False


class HolidayCreate(HolidayBase):
    pass


class HolidayUpdate(BaseModel):
    name: Optional[str] = None
    is_optional: Optional[bool] = None


class HolidayResponse(HolidayBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HolidayBulkCreate(BaseModel):
    holidays: list[HolidayCreate]
