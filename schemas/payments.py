from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class PaymentType(str, Enum):
    CASH = "cash"
    CLICK = "click"

class Month(str, Enum):
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"

class PaymentCreate(BaseModel):
    student_id: int
    group_id: int
    amount: int = Field(ge=0)
    month: Month
    payment_type: PaymentType
    payment_date: date = date.today()
    discount: int = Field(ge=0, le=10, default=10)

class PaymentUpdate(BaseModel):
    amount: int = Field(gt=0)
    payment_type: PaymentType
