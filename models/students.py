from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Students(Base):

    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    phone_number = Column(Integer, nullable=False)
    started_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    discount = Column(Integer, nullable=False)
    payment_amount = Column(Integer, nullable=False)

    group = relationship("Groups", back_populates="student")

    attendances = relationship("Attendance", back_populates="student")

    payments = relationship("Payment", back_populates="student")

    info = relationship("Info", back_populates="student")