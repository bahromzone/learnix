from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base
from sqlalchemy.orm import relationship


class Info(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_name = Column(String(50), nullable=False)
    parent_phone = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)

    student = relationship("Students", back_populates="info")


