from pydantic import BaseModel


class user_login_response(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = "bearer"
