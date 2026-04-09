from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.job_description import JobDescription


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_active_jobs(self, now: datetime) -> list[JobDescription]:
        return (
            self.db.query(JobDescription)
            .filter(JobDescription.start_date <= now)
            .filter(or_(JobDescription.end_date.is_(None), JobDescription.end_date >= now))
            .all()
        )
