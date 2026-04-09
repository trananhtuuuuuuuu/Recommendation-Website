from sqlalchemy.orm import Session

from app.repositories.applicant_repository import ApplicantRepository
from app.repositories.user_repository import UserRepository


class UnitOfWork:
	def __init__(self, db: Session):
		self.db = db
		self.users = UserRepository(db)
		self.applicants = ApplicantRepository(db)

	async def __aenter__(self):
		return self

	async def __aexit__(self, exc_type, exc, tb):
		if exc:
			await self.rollback()

	async def commit(self):
		self.db.commit()

	async def rollback(self):
		self.db.rollback()
