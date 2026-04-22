from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, String, Integer


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)
    phone_number = Column(Integer, nullable=False)

    group = relationship("Groups", back_populates="teacher")