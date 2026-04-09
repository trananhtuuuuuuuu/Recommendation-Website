import os

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from app.schemas.request.user.applicant.applicant_login_request import applicant_login_request
from app.schemas.request.user.applicant.applicant_registration_request import applicant_registration_request
from app.schemas.request.user.applicant.applicant_refresh_token_request import applicant_refresh_token_request
from app.schemas.response.applicant.applicant_registration_response import applicant_registration_response
from app.schemas.response.user_login_response import user_login_response
from app.core.provider import get_applicant_service
from app.services.applicant_service import ApplicantService

router = APIRouter(prefix="/applicants", tags=["Applicants"])

REFRESH_COOKIE_KEY = "refresh_token"


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    is_secure_cookie = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    response.set_cookie(
        key=REFRESH_COOKIE_KEY,
        value=refresh_token,
        httponly=True,
        secure=is_secure_cookie,
        samesite="lax",
        path="/",
        max_age=7 * 24 * 60 * 60,
    )



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
    response: Response,
    request: applicant_login_request,
    service: ApplicantService = Depends(get_applicant_service),
):
    token_payload = await service.login_applicant(request)
    _set_refresh_cookie(response, token_payload.refresh_token)
    return token_payload


@router.post(
    "/refresh-token",
    response_model=user_login_response,
    status_code=status.HTTP_200_OK,
)
async def refresh_applicant_token(
    response: Response,
    http_request: Request,
    request: applicant_refresh_token_request | None = None,
    service: ApplicantService = Depends(get_applicant_service),
):
    cookie_refresh_token = http_request.cookies.get(REFRESH_COOKIE_KEY)
    body_refresh_token = request.refresh_token if request else None
    resolved_refresh_token = cookie_refresh_token or body_refresh_token

    if not resolved_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    token_payload = await service.refresh_applicant_token(resolved_refresh_token)
    _set_refresh_cookie(response, token_payload.refresh_token)
    return token_payload


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_applicant(
    response: Response,
    http_request: Request,
    service: ApplicantService = Depends(get_applicant_service),
):
    refresh_token = http_request.cookies.get(REFRESH_COOKIE_KEY)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    await service.logout_applicant(refresh_token)
    response.delete_cookie(key=REFRESH_COOKIE_KEY, path="/")
    return None