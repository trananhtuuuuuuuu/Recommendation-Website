# app/models/cv.py
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Cv(Base):
    __tablename__ = "cv"

    id = Column(Integer, primary_key=True)

    full_name = Column(String)
    address = Column(String)
    phone_number = Column(String)

    objective = Column(String)
    skill = Column(String)
    gpa = Column(Float)
    experience = Column(String)
    education = Column(String)
    certificate = Column(String)

    applicant = relationship("Applicant", back_populates="cv", uselist=False)