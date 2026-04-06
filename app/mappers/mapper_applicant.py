from datetime import datetime
from app.models.user import User
from app.models.applicant import Applicant
from app.schemas.request.user.applicant.applicant_registration_request import applicant_registration_request
from app.schemas.response.applicant.applicant_registration_response import applicant_registration_response


class MapperApplicant:
    
    @staticmethod
    def map_request_to_entity(request: applicant_registration_request) -> Applicant:
        """
        Maps the flat registration request into a nested Entity structure (User + Applicant).
        """
        # 1. Create the User portion of the entity
        user_entity = User(
            address=request.address,
            phone_number=request.phone_number,
            email=request.email,
            user_name=request.user_name,
            password=request.password,  # Note: In a real app, hash this first!
        )

        # 2. Create the Applicant portion and link the user
        # Handle date conversion if date_of_birth is a string
        dob = None
        if request.date_of_birth:
            try:
                dob = datetime.strptime(request.date_of_birth, "%Y-%m-%d").date()
            except ValueError:
                dob = None

        applicant_entity = Applicant(
            full_name=request.full_name,
            gender=request.gender,
            applicant_status=request.applicant_status,
            data_of_birth=dob,
            user=user_entity  # SQLAlchemy handles the ID linking automatically here
        )
        
        return applicant_entity

    @staticmethod
    def map_entity_to_response(applicant: Applicant) -> applicant_registration_response:
        """
        Flattens the Entity (Applicant + User) into a single Response DTO.
        """
        return applicant_registration_response(
            full_name=applicant.full_name,
            gender=applicant.gender,
            phone_number=applicant.user.phone_number,
            email=applicant.user.email,
            user_name=applicant.user.user_name,
            address=applicant.user.address,
            date_of_birth=str(applicant.data_of_birth) if applicant.data_of_birth else "",
            applicant_status=applicant.applicant_status
        )