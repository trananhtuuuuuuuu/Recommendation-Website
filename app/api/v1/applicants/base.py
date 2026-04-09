from fastapi import APIRouter, Depends, status
from app.schemas.request.user.applicant.applicant_registration_request import applicant_registration_request
from app.schemas.response.applicant.applicant_registration_response import applicant_registration_response
from app.services.applicant_service import ApplicantService
from app.core.provider import InternalProvider # Assuming this is your provider path

router = APIRouter(prefix="/applicants", tags=["Applicants"])


def get_applicant_service(
    provider: InternalProvider = Depends(InternalProvider),
) -> ApplicantService:
    return provider.get_applicant_service()

@router.post(
    "/register", 
    response_model=applicant_registration_response,
    status_code=status.HTTP_201_CREATED
)
async def create_applicant(
    request: applicant_registration_request,
    service: ApplicantService = Depends(get_applicant_service),
):
    """
    Register a new applicant.
    The database session and logic are handled by the Service and UoW.
    """
    return await service.create_applicant(request)