from app.core.exceptions.business import DuplicateResourceException
from app.core.uow import UnitOfWork
from app.mappers.mapper_applicant import MapperApplicant
from app.schemas.request.user.applicant.applicant_registration_request import ApplicantRegistrationRequest

class ApplicantService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_applicant(self, request: ApplicantRegistrationRequest):
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