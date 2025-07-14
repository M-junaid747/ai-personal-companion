from pydantic import BaseModel
from datetime import datetime

class ChatMessageBase(BaseModel):
    sender: str
    content: str

class ChatMessageCreate(ChatMessageBase):
    greeting_id: int

class ChatMessageResponse(ChatMessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
