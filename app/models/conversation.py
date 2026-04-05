# app/models/conversation.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from app.db.base import Base

class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id"))

    created_at = Column(DateTime, default=datetime.utcnow)