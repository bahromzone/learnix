from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class StudentStatus(str, Enum):
    active = "active"
    graduated = "graduated"
    inactive = "inactive"

class StudentBase(BaseModel):
    full_name: str
    group_id: int
    discount: int = Field(ge=0, le=100)
    phone_number: int
    started_date: date

class UpdateStatus(BaseModel):
    student_id: int
    status: StudentStatus

class CreateStudent(StudentBase):
    pass

class UpdateStudent(StudentBase):
    pass