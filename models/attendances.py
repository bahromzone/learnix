from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from db import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Boolean, nullable=False)

    student = relationship("Students", back_populates="attendances")

    group = relationship("Groups", back_populates="attendances")
