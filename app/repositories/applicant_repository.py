from app.models.user import User
from app.models.applicant import Applicant
from sqlalchemy.orm import Session
from sqlalchemy import or_

class ApplicantRepository:
    def __init__(self, applicant_repository: Session):
        self.applicant_repository = applicant_repository

    def add(self, entity: Applicant):
        self.applicant_repository.add(entity)

    async def get_by_email_or_username(self, email: str, username: str):
        # Logic move here from the service
        return self.applicant_repository.query(User).filter(
            or_(User.email == email, User.user_name == username)
        ).first()

    async def save(self, entity: Applicant):
        try:
            self.applicant_repository.add(entity)
            self.applicant_repository.commit()
            self.applicant_repository.refresh(entity)
            return entity
        except Exception:
            self.applicant_repository.rollback()
            raise # Re-raise to be caught by global exception handler