from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse
from app.services.chat_service import ChatService
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=ChatMessageResponse)
async def add_message(msg_in: ChatMessageCreate, db: AsyncSession = Depends(get_db)):
    service = ChatService(db)
    message = await service.add_message(
        greeting_id=msg_in.greeting_id,
        sender=msg_in.sender,
        content=msg_in.content
    )
    return message

@router.get("/{greeting_id}", response_model=list[ChatMessageResponse])
async def get_messages(greeting_id: int, db: AsyncSession = Depends(get_db)):
    service = ChatService(db)
    messages = await service.get_messages_for_greeting(greeting_id)
    return messages
