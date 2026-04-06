from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, Field
import re
from datetime import datetime
from app.models.enums import ApplicantStatus, GenderEnum

class applicant_registration_request(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    gender: Optional[GenderEnum] = None
    phone_number: str = Field(..., pattern=r"^\+?1?\d{9,15}$")
    email: EmailStr
    user_name: str = Field(..., min_length=4)
    password: str = Field(..., min_length=8, max_length=72)
    address: str
    date_of_birth: Optional[str] = None
    applicant_status: ApplicantStatus = ApplicantStatus.Archived

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v) > 72:
            raise ValueError("Password is too long (max 72 characters for security reasons)")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        return v

    @field_validator('date_of_birth')
    @classmethod
    def validate_dob_format(cls, v: Optional[str]):
        if v:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date of birth must be in YYYY-MM-DD format")
        return v