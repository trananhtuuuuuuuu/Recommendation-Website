# app/models/recruiter.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.base import Base

class Recruiter(Base):
    __tablename__ = "recruiter"

    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    company_name = Column(String)
    opening_date = Column(Date)

    user = relationship("User", back_populates="recruiter")
    jobs = relationship("JobDescription", back_populates="recruiter")