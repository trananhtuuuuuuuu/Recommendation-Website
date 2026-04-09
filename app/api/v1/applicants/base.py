from fastapi import APIRouter, Depends, status
from app.schemas.request.user.applicant import ApplicantRegistrationRequest
from app.schemas.response.applicant import ApplicantRegistrationResponse
from app.services.applicant_service import ApplicantService
from app.core.provider import InternalProvider # Assuming this is your provider path

router = APIRouter(prefix="/applicants", tags=["Applicants"])

@router.post(
    "/register", 
    response_model=ApplicantRegistrationResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_applicant(
    request: ApplicantRegistrationRequest, 
    service: ApplicantService = Depends(InternalProvider().get_applicant_service)
):
    """
    Register a new applicant.
    The database session and logic are handled by the Service and UoW.
    """
    return await service.create_applicant(request)