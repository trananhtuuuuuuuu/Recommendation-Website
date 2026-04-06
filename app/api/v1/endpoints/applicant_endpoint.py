from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.request.user.applicant.applicant_registration_request import applicant_registration_request
from app.schemas.response.applicant.applicant_registration_response import applicant_registration_response
from app.services.applicant_service import ApplicantService

router = APIRouter()

@router.post("/register", response_model=applicant_registration_response, status_code=status.HTTP_201_CREATED)
def create_applicant(request: applicant_registration_request, db: Session = Depends(get_db)):
    """
    Endpoint to register a new applicant. 
    Pydantic handles the format validation before this code runs.
    """
    
    # Call the service layer to handle hashing and database persistence
    new_applicant = ApplicantService.create_applicant(db=db, request=request)
    
    return new_applicant