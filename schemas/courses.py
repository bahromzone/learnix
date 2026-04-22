from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    name: str
    period: int = Field(..., gt=0)
    price: int = Field(..., gt=0)
    course_id: int
    teacher_id: int


class CreateGroup(GroupBase):
    pass


class UpdateGroup(GroupBase):
    pass
