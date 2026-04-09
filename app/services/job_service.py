from datetime import datetime, timezone

from app.repositories.job_repository import JobRepository


class JobService:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    async def get_active_jobs(self):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return await self.job_repository.get_active_jobs(now=now)
