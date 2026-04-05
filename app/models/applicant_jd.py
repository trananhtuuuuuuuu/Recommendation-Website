# app/models/applicant_jd.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ApplicantJD(Base):
    __tablename__ = "applicant_jd"

    id = Column(Integer, primary_key=True)

    applicant_id = Column(Integer, ForeignKey("applicant.id"))
    jd_id = Column(Integer, ForeignKey("job_description.id"))

    applicant = relationship("Applicant", back_populates="applications")
    job = relationship("JobDescription", back_populates="applicants")