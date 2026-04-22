from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship
from datetime import date
from db import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_date = Column(DateTime, default=date.today(), nullable=False)
    month = Column(String(255), nullable=False)
    payment_type = Column(String(255), nullable=False)
    payment_persent = Column(Float, nullable=True)
    discount = Column(Integer, nullable=True)

    student = relationship("Students", back_populates="payments")

    group = relationship("Groups", back_populates="payments")
