from sqlalchemy import Column, Integer, String, Date, Text, JSON
from db import Base

class Reception(Base):
    __tablename__ = 'reception'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    visit_date = Column(Date, nullable=False)
    phone_number = Column(String(30), nullable=False)
    secondary_phone = Column(String(30), nullable=True)
    source = Column(String(100), nullable=False)
    course = Column(String(50), nullable=False)
    free_days = Column(JSON, nullable=False)
    free_times = Column(JSON, nullable=False)
    address = Column(String(255), nullable=False)
    status = Column(String(100), nullable=True)
    additional_info = Column(Text, nullable=True)