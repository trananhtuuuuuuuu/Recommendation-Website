from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    async def get_by_email_or_username(self, identifier: str):
        return (
            self.db.query(User)
            .filter(or_(User.email == identifier, User.user_name == identifier))
            .first()
        )

    async def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    async def update_tokens(self, user_id: int, access_token: str, refresh_token: str):
        user = await self.get_by_id(user_id)
        if user is None:
            return None
        user.access_token = access_token
        user.refresh_token = refresh_token
        self.db.flush()
        return user
