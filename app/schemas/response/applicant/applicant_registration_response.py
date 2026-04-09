from typing import Optional
from app.models.enums import ApplicantStatus, GenderEnum
from pydantic import BaseModel, ConfigDict


class applicant_registration_response(BaseModel):
    full_name: str
    gender: Optional[GenderEnum] = None
    phone_number: str
    email: str
    user_name: str
    address: str
    date_of_birth: str
    applicant_status: ApplicantStatus

    model_config = ConfigDict(from_attributes=True)