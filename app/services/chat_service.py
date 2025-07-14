from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.chat import ChatMessage

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_message(self, greeting_id: int, sender: str, content: str) -> ChatMessage:
        message = ChatMessage(
            greeting_id=greeting_id,
            sender=sender,
            content=content
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages_for_greeting(self, greeting_id: int) -> list[ChatMessage]:
        result = await self.db.execute(select(ChatMessage).where(ChatMessage.greeting_id == greeting_id).order_by(ChatMessage.timestamp))
        return result.scalars().all()
