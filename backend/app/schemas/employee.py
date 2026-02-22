from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    college_id: int
    department_id: int
    designation_id: int
    date_of_joining: date
    date_of_leaving: Optional[date] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    pan_number: Optional[str] = None
    ctc: Decimal
    monthly_gross: Decimal
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    date_of_leaving: Optional[date] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    pan_number: Optional[str] = None
    ctc: Optional[Decimal] = None
    monthly_gross: Optional[Decimal] = None
    is_active: Optional[bool] = None


class EmployeeResponse(EmployeeBase):
    id: int
    college_name: Optional[str] = None
    department_name: Optional[str] = None
    designation_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployeeBulkCreate(BaseModel):
    employees: list[EmployeeCreate]


class EmployeeBulkUploadResponse(BaseModel):
    total: int
    successful: int
    failed: int
    errors: list[dict]
