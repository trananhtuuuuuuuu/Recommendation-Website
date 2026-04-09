from pydantic import BaseModel, Field


class applicant_login_request(BaseModel):
    identifier: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8, max_length=72)
