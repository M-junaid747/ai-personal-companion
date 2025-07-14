from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GreetingBase(BaseModel):
    sender_name: str
    recipient_name: str
    message: str

class GreetingCreate(GreetingBase):
    pass

class GreetingResponse(GreetingBase):
    id: int
    link_token: str
    created_at: datetime

    class Config:
        orm_mode = True
