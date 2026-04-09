from fastapi import HTTPException, status

from app.core.exceptions.business import DuplicateResourceException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from app.core.uow import UnitOfWork
from app.mappers.mapper_applicant import MapperApplicant
from app.schemas.request.user.applicant.applicant_login_request import applicant_login_request
from app.schemas.request.user.applicant.applicant_registration_request import applicant_registration_request
from app.schemas.response.user_login_response import user_login_response

class ApplicantService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_applicant(self, request: applicant_registration_request):
        # 1. Use the UoW to check for existing users
        existing = await self.uow.users.get_by_email(request.email)
        
        if existing:
            raise DuplicateResourceException("Email already in use", status_code=409)
          
        # 2. Logic & Mapping
        entity = MapperApplicant.map_request_to_entity(request)
        
        # 3. Save via UoW (Transaction management)
        async with self.uow:
            self.uow.applicants.add(entity)
            await self.uow.commit()
        
        return MapperApplicant.map_entity_to_response(entity)

    async def login_applicant(self, request: applicant_login_request) -> user_login_response:
        
        user = await self.uow.users.get_by_email_or_username(request.identifier)
        if user is None or not verify_password(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        applicant = await self.uow.applicants.get_by_user_id(user.id)
        if applicant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Applicant account not found")

        access_token = create_access_token(subject=str(user.id), additional_claims={"email": user.email})
        refresh_token = create_refresh_token(subject=str(user.id))

        async with self.uow:
            await self.uow.users.update_tokens(
                user_id=user.id,
                access_token=access_token,
                refresh_token=refresh_token,
            )
            await self.uow.commit()

        return user_login_response(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_applicant_token(self, refresh_token: str) -> user_login_response:
        try:
            payload = decode_refresh_token(refresh_token)
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")
            user_id = int(payload.get("sub"))
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

        user = await self.uow.users.get_by_id(user_id)
        if user is None or user.refresh_token != refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is not recognized")

        new_access_token = create_access_token(subject=str(user.id), additional_claims={"email": user.email})
        new_refresh_token = create_refresh_token(subject=str(user.id))

        async with self.uow:
            await self.uow.users.update_tokens(
                user_id=user.id,
                access_token=new_access_token,
                refresh_token=new_refresh_token,
            )
            await self.uow.commit()

        return user_login_response(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    async def logout_applicant(self, refresh_token: str) -> None:
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

        user = await self.uow.users.get_by_refresh_token(refresh_token)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session not found")

        async with self.uow:
            await self.uow.users.clear_tokens(user.id)
            await self.uow.commit()