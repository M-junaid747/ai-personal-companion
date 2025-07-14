from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.greeting import Greeting
import uuid

class GreetingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_greeting(self, sender_name: str, recipient_name: str, message: str) -> Greeting:
        link_token = str(uuid.uuid4())
        greeting = Greeting(
            sender_name=sender_name,
            recipient_name=recipient_name,
            message=message,
            link_token=link_token
        )
        self.db.add(greeting)
        await self.db.commit()
        await self.db.refresh(greeting)
        return greeting

    async def get_greeting_by_token(self, token: str) -> Greeting | None:
        result = await self.db.execute(select(Greeting).where(Greeting.link_token == token))
        return result.scalars().first()
