from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Greeting(Base):
    __tablename__ = "greetings"

    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String, nullable=False)
    recipient_name = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    link_token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.timezone.utc)

    chat_messages = relationship("ChatMessage", back_populates = "greeting", cascade = "all, delete-orphan")