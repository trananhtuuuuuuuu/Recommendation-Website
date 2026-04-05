# app/models/message.py

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String
from datetime import datetime
from app.db.base import Base

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)

    conversation_id = Column(Integer, ForeignKey("conversation.id"))

    role = Column(String)  
    # "user" or "assistant"

    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)