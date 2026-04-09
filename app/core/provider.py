from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

# Import repositories
from app.repositories.applicant_repository import ApplicantRepository
from app.repositories.job_repository import JobRepository

# Import services
from app.services.applicant_service import ApplicantService
from app.services.job_service import JobService

# Import unit of work
from app.core.uow import UnitOfWork

class InternalProvider:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # --- Unit of Work ---
    def get_uow(self) -> UnitOfWork:
        return UnitOfWork(self.db)

    # --- Repositories ---
    def get_applicant_repository(self) -> ApplicantRepository:
        return ApplicantRepository(self.db)

    def get_job_repository(self) -> JobRepository:
        return JobRepository(self.db)

    # --- Services ---
    def get_applicant_service(self) -> ApplicantService:
        return ApplicantService(uow=self.get_uow())

    def get_job_service(self) -> JobService:
        return JobService(job_repository=self.get_job_repository())