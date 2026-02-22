from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ReportGenerateRequest(BaseModel):
    college_id: Optional[int] = None
    year: int
    month: int
    report_type: str


class ReportResponse(BaseModel):
    id: int
    college_id: Optional[int] = None
    year: int
    month: int
    report_type: str
    file_path: str
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
