from pydantic import BaseModel
from datetime import date

class ReceptionData(BaseModel):
    full_name: str
    visit_date: date
    phone_number: str
    secondary_phone: str
    source: str
    course: str
    free_days: list
    free_times: list
    address: str
    status: str
    additional_info: str


class CreateReception(ReceptionData):
    pass


class UpdateReception(ReceptionData):
    id: int
