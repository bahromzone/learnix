from pydantic import BaseModel

class SchemaInfo(BaseModel):
    student_id: int
    parent_name: str
    parent_phone: str
    address: str
