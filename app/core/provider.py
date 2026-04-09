from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

# Import your Repositories
from app.repositories.user_repository import UserRepository
from app.repositories.applicant_repository import ApplicantRepository

# Import your Services
from app.services.user_service import UserService
from app.services.applicant_service import ApplicantService

# Import your Unit of Work
from app.core.uow import UnitOfWork

class InternalProvider:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    # --- Unit of Work ---
    def get_uow(self) -> UnitOfWork:
        return UnitOfWork(self.db)

    # --- Repositories ---
    def get_user_repository(self) -> UserRepository:
        return UserRepository(self.db)

    def get_applicant_repository(self) -> ApplicantRepository:
        return ApplicantRepository(self.db)

    # --- Services ---
    def get_user_service(self) -> UserService:
        return UserService(uow=self.get_uow())

    def get_applicant_service(self) -> ApplicantService:
        return ApplicantService(uow=self.get_uow())