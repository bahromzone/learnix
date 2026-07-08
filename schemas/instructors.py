from typing import List, Optional
from pydantic import BaseModel


class InstructorCourse(BaseModel):
    id: int
    name: str


class InstructorGroup(BaseModel):
    id: int
    name: str
    period: int
    status: str
    course_id: int
    course_name: str
    student_count: int


class InstructorProfile(BaseModel):
    id: int
    full_name: str
    image: Optional[str] = None
    courses: List[InstructorCourse]
    groups: List[InstructorGroup]
    total_groups: int
    total_students: int
