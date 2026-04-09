from pydantic import BaseModel, Field


class applicant_refresh_token_request(BaseModel):
    refresh_token: str | None = Field(default=None, min_length=20)
