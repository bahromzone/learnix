from pydantic import BaseModel
from datetime import date

class AttendanceBase(BaseModel):
    date: date
    student_id: int
    group_id: int
    description: str
    status: bool


class CreateAttendance(AttendanceBase):
    pass

class UpdateAttendance(AttendanceBase):
    pass