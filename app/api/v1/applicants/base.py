from fastapi import APIRouter, Depends, status
from app.schemas.request.user.applicant.applicant_login_request import applicant_login_request
from app.schemas.request.user.applicant.applicant_registration_request import applicant_registration_request
from app.schemas.request.user.applicant.applicant_refresh_token_request import applicant_refresh_token_request
from app.schemas.response.applicant.applicant_registration_response import applicant_registration_response
from app.schemas.response.user_login_response import user_login_response
from app.core.provider import get_applicant_service
from app.services.applicant_service import ApplicantService

router = APIRouter(prefix="/applicants", tags=["Applicants"])



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


@router.post(
    "/login",
    response_model=user_login_response,
    status_code=status.HTTP_200_OK,
)
async def login_applicant(
    request: applicant_login_request,
    service: ApplicantService = Depends(get_applicant_service),
):
    return await service.login_applicant(request)


@router.post(
    "/refresh-token",
    response_model=user_login_response,
    status_code=status.HTTP_200_OK,
)
async def refresh_applicant_token(
    request: applicant_refresh_token_request,
    service: ApplicantService = Depends(get_applicant_service),
):
    return await service.refresh_applicant_token(request)