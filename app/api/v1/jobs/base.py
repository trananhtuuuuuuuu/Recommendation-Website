from fastapi import APIRouter, Depends

from app.core.provider import InternalProvider
from app.schemas.response.job_response import JobResponse
from app.services.job_service import JobService

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])


def get_job_service(provider: InternalProvider = Depends(InternalProvider)) -> JobService:
    return provider.get_job_service()


@router.get("", response_model=list[JobResponse])
async def get_active_jobs(service: JobService = Depends(get_job_service)):
    return await service.get_active_jobs()
