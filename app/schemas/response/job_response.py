from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
    id: int
    job_name: str | None = None
    about_job: str | None = None
    responsibilities: str | None = None
    requirements: str | None = None
    benefit: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    recruiter_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
