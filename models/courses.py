from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base
from sqlalchemy.orm import relationship

class Courses(Base):

    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    image = Column(String(255), nullable=True)

    group = relationship("Groups", back_populates="course")


class Groups(Base):

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    period = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    status = Column(String(50), nullable=False)


    course = relationship("Courses", back_populates="group")

    teacher = relationship("Users", back_populates="group")

    attendances = relationship("Attendance", back_populates="group")

    payments = relationship("Payment", back_populates="group")

    student = relationship("Students", back_populates="group")
