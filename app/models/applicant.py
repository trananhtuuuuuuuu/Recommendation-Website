# app/models/applicant.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import GenderEnum, ApplicantStatus

class Applicant(Base):
    __tablename__ = "applicant"

    id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    applicant_status = Column(Enum(ApplicantStatus))
    gender = Column(Enum(GenderEnum))
    full_name = Column(String)
    data_of_birth = Column(Date, nullable=True)

    cv_id = Column(Integer, ForeignKey("cv.id"), nullable=True)

    user = relationship("User", back_populates="applicant")
    cv = relationship("Cv", back_populates="applicant")
    applications = relationship("ApplicantJD", back_populates="applicant")