from pydantic import BaseModel, Field
from datetime import date
from schemas.payments import PaymentType


class ExpenseBase(BaseModel):
    date: date
    amount: int = Field(gt=0)
    description: str
    category: str
    payment_type: PaymentType


class CreateExpense(ExpenseBase):
    pass


class UpdateExpense(ExpenseBase):
    ident: int