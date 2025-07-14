from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    greeting_id = Column(Integer, ForeignKey("greetings.id", ondelete="CASCADE"))
    sender = Column(String, nullable=False)  # "bot" or "user"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    greeting = relationship("Greeting", back_populates="chat_messages")
