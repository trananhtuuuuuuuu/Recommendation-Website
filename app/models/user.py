# app/models/user.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True)
    user_name = Column(String)
    password = Column(String)

    refresh_token = Column(String)
    access_token = Column(String)

    role_id = Column(Integer, ForeignKey("role.id"))

    role = relationship("Role", back_populates="users")
    recruiter = relationship("Recruiter", back_populates="user", uselist=False)
    applicant = relationship("Applicant", back_populates="user", uselist=False)