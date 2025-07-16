from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.chat import ChatMessage
from services.llm_service import get_groq_reply

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_user_and_bot_message(self, greeting_id: int, user_content: str) -> tuple[ChatMessage, ChatMessage]:
        # Save user message
        user_msg = ChatMessage(
            greeting_id=greeting_id,
            sender="user",
            content=user_content
        )
        self.db.add(user_msg)
        await self.db.commit()
        await self.db.refresh(user_msg)

        # Fetch chat history for context
        history = await self.get_messages_for_greeting(greeting_id)
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for msg in history:
            messages.append({"role": msg.sender if msg.sender in ("user", "assistant", "bot") else "user", "content": msg.content})
        messages.append({"role": "user", "content": user_content})

        # Get bot reply from Groq LLM
        bot_reply = await get_groq_reply(messages)

        # Save bot message
        bot_msg = ChatMessage(
            greeting_id=greeting_id,
            sender="bot",
            content=bot_reply
        )
        self.db.add(bot_msg)
        await self.db.commit()
        await self.db.refresh(bot_msg)

        return user_msg, bot_msg

    async def add_message(self, greeting_id: int, sender: str, content: str) -> ChatMessage:
        # For manual message addition (not LLM-driven)
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
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.greeting_id == greeting_id)
            .order_by(ChatMessage.timestamp)
        )
        return result.scalars().all()
