from sqlalchemy import Column, Integer, String, Date
from db import Base
from datetime import date

class Expenses(Base):

    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today(), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    payment_type = Column(String(20), nullable=False)