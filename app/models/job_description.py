# app/models/job.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class JobDescription(Base):
    __tablename__ = "job_description"

    id = Column(Integer, primary_key=True)

    job_name = Column(String)
    about_job = Column(String)
    responsibilities = Column(String)
    requirements = Column(String)
    benefit = Column(String)

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    recruiter_id = Column(Integer, ForeignKey("recruiter.id"))

    recruiter = relationship("Recruiter", back_populates="jobs")
    applicants = relationship("ApplicantJD", back_populates="job")